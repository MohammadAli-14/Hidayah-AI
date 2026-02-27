"""
Hidayah AI — Tafseer API Adapter
Fetches ayah-specific Tafseer from AlQuran.cloud editions.
"""

import requests
import streamlit as st
from utils.config import (
    QURAN_API_BASE,
    TAFSEER_EDITIONS,
    DEFAULT_TAFSEER_EDITION,
    TAFSEER_SOURCE_TARGET_COUNT,
    TAFSEER_PREFERRED_BY_LANGUAGE,
)
from utils.evidence import normalize_tafseer


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_tafseer_for_ayah(
    surah_number: int,
    ayah_number: int,
    edition: str = DEFAULT_TAFSEER_EDITION,
) -> dict | None:
    """Fetch Tafseer text for a single ayah from AlQuran.cloud."""
    if edition not in TAFSEER_EDITIONS:
        edition = DEFAULT_TAFSEER_EDITION

    url = f"{QURAN_API_BASE}/ayah/{surah_number}:{ayah_number}/{edition}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 200:
            return None

        data = payload.get("data", {})
        text = data.get("text", "")

        return normalize_tafseer(
            source_id=edition,
            source_name=TAFSEER_EDITIONS.get(edition, edition),
            surah_number=surah_number,
            ayah_number=ayah_number,
            text=text,
            url=url,
            language=edition.split(".", 1)[0] if "." in edition else "",
            citation_id=f"tafsir:{edition}:{surah_number}:{ayah_number}",
            canonical_url=url,
            link_type="api_fallback",
            canonical_status="unverified",
            source_rank=1,
            metadata={
                "edition": edition,
                "edition_name": TAFSEER_EDITIONS.get(edition, edition),
                "api_url": url,
                "canonical_url_human": "",
            },
        )

    except requests.RequestException:
        return None


def list_tafseer_sources() -> dict[str, str]:
    """Return available Tafseer sources for UI selection."""
    return TAFSEER_EDITIONS.copy()


@st.cache_data(ttl=86400, show_spinner=False)
def discover_tafseer_editions(language: str) -> list[dict]:
    """Discover available Tafseer editions for a language from AlQuran.cloud."""
    normalized_language = (language or "").strip().lower()
    if normalized_language not in {"ar", "en", "ur"}:
        return []

    # First attempt: server-side filtered editions endpoint
    filtered_url = (
        f"{QURAN_API_BASE}/edition"
        f"?format=text&type=tafsir&language={normalized_language}"
    )

    try:
        response = requests.get(filtered_url, timeout=20)
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") == 200:
            entries = payload.get("data", [])
            if entries:
                return [
                    {
                        "identifier": entry.get("identifier", ""),
                        "name": entry.get("name", ""),
                        "english_name": entry.get("englishName", ""),
                        "language": entry.get("language", normalized_language),
                        "type": entry.get("type", "tafsir"),
                    }
                    for entry in entries
                    if entry.get("identifier")
                ]
    except requests.RequestException:
        pass

    # Fallback: query all editions and filter locally
    try:
        response = requests.get(f"{QURAN_API_BASE}/edition", timeout=20)
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 200:
            return []

        entries = []
        for entry in payload.get("data", []):
            entry_type = entry.get("type")
            if normalized_language == "ar" and entry_type != "tafsir":
                continue
            if normalized_language in {"en", "ur"} and entry_type not in {"tafsir", "translation"}:
                continue
            if entry.get("format") != "text":
                continue
            if entry.get("language") != normalized_language:
                continue
            identifier = entry.get("identifier")
            if not identifier:
                continue
            entries.append(
                {
                    "identifier": identifier,
                    "name": entry.get("name", ""),
                    "english_name": entry.get("englishName", ""),
                    "language": entry.get("language", normalized_language),
                    "type": entry_type or "tafsir",
                }
            )
        return entries
    except requests.RequestException:
        return []


def _rank_discovered_sources(language: str, discovered: list[dict]) -> list[dict]:
    """Rank discovered tafseer editions by preference list then stable name order."""
    preferred = TAFSEER_PREFERRED_BY_LANGUAGE.get(language, [])
    preferred_index = {edition: idx for idx, edition in enumerate(preferred)}

    def sort_key(item: dict):
        identifier = item.get("identifier", "")
        source_type = (item.get("type") or "").lower()
        type_rank = 0 if source_type == "tafsir" else 1
        preferred_rank = preferred_index.get(identifier, len(preferred) + 99)
        display_name = (item.get("english_name") or item.get("name") or identifier).lower()
        return type_rank, preferred_rank, display_name

    return sorted(discovered, key=sort_key)


def get_ranked_tafseer_sources(language: str, max_sources: int = TAFSEER_SOURCE_TARGET_COUNT) -> list[dict]:
    """Return ranked native tafseer sources for a language."""
    normalized_language = (language or "").strip().lower()
    discovered = discover_tafseer_editions(normalized_language)
    ranked = _rank_discovered_sources(normalized_language, discovered)
    return ranked[:max_sources]


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_multisource_tafseer_for_ayah(
    surah_number: int,
    ayah_number: int,
    language: str,
    max_sources: int = TAFSEER_SOURCE_TARGET_COUNT,
) -> list[dict]:
    """Fetch up to top-N native tafseer sources for an ayah in the requested language."""
    requested_language = (language or "").strip().lower()
    sources = get_ranked_tafseer_sources(language=requested_language, max_sources=max_sources)
    resolved_language = requested_language

    if not sources and requested_language in {"en", "ur"}:
        resolved_language = "ar"
        sources = get_ranked_tafseer_sources(language=resolved_language, max_sources=max_sources)

    tafseer_items = []

    for rank, source in enumerate(sources, start=1):
        edition = source.get("identifier", "")
        if not edition:
            continue
        url = f"{QURAN_API_BASE}/ayah/{surah_number}:{ayah_number}/{edition}"

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            payload = response.json()
            if payload.get("code") != 200:
                continue
            data = payload.get("data", {})
            text = data.get("text", "")
            if not text:
                continue

            tafseer_items.append(
                normalize_tafseer(
                    source_id=edition,
                    source_name=source.get("english_name") or source.get("name") or edition,
                    surah_number=surah_number,
                    ayah_number=ayah_number,
                    text=text,
                    url=url,
                    language=source.get("language") or (edition.split(".", 1)[0] if "." in edition else resolved_language),
                    citation_id=f"tafsir:{edition}:{surah_number}:{ayah_number}",
                    canonical_url=url,
                    link_type="api_fallback",
                    canonical_status="unverified",
                    source_rank=rank,
                    metadata={
                        "edition": edition,
                        "edition_name": source.get("name", ""),
                        "edition_english_name": source.get("english_name", ""),
                        "language": source.get("language") or resolved_language,
                        "source_type": source.get("type", "tafsir"),
                        "requested_language": requested_language,
                        "fallback_language_used": resolved_language != requested_language,
                        "api_url": url,
                        "canonical_url_human": "",
                    },
                )
            )
        except requests.RequestException:
            continue

    return tafseer_items
