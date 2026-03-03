"""
Hidayah AI — Sunnah.com Hadith API Adapter
Fetches authenticated hadith with grades from the sunnah.com REST API.
Provides verified hadith text with narrator chains and scholarly grades.

API docs: https://sunnah.api-docs.io/
"""

import requests
import streamlit as st
from utils.config import (
    SUNNAH_API_KEY,
    SUNNAH_API_BASE,
    HADITH_COLLECTIONS,
    HADITH_MAX_RESULTS,
)
from utils.evidence import normalize_hadith
from utils.logger import get_logger
from utils.retry import get_with_retry

log = get_logger("sunnah_api")

_HEADERS = {}


def _get_headers() -> dict:
    """Build API headers with key (cached for session)."""
    global _HEADERS
    if not _HEADERS and SUNNAH_API_KEY:
        _HEADERS = {"x-api-key": SUNNAH_API_KEY}
    return _HEADERS


def _grade_label(grades: list[dict]) -> str:
    """Extract the best authentication grade from a hadith's grade list.

    Returns one of: Sahih, Hasan, Da'if, or the raw grade string.
    """
    if not grades:
        return "Unknown"
    # Take the first (primary) grade
    grade_text = (grades[0].get("grade") or "").strip()
    lowered = grade_text.lower()

    if "sahih" in lowered:
        return "Sahih"
    if "hasan" in lowered:
        return "Hasan"
    if "da'if" in lowered or "daif" in lowered or "weak" in lowered:
        return "Da'if"
    if "maudu" in lowered or "fabricated" in lowered:
        return "Fabricated"
    return grade_text or "Unknown"


def _grade_to_confidence(grade: str) -> str:
    """Map hadith grade to confidence level."""
    grade_lower = grade.lower()
    if "sahih" in grade_lower:
        return "verified"
    if "hasan" in grade_lower:
        return "domain_verified"
    return "unverified"


@st.cache_data(ttl=3600, show_spinner=False)
def search_hadith_by_keyword(
    keyword: str,
    collection: str = "",
    max_results: int = HADITH_MAX_RESULTS,
) -> list[dict]:
    """Search for hadith by keyword across collections.

    Args:
        keyword: Search term (e.g., "fasting ramadan").
        collection: Optional specific collection (e.g., "bukhari"). Empty = all.
        max_results: Maximum results to return.

    Returns:
        List of normalized hadith evidence dicts.
    """
    if not SUNNAH_API_KEY:
        log.warning("SUNNAH_API_KEY not configured — skipping sunnah.com search")
        return []

    headers = _get_headers()
    results = []

    # Search across priority collections if none specified
    collections_to_search = (
        [collection] if collection
        else ["bukhari", "muslim", "abudawud", "tirmidhi", "nasai", "ibnmajah"]
    )

    for coll_name in collections_to_search:
        if len(results) >= max_results:
            break

        url = f"{SUNNAH_API_BASE}/hadiths"
        params = {
            "collection": coll_name,
            "limit": min(max_results - len(results), 5),
            "page": 1,
        }

        try:
            log.info(f"Searching sunnah.com: collection={coll_name}, keyword='{keyword[:60]}'")
            resp = get_with_retry(url, headers=headers, params=params, timeout=12, label=f"sunnah:search:{coll_name}")
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("data", []):
                hadith_en = ""
                hadith_ar = ""
                for body in item.get("hadith", []):
                    lang = body.get("lang", "")
                    if lang == "en":
                        hadith_en = body.get("body", "")
                    elif lang == "ar":
                        hadith_ar = body.get("body", "")

                text = hadith_en or hadith_ar
                if not text:
                    continue

                grades = item.get("grades", [])
                grade = _grade_label(grades)
                hadith_number = item.get("hadithNumber", "")
                book_number = item.get("bookNumber", "")
                collection_display = HADITH_COLLECTIONS.get(coll_name, coll_name)
                canonical_url = f"https://sunnah.com/{coll_name}/{book_number}/{hadith_number}" if book_number else f"https://sunnah.com/{coll_name}"

                results.append(
                    normalize_hadith(
                        source_name=f"Sunnah.com — {collection_display}",
                        title=f"{collection_display} {hadith_number}",
                        excerpt=text.strip(),
                        url=canonical_url,
                        language="en" if hadith_en else "ar",
                        citation_id=f"hadith:sunnah:{coll_name}:{hadith_number}",
                        canonical_url=canonical_url,
                        link_type="api_verified",
                        canonical_status=_grade_to_confidence(grade),
                        authority="Hadith Corpus — Authenticated",
                        metadata={
                            "collection": coll_name,
                            "collection_name": collection_display,
                            "hadith_number": str(hadith_number),
                            "book_number": str(book_number),
                            "grade": grade,
                            "grade_raw": grades,
                            "source_type": "hadith_collection",
                            "provider": "sunnah.com",
                        },
                    )
                )

                if len(results) >= max_results:
                    break

        except requests.RequestException as e:
            log.warning(f"sunnah.com API error for {coll_name}: {e}")
            continue

    log.info(f"sunnah.com returned {len(results)} hadith results")
    return results[:max_results]


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_hadith_by_reference(
    collection: str,
    hadith_number: str,
) -> dict | None:
    """Fetch a specific hadith by collection and number.

    Args:
        collection: Collection name (e.g., "bukhari").
        hadith_number: Hadith number within collection.

    Returns:
        Normalized hadith dict or None.
    """
    if not SUNNAH_API_KEY:
        log.warning("SUNNAH_API_KEY not configured")
        return None

    headers = _get_headers()
    url = f"{SUNNAH_API_BASE}/hadiths/{collection}:{hadith_number}"

    try:
        resp = get_with_retry(url, headers=headers, timeout=12, label=f"sunnah:fetch:{collection}:{hadith_number}")
        resp.raise_for_status()
        item = resp.json()

        hadith_en = ""
        hadith_ar = ""
        for body in item.get("hadith", []):
            lang = body.get("lang", "")
            if lang == "en":
                hadith_en = body.get("body", "")
            elif lang == "ar":
                hadith_ar = body.get("body", "")

        text = hadith_en or hadith_ar
        if not text:
            return None

        grades = item.get("grades", [])
        grade = _grade_label(grades)
        book_number = item.get("bookNumber", "")
        collection_display = HADITH_COLLECTIONS.get(collection, collection)
        canonical_url = f"https://sunnah.com/{collection}/{book_number}/{hadith_number}" if book_number else f"https://sunnah.com/{collection}"

        return normalize_hadith(
            source_name=f"Sunnah.com — {collection_display}",
            title=f"{collection_display} {hadith_number}",
            excerpt=text.strip(),
            url=canonical_url,
            language="en" if hadith_en else "ar",
            citation_id=f"hadith:sunnah:{collection}:{hadith_number}",
            canonical_url=canonical_url,
            link_type="api_verified",
            canonical_status=_grade_to_confidence(grade),
            authority="Hadith Corpus — Authenticated",
            metadata={
                "collection": collection,
                "collection_name": collection_display,
                "hadith_number": str(hadith_number),
                "book_number": str(book_number),
                "grade": grade,
                "grade_raw": grades,
                "source_type": "hadith_collection",
                "provider": "sunnah.com",
            },
        )

    except requests.RequestException as e:
        log.warning(f"sunnah.com fetch error for {collection}:{hadith_number}: {e}")
        return None


def is_available() -> bool:
    """Check if sunnah.com API is configured and reachable."""
    return bool(SUNNAH_API_KEY)
