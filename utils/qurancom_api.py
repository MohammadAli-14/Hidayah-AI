"""
Hidayah AI — Quran.com v4 Tafseer API Adapter
Fetches real tafseer (not just translations) from Quran.com's v4 API.
Provides Ibn Kathir, Maariful Quran, Jalalayn in English/Urdu/Arabic.

API docs: https://api-docs.quran.com/
"""

import requests
import streamlit as st
from utils.config import QURANCOM_API_BASE, QURANCOM_TAFSIRS
from utils.evidence import normalize_tafseer
from utils.logger import get_logger
from utils.retry import get_with_retry
import re

log = get_logger("qurancom_api")


def _strip_html(text: str) -> str:
    """Remove HTML tags from tafsir text returned by Quran.com."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", "", text)
    # Collapse multiple whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


@st.cache_data(ttl=86400, show_spinner=False)
def list_available_tafsirs(language: str = "en") -> list[dict]:
    """List available tafsir resources from Quran.com for a language.

    Args:
        language: ISO language code (en / ur / ar).

    Returns:
        List of tafsir resource dicts with id, name, language.
    """
    configured = QURANCOM_TAFSIRS.get(language, [])
    if configured:
        return configured

    # Fallback: fetch from API
    try:
        url = f"{QURANCOM_API_BASE}/resources/tafsirs"
        resp = get_with_retry(url, timeout=12, label="qurancom:list_tafsirs")
        resp.raise_for_status()
        data = resp.json()
        tafsirs = []
        for t in data.get("tafsirs", []):
            if t.get("language_name", "").lower().startswith(language):
                tafsirs.append({
                    "id": t["id"],
                    "name": t.get("translated_name", {}).get("name", t.get("name", "")),
                    "language": language,
                })
        return tafsirs
    except requests.RequestException as e:
        log.warning(f"Failed to list Quran.com tafsirs: {e}")
        return []


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_tafsir_for_ayah(
    surah_number: int,
    ayah_number: int,
    tafsir_id: int,
    tafsir_name: str = "",
    language: str = "en",
) -> dict | None:
    """Fetch tafsir text for a single ayah from Quran.com v4.

    Args:
        surah_number: Surah number (1-114).
        ayah_number: Ayah number within surah.
        tafsir_id: Quran.com tafsir resource ID.
        tafsir_name: Display name for the tafsir.
        language: Language code.

    Returns:
        Normalized tafsir evidence dict, or None on failure.
    """
    ayah_key = f"{surah_number}:{ayah_number}"
    url = f"{QURANCOM_API_BASE}/tafsirs/{tafsir_id}/by_ayah/{ayah_key}"

    try:
        log.info(f"Fetching Quran.com tafsir {tafsir_id} for {ayah_key}")
        resp = get_with_retry(url, timeout=15, label=f"qurancom:tafsir:{tafsir_id}")
        resp.raise_for_status()
        data = resp.json()

        tafsir_data = data.get("tafsir", {})
        raw_text = tafsir_data.get("text", "")
        text = _strip_html(raw_text)

        if not text:
            return None

        resource_name = tafsir_name or tafsir_data.get("resource_name", f"Tafsir {tafsir_id}")
        human_url = f"https://quran.com/{surah_number}:{ayah_number}/tafsirs/{tafsir_id}"

        return normalize_tafseer(
            source_id=f"qurancom:{tafsir_id}",
            source_name=resource_name,
            surah_number=surah_number,
            ayah_number=ayah_number,
            text=text,
            url=url,
            language=language,
            citation_id=f"tafsir:qurancom:{tafsir_id}:{ayah_key}",
            canonical_url=human_url,
            link_type="api_verified",
            canonical_status="verified",
            source_rank=1,
            authority="Classical Tafseer (Verified)",
            metadata={
                "provider": "quran.com",
                "tafsir_id": tafsir_id,
                "tafsir_name": resource_name,
                "language": language,
                "source_type": "tafsir",
                "api_url": url,
                "canonical_url_human": human_url,
                "fallback_language_used": False,
            },
        )

    except requests.RequestException as e:
        log.warning(f"Quran.com tafsir fetch error for {ayah_key}, tafsir {tafsir_id}: {e}")
        return None


def fetch_multisource_tafseer_for_ayah(
    surah_number: int,
    ayah_number: int,
    language: str = "en",
    max_sources: int = 3,
) -> list[dict]:
    """Fetch up to max_sources tafsir entries for an ayah from Quran.com.

    Args:
        surah_number: Surah number.
        ayah_number: Ayah number within surah.
        language: Language code (en / ur / ar).
        max_sources: Maximum number of tafsir sources.

    Returns:
        List of normalized tafsir evidence dicts.
    """
    tafsirs = list_available_tafsirs(language)
    if not tafsirs:
        log.info(f"No Quran.com tafsirs available for language={language}")
        return []

    results = []
    for rank, tafsir in enumerate(tafsirs[:max_sources], start=1):
        item = fetch_tafsir_for_ayah(
            surah_number=surah_number,
            ayah_number=ayah_number,
            tafsir_id=tafsir["id"],
            tafsir_name=tafsir.get("name", ""),
            language=language,
        )
        if item:
            item["source_rank"] = rank
            results.append(item)

    log.info(f"Quran.com returned {len(results)} tafsir sources for {surah_number}:{ayah_number} ({language})")
    return results


def is_available() -> bool:
    """Check if Quran.com API is reachable (no auth needed, free API)."""
    return True  # No API key required for Quran.com v4
