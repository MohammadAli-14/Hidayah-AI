"""
Hidayah AI — Evidence Normalization
Normalizes Tafseer/Hadith payloads for consistent UI rendering and citations.
"""


def normalize_tafseer(
    source_id: str,
    source_name: str,
    surah_number: int,
    ayah_number: int,
    text: str,
    url: str = "",
    language: str = "",
    citation_id: str = "",
    canonical_url: str = "",
    link_type: str = "api_fallback",
    canonical_status: str = "unverified",
    source_rank: int = 0,
    authority: str = "Classical Tafseer",
    metadata: dict | None = None,
) -> dict:
    """Normalize a Tafseer entry to a standard schema."""
    reference = f"{surah_number}:{ayah_number}"
    resolved_canonical = canonical_url or url or ""
    resolved_citation_id = citation_id or f"tafsir:{source_id}:{reference}"

    return {
        "id": resolved_citation_id,
        "type": "tafsir",
        "citation_id": resolved_citation_id,
        "source_id": source_id,
        "source_name": source_name,
        "reference": reference,
        "excerpt": (text or "").strip(),
        "url": resolved_canonical,
        "canonical_url": resolved_canonical,
        "link_type": link_type,
        "canonical_status": canonical_status,
        "language": language,
        "source_rank": source_rank,
        "metadata": metadata or {},
        "authority": authority,
    }


def normalize_hadith(
    source_name: str,
    title: str,
    excerpt: str,
    url: str,
    language: str = "en",
    citation_id: str = "",
    canonical_url: str = "",
    link_type: str = "search_fallback",
    canonical_status: str = "unverified",
    source_rank: int = 0,
    authority: str = "Hadith Reference",
    metadata: dict | None = None,
) -> dict:
    """Normalize a Hadith/search-derived entry to a standard schema."""
    source_id = source_name.lower().replace(" ", "_")
    reference = title
    resolved_canonical = canonical_url or url or ""
    resolved_citation_id = citation_id or f"hadith:{source_id}:{reference}:{resolved_canonical}".lower()

    return {
        "id": resolved_citation_id,
        "type": "hadith",
        "citation_id": resolved_citation_id,
        "source_id": source_id,
        "source_name": source_name,
        "reference": reference,
        "excerpt": (excerpt or "").strip(),
        "url": resolved_canonical,
        "canonical_url": resolved_canonical,
        "link_type": link_type,
        "canonical_status": canonical_status,
        "language": language,
        "source_rank": source_rank,
        "metadata": metadata or {},
        "authority": authority,
    }
