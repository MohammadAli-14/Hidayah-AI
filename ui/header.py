"""
Hidayah AI — Header Component
Renders the top header bar: Ramadan day counter, current Surah info, verse range, and action icons.
"""

import streamlit as st
from datetime import date
from utils.config import GOLD, get_logo_base64


def _get_ramadan_day(juz_num: int) -> str:
    """
    Derive the Ramadan day from the currently selected Juz.
    Since this is a 30-Day companion, Juz N naturally corresponds to Day N.
    """
    if 1 <= juz_num <= 30:
        return f"Ramadan Day {juz_num}"
    return "Ramadan 2026"


def render_header(ayahs: list[dict], current_index: int = 0):
    """Render the top header bar with Surah info and Ramadan day."""

    current_juz = st.session_state.get("current_juz", 1)
    ramadan_day = _get_ramadan_day(current_juz)

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
            min-height: 4rem;
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
            <div style="display: flex; align-items: center; gap: 0.75rem; width: 2.5rem; height: 2.5rem;">
                <!-- Placeholder for absolute placed Streamlit Button -->
            </div>
        </div>
        """
    )
    
    logo_b64 = get_logo_base64()
    
    st.markdown(
        f"""
        <style>
        .scholar-toggle-anchor {{
            position: relative;
            width: 100%;
            height: 0px;
            overflow: visible;
        }}
        
        button[title="Toggle Scholar Agent"] {{
            position: absolute !important;
            right: 1.5rem !important;
            top: -3.85rem !important;
            width: 2.5rem !important;
            height: 2.5rem !important;
            padding: 0 !important;
            border-radius: 50% !important;
            background-image: url('{logo_b64}') !important;
            background-size: cover !important;
            background-position: center !important;
            border: 2px solid {GOLD} !important;
            color: transparent !important;
            box-shadow: 0 0 0 2px #0F172A, 0 4px 10px rgba(0,0,0,0.5) !important;
            z-index: 100 !important;
            transition: all 0.2s ease !important;
            background-color: transparent !important;
        }}
        
        button[title="Toggle Scholar Agent"]:hover {{
            transform: scale(1.08) !important;
            box-shadow: 0 0 15px {GOLD}, 0 0 0 2px #0F172A !important;
            border-color: #F3E5AB !important;
        }}
        
        button[title="Toggle Scholar Agent"] p {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="scholar-toggle-anchor"></div>', unsafe_allow_html=True)
        if st.button("HA", help="Toggle Scholar Agent", key="btn_toggle_scholar_header", use_container_width=False):
            st.session_state.show_scholar_agent = not st.session_state.show_scholar_agent
            st.rerun()
