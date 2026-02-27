"""
Hidayah AI — Hadith Retrieval Adapter
Uses trusted-domain web retrieval to surface relevant Hadith references.
"""

import streamlit as st
from urllib.parse import urlparse
from utils.config import HADITH_TRUSTED_DOMAINS, HADITH_MAX_RESULTS
from utils.evidence import normalize_hadith
from agents.web_search import search_web


def _trusted_host(url: str) -> str:
    """Return matched trusted host using strict hostname matching, else empty."""
    try:
        hostname = (urlparse(url).hostname or "").lower().strip()
    except Exception:
        return ""

    if hostname.startswith("www."):
        hostname = hostname[4:]

    for domain in HADITH_TRUSTED_DOMAINS:
        normalized = domain.lower().strip()
        if hostname == normalized or hostname.endswith(f".{normalized}"):
            return normalized
    return ""


@st.cache_data(ttl=900, show_spinner=False)
def fetch_related_hadith(
    ayah_text_english: str,
    surah_name: str,
    ayah_number: int,
    max_results: int = HADITH_MAX_RESULTS,
) -> list[dict]:
    """Fetch related Hadith references from trusted domains via Tavily."""
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

        trusted_host = _trusted_host(url)
        if not trusted_host:
            continue

        source_name = "Sunnah Reference"
        source_type = "hadith_collection"
        authority = "Hadith Corpus Reference"
        canonical_status = "domain_verified"

        if trusted_host == "sunnah.com":
            source_name = "Sunnah.com"
        elif trusted_host == "islamqa.info":
            source_name = "IslamQA Commentary"
            source_type = "scholarly_commentary"
            authority = "Scholarly Commentary"
            canonical_status = "unverified"

        normalized.append(
            normalize_hadith(
                source_name=source_name,
                title=title or f"Related Hadith — {surah_name} {ayah_number}",
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
                    "trusted_domain": trusted_host,
                    "source_type": source_type,
                },
            )
        )

    return normalized[:max_results]
