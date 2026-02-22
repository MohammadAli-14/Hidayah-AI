"""
Hidayah AI — AlQuran.cloud API Integration
Fetches Juz data (Arabic text, audio URLs, English & Urdu translations).
"""

import requests
import streamlit as st
from utils.config import QURAN_API_BASE, ARABIC_EDITION, ENGLISH_EDITION, URDU_EDITION, ENGLISH_AUDIO_EDITION, URDU_AUDIO_EDITION


@st.cache_data(ttl=3600, show_spinner=False)
def _fetch_juz_edition(juz_number: int, edition: str) -> dict | None:
    """Fetch a specific Juz in a specific edition from AlQuran.cloud."""
    url = f"{QURAN_API_BASE}/juz/{juz_number}/{edition}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 200:
            return data["data"]
        return None
    except requests.RequestException as e:
        st.error(f"Failed to fetch Juz {juz_number} ({edition}): {e}")
        return None


def fetch_juz_arabic(juz_number: int) -> dict | None:
    """Fetch Arabic text + audio URLs for a Juz (Alafasy edition)."""
    return _fetch_juz_edition(juz_number, ARABIC_EDITION)


def fetch_juz_english(juz_number: int) -> dict | None:
    """Fetch English translation for a Juz."""
    return _fetch_juz_edition(juz_number, ENGLISH_EDITION)


def fetch_juz_urdu(juz_number: int) -> dict | None:
    """Fetch Urdu translation for a Juz."""
    return _fetch_juz_edition(juz_number, URDU_EDITION)


def fetch_juz_english_audio(juz_number: int) -> dict | None:
    """Fetch English audio for a Juz (Ibrahim Walk)."""
    return _fetch_juz_edition(juz_number, ENGLISH_AUDIO_EDITION)


def fetch_juz_urdu_audio(juz_number: int) -> dict | None:
    """Fetch Urdu audio for a Juz (Shamshad Ali Khan)."""
    return _fetch_juz_edition(juz_number, URDU_AUDIO_EDITION)


@st.cache_data(ttl=3600, show_spinner="Loading Quranic text...")
def fetch_juz_combined(juz_number: int) -> list[dict]:
    """
    Fetch and merge Arabic, English, and Urdu data for a Juz.
    Returns a list of ayah dicts:
    [
        {
            "number": 1,
            "number_in_surah": 1,
            "surah_number": 1,
            "surah_name": "Al-Faatiha",
            "surah_english_name": "The Opening",
            "arabic": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
            "english": "In the name of God, The Most Gracious, ...",
            "urdu": "شروع اللہ کے نام سے ...",
            "audio_url": "https://cdn.islamic.network/...",
            "page": 1,
            "juz": 1,
        },
        ...
    ]
    """
    arabic_data = fetch_juz_arabic(juz_number)
    english_data = fetch_juz_english(juz_number)
    urdu_data = fetch_juz_urdu(juz_number)
    english_audio_data = fetch_juz_english_audio(juz_number)
    urdu_audio_data = fetch_juz_urdu_audio(juz_number)

    if not arabic_data:
        return []

    arabic_ayahs = arabic_data.get("ayahs", [])
    english_ayahs = english_data.get("ayahs", []) if english_data else []
    urdu_ayahs = urdu_data.get("ayahs", []) if urdu_data else []
    english_audio_ayahs = english_audio_data.get("ayahs", []) if english_audio_data else []
    urdu_audio_ayahs = urdu_audio_data.get("ayahs", []) if urdu_audio_data else []

    # Build lookup dicts by ayah number for quick merging
    english_map = {a["number"]: a.get("text", "") for a in english_ayahs}
    urdu_map = {a["number"]: a.get("text", "") for a in urdu_ayahs}
    english_audio_map = {a["number"]: a.get("audio", "") for a in english_audio_ayahs}
    urdu_audio_map = {a["number"]: a.get("audio", "") for a in urdu_audio_ayahs}

    combined = []
    for ayah in arabic_ayahs:
        num = ayah["number"]
        surah = ayah.get("surah", {})
        combined.append({
            "number": num,
            "number_in_surah": ayah.get("numberInSurah", 0),
            "surah_number": surah.get("number", 0),
            "surah_name": surah.get("englishName", ""),
            "surah_english_name": surah.get("englishNameTranslation", ""),
            "surah_arabic_name": surah.get("name", ""),
            "arabic": ayah.get("text", ""),
            "english": english_map.get(num, ""),
            "urdu": urdu_map.get(num, ""),
            "audio_url": ayah.get("audio", ""),
            "audio_en": english_audio_map.get(num, ""),
            "audio_ur": urdu_audio_map.get(num, ""),
            "audio_secondary": ayah.get("audioSecondary", []),
            "page": ayah.get("page", 0),
            "juz": ayah.get("juz", juz_number),
        })

    return combined


def get_surah_info_for_juz(ayahs: list[dict]) -> list[dict]:
    """Extract unique surah info from a list of ayahs."""
    seen = set()
    surahs = []
    for ayah in ayahs:
        snum = ayah["surah_number"]
        if snum not in seen:
            seen.add(snum)
            surahs.append({
                "number": snum,
                "name": ayah["surah_name"],
                "english_name": ayah["surah_english_name"],
                "arabic_name": ayah.get("surah_arabic_name", ""),
            })
    return surahs
