"""
Hidayah AI — Header Component
Renders the top header bar: Ramadan day counter, current Surah info, verse range, and action icons.
"""

import streamlit as st
from datetime import date
from utils.config import GOLD


def _get_ramadan_day() -> str:
    """
    Estimate the current Ramadan day.
    Ramadan 2026 is estimated to start around Feb 18, 2026.
    This is an approximation — real Islamic calendar depends on moon sighting.
    """
    ramadan_start = date(2026, 2, 18)
    today = date.today()
    delta = (today - ramadan_start).days + 1

    if 1 <= delta <= 30:
        return f"Ramadan Day {delta}"
    elif delta < 1:
        return "Pre-Ramadan"
    else:
        return "Post-Ramadan"


def render_header(ayahs: list[dict], current_index: int = 0):
    """Render the top header bar with Surah info and Ramadan day."""

    ramadan_day = _get_ramadan_day()

    # Determine current surah and verse range from loaded ayahs
    if ayahs:
        current_ayah = ayahs[min(current_index, len(ayahs) - 1)]
        surah_name = current_ayah.get("surah_name", "")
        surah_arabic = current_ayah.get("surah_arabic_name", "")
        verse_num = current_ayah.get("number_in_surah", 0)

        # Find verse range for current page view (show 5 at a time)
        page_start = current_index
        page_end = min(current_index + 5, len(ayahs) - 1)
        start_verse = ayahs[page_start].get("number_in_surah", 0)
        end_verse = ayahs[page_end].get("number_in_surah", 0)
        verse_range = f"Verse {start_verse}–{end_verse}" if start_verse != end_verse else f"Verse {start_verse}"
    else:
        surah_name = "Loading..."
        surah_arabic = ""
        verse_range = ""

    st.html(
        f"""
        <div style="
            display: flex; align-items: center; justify-content: space-between;
            padding: 0.75rem 1.5rem;
            background: rgba(26, 42, 64, 0.7);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(148,163,184,0.15);
            border-radius: 1rem 1rem 0 0;
            margin-bottom: 0;
            font-family: Inter, sans-serif;
        ">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="
                    font-size: 0.8rem; font-weight: 600; color: {GOLD};
                    text-transform: uppercase; letter-spacing: 0.15em;
                ">{ramadan_day}</span>
                <span style="height: 1rem; width: 1px; background: rgba(148,163,184,0.3);"></span>
                <span style="font-size: 1.1rem; color: white; font-family: 'Playfair Display', serif;">
                    {surah_name}
                    <span style="color: #94a3b8; font-size: 0.9rem; font-family: Inter, sans-serif; margin-left: 0.5rem;">
                        {verse_range}
                    </span>
                </span>
                <span style="
                    font-family: 'Amiri', serif; font-size: 1rem; color: rgba(255,255,255,0.5); margin-left: 0.5rem;
                ">{surah_arabic}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="
                    display: inline-flex; align-items: center; justify-content: center;
                    width: 2rem; height: 2rem; border-radius: 50%;
                    background: rgba(6,78,59,1); color: white; font-size: 0.65rem; font-weight: 700;
                    box-shadow: 0 0 0 2px {GOLD}, 0 0 0 4px #0F172A;
                ">HA</span>
            </div>
        </div>
        """
    )
