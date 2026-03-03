"""
Hidayah AI — Hadith Retrieval Adapter
Primary: sunnah.com API (verified hadith with authentication grades).
Fallback: Tavily web search filtered to trusted domains (commentary only).
"""

import streamlit as st
from utils.config import (
    HADITH_TRUSTED_DOMAINS,
    HADITH_MAX_RESULTS,
    HADITH_PROVIDER_PRIMARY,
)
from utils.evidence import normalize_hadith
from utils.trust import trusted_host, COMMENTARY_DOMAINS
from utils.logger import get_logger

log = get_logger("hadith_api")


# ── Primary: sunnah.com API ──────────────────────────────────────

def _fetch_from_sunnah_api(
    ayah_text_english: str,
    surah_name: str,
    ayah_number: int,
    max_results: int,
) -> list[dict]:
    """Fetch hadith from sunnah.com API using keyword search."""
    try:
        from utils.sunnah_api import search_hadith_by_keyword, is_available

        if not is_available():
            log.warning("sunnah.com API not configured, skipping")
            return []

        # Build a focused search keyword from the ayah context
        keyword_parts = []
        if surah_name:
            keyword_parts.append(surah_name)
        if ayah_text_english:
            keyword_parts.append(ayah_text_english[:120])

        keyword = " ".join(keyword_parts).strip()
        if not keyword:
            keyword = f"Quran {surah_name} verse {ayah_number}"

        results = search_hadith_by_keyword(
            keyword=keyword,
            max_results=max_results,
        )
        log.info(f"sunnah.com returned {len(results)} results for {surah_name}:{ayah_number}")
        return results

    except Exception as e:
        log.error(f"sunnah.com adapter error: {e}")
        return []


# ── Fallback: Tavily Web Search (commentary only) ───────────────

def _fetch_web_commentary_fallback(
    ayah_text_english: str,
    surah_name: str,
    ayah_number: int,
    max_results: int,
) -> list[dict]:
    """Fetch scholarly commentary via Tavily web search (NOT hadith corpus)."""
    try:
        from agents.web_search import search_web
    except ImportError:
        log.error("web_search module not available")
        return []

    query = f"{surah_name} {ayah_number} related hadith explanation"
    if ayah_text_english:
        query = f"{query} {ayah_text_english[:140]}"

    domain_filter = " OR ".join(f"site:{d}" for d in HADITH_TRUSTED_DOMAINS)
    full_query = f"{query} {domain_filter}"

    results = search_web(full_query, max_results=max_results)
    normalized = []

    for item in results:
        title = item.get("title", "")
        url = item.get("url", "")
        content = item.get("content", "")

        if not url:
            continue

        trusted = trusted_host(url, HADITH_TRUSTED_DOMAINS)
        if not trusted:
            continue

        is_commentary = trusted_host(url, COMMENTARY_DOMAINS)
        if trusted == "sunnah.com":
            source_name = "Sunnah.com (Web)"
            source_type = "hadith_collection"
            authority = "Hadith Reference (Web-sourced)"
            canonical_status = "domain_verified"
        elif is_commentary:
            source_name = "IslamQA Commentary"
            source_type = "scholarly_commentary"
            authority = "Scholarly Commentary"
            canonical_status = "unverified"
        else:
            source_name = f"{trusted} Reference"
            source_type = "web_reference"
            authority = "Web Reference"
            canonical_status = "unverified"

        normalized.append(
            normalize_hadith(
                source_name=source_name,
                title=title or f"Related Reference — {surah_name} {ayah_number}",
                excerpt=content,
                url=url,
                language="en",
                citation_id=f"hadith:{source_name.lower().replace(' ', '_')}:{url}",
                canonical_url=url,
                link_type="search_fallback",
                canonical_status=canonical_status,
                authority=authority,
                metadata={
                    "surah_name": surah_name,
                    "ayah_number": ayah_number,
                    "trusted_domain": trusted,
                    "source_type": source_type,
                    "provider": "tavily_web",
                },
            )
        )

    return normalized[:max_results]


# ── Public Interface ─────────────────────────────────────────────

@st.cache_data(ttl=900, show_spinner=False)
def fetch_related_hadith(
    ayah_text_english: str,
    surah_name: str,
    ayah_number: int,
    max_results: int = HADITH_MAX_RESULTS,
) -> list[dict]:
    """Fetch related Hadith references using the configured provider strategy.

    Primary: sunnah.com API (authenticated hadith with grades).
    Fallback: Tavily web search (commentary, not authoritative hadith).
    """
    results = []

    if HADITH_PROVIDER_PRIMARY == "sunnah_api":
        results = _fetch_from_sunnah_api(
            ayah_text_english=ayah_text_english,
            surah_name=surah_name,
            ayah_number=ayah_number,
            max_results=max_results,
        )

    if not results:
        log.info("Primary hadith source returned 0 results, falling back to web search")
        results = _fetch_web_commentary_fallback(
            ayah_text_english=ayah_text_english,
            surah_name=surah_name,
            ayah_number=ayah_number,
            max_results=max_results,
        )

    return results[:max_results]
