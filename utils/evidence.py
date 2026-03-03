"""
Hidayah AI — Evidence Normalization
Normalizes Tafseer/Hadith payloads for consistent UI rendering and citations.
Provides shared confidence formatting for all UI surfaces.
"""


# ── Shared Confidence Formatter ──────────────────────────────────
def format_confidence(
    status: str,
    source_type: str = "",
    used_fallback: bool = False,
    hadith_grade: str = "",
) -> str:
    """Return a user-friendly confidence label for source display.

    Used by verse_context_panel, chat_panel, and any future citation surface.

    Args:
        status: canonical_status field (verified / domain_verified / unverified).
        source_type: e.g. "tafsir", "hadith_collection", "scholarly_commentary".
        used_fallback: Whether a language fallback was used.
        hadith_grade: Optional hadith authentication grade (Sahih / Hasan / Da'if).
    """
    normalized_status = (status or "unverified").lower()
    normalized_type = (source_type or "").lower()

    # Hadith-specific grading takes priority
    if hadith_grade:
        grade_lower = hadith_grade.lower()
        if "sahih" in grade_lower:
            base = "High — Sahih"
        elif "hasan" in grade_lower:
            base = "Moderate — Hasan"
        elif "da'if" in grade_lower or "daif" in grade_lower or "weak" in grade_lower:
            base = "Low — Da'if (Weak)"
        elif "fabricated" in grade_lower or "maudu" in grade_lower:
            base = "Rejected — Fabricated"
        else:
            base = f"Graded: {hadith_grade}"
    elif normalized_status in {"verified", "domain_verified"} and normalized_type == "tafsir":
        base = "High"
    elif normalized_status in {"verified", "domain_verified"}:
        base = "Moderate"
    elif normalized_status == "unverified":
        base = "Needs Verification"
    else:
        base = "Needs Verification"

    if used_fallback:
        return f"{base} (Fallback Source)"
    return base


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
