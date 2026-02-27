"""
Hidayah AI — Context Retriever
Builds grounded Tafseer/Hadith context for a given ayah.
"""

from utils.tafsir_api import fetch_multisource_tafseer_for_ayah
from utils.hadith_api import fetch_related_hadith
from utils.config import TAFSEER_SOURCE_TARGET_COUNT


def get_context_bundle_for_ayah(ayah: dict) -> dict:
    """Retrieve normalized Tafseer/Hadith evidence for a single ayah."""
    if not ayah:
        return {"tafsir": None, "tafsir_sources": [], "hadith": []}

    surah_number = ayah.get("surah_number", 0)
    ayah_number = ayah.get("number_in_surah", 0)

    tafsir_sources = fetch_multisource_tafseer_for_ayah(
        surah_number=surah_number,
        ayah_number=ayah_number,
        language="en",
        max_sources=TAFSEER_SOURCE_TARGET_COUNT,
    )

    hadith = fetch_related_hadith(
        ayah_text_english=ayah.get("english", ""),
        surah_name=ayah.get("surah_name", ""),
        ayah_number=ayah_number,
    )

    return {
        "tafsir": tafsir_sources[0] if tafsir_sources else None,
        "tafsir_sources": tafsir_sources,
        "hadith": hadith,
    }


def get_context_bundle_for_window(
    ayah_window: list[dict],
    tafseer_language: str = "en",
    max_tafseer_sources: int = TAFSEER_SOURCE_TARGET_COUNT,
) -> dict:
    """Retrieve tafseer + hadith evidence for each ayah in a visible window."""
    if not ayah_window:
        return {
            "tafsir_by_ayah": {},
            "hadith_by_ayah": {},
            "citations": [],
        }

    tafsir_by_ayah = {}
    hadith_by_ayah = {}
    citations = []
    seen_citation_ids = set()

    for ayah in ayah_window:
        surah_number = ayah.get("surah_number", 0)
        ayah_number = ayah.get("number_in_surah", 0)
        ayah_ref = f"{surah_number}:{ayah_number}"

        tafsir_sources = fetch_multisource_tafseer_for_ayah(
            surah_number=surah_number,
            ayah_number=ayah_number,
            language=tafseer_language,
            max_sources=max_tafseer_sources,
        )
        hadith_sources = fetch_related_hadith(
            ayah_text_english=ayah.get("english", ""),
            surah_name=ayah.get("surah_name", ""),
            ayah_number=ayah_number,
        )

        tafsir_by_ayah[ayah_ref] = tafsir_sources
        hadith_by_ayah[ayah_ref] = hadith_sources

        for item in tafsir_sources:
            citation = {
                **item,
                "metadata": {
                    **item.get("metadata", {}),
                    "ayah_ref": ayah_ref,
                },
            }
            citation_id = citation.get("citation_id") or citation.get("id")
            if citation_id and citation_id in seen_citation_ids:
                continue
            if citation_id:
                seen_citation_ids.add(citation_id)
            citations.append(citation)

        for item in hadith_sources[:2]:
            citation = {
                **item,
                "metadata": {
                    **item.get("metadata", {}),
                    "ayah_ref": ayah_ref,
                },
            }
            citation_id = citation.get("citation_id") or citation.get("id")
            if citation_id and citation_id in seen_citation_ids:
                continue
            if citation_id:
                seen_citation_ids.add(citation_id)
            citations.append(citation)

    return {
        "tafsir_by_ayah": tafsir_by_ayah,
        "hadith_by_ayah": hadith_by_ayah,
        "citations": citations,
    }
