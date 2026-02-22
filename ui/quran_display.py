"""
Hidayah AI — Quran Display Component
Renders the dual-pane view: Arabic text (RTL) on the left, English + Urdu translations on the right.
"""

import streamlit as st
from utils.config import GOLD, MIDNIGHT_BLUE

AYAHS_PER_PAGE = 5


def render_quran_view(ayahs: list[dict], current_index: int = 0):
    """
    Render the dual-pane Quran display with pagination.
    Shows AYAHS_PER_PAGE ayahs at a time starting from current_index.
    """

    if not ayahs:
        st.html(
            """
            <div style="
                display: flex; align-items: center; justify-content: center;
                height: 400px; color: #94a3b8; font-size: 1.1rem;
                font-family: Inter, sans-serif;
            ">
                <div style="text-align: center;">
                    <p style="font-size: 2rem; margin-bottom: 0.5rem;">📖</p>
                    <p>Select a Juz from the sidebar to begin reading</p>
                </div>
            </div>
            """
        )
        return

    # Paginate (page-locked to avoid drifting windows)
    total = len(ayahs)
    safe_index = min(current_index, total - 1)
    start = (safe_index // AYAHS_PER_PAGE) * AYAHS_PER_PAGE
    end = min(start + AYAHS_PER_PAGE, total)
    page_ayahs = ayahs[start:end]

    # Build the dual-pane HTML for each ayah
    rows_html = ""
    for i, ayah in enumerate(page_ayahs):
        actual_idx = start + i
        is_playing = st.session_state.get("is_playing", False) and actual_idx == st.session_state.get("current_ayah_index", 0)

        playing_border = f"border-left: 3px solid {GOLD}; padding-left: 1rem;" if is_playing else ""
        playing_border_rtl = f"border-right: 3px solid {GOLD}; padding-right: 1rem;" if is_playing else ""

        ayah_num = ayah.get("number_in_surah", "")
        surah_name = ayah.get("surah_name", "")

        rows_html += f"""
        <div style="
            display: flex; border-bottom: 1px solid rgba(148,163,184,0.1);
            min-height: 120px; position: relative;
        ">
            <!-- Arabic Pane (Left) -->
            <div style="
                width: 50%; padding: 1.5rem 2rem;
                display: flex; align-items: center; justify-content: center;
                border-right: 1px solid rgba(148,163,184,0.1);
                background: rgba(255,255,255,0.02);
                {playing_border_rtl}
            ">
                <div style="text-align: center; width: 100%;">
                    <p style="
                        font-family: 'Amiri', serif; font-size: 1.7rem; line-height: 2.2;
                        color: #e2e8f0; direction: rtl; text-align: center;
                        margin: 0;
                    ">{ayah.get('arabic', '')}</p>
                    <div style="display:flex; align-items:center; justify-content:center; gap:0.5rem; margin-top:0.5rem;">
                        <span style="
                            display:inline-flex; align-items:center; justify-content:center;
                            min-width: 1.5rem; height: 1.5rem; border-radius: 50%;
                            border: 1px solid rgba(212,175,55,0.3); color: {GOLD};
                            font-size: 0.65rem; font-weight: 600;
                        ">{ayah_num}</span>
                    </div>
                </div>
            </div>

            <!-- Translation Pane (Right) -->
            <div style="
                width: 50%; padding: 1.5rem 2rem;
                display: flex; flex-direction: column; justify-content: center;
                background: rgba(26,42,64,0.3);
                {playing_border}
            ">
                <span style="
                    color: {GOLD}; font-size: 0.65rem; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;
                ">English Translation</span>
                <p style="
                    font-family: 'Playfair Display', serif; font-size: 1rem; line-height: 1.7;
                    color: #cbd5e1; margin: 0 0 1rem 0;
                ">{ayah.get('english', '')}</p>

                <span style="
                    color: {GOLD}; font-size: 0.65rem; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;
                ">Urdu Translation</span>
                <p style="
                    font-family: 'Amiri', serif; font-size: 1rem; line-height: 1.9;
                    color: #94a3b8; direction: rtl; text-align: right; margin: 0;
                ">{ayah.get('urdu', '')}</p>
            </div>
        </div>
        """

    # Wrap in the glass panel container with arabesque background
    st.html(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
        <div style="
            border-radius: 1rem;
            background: rgba(26, 42, 64, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(148,163,184,0.1);
            overflow: hidden;
            box-shadow: 0 25px 50px rgba(0,0,0,0.25);
            position: relative;
            font-family: Inter, sans-serif;
        ">
            <!-- Arabesque overlay -->
            <div style="
                position: absolute; inset: 0; opacity: 0.03; pointer-events: none;
                background-image: url('https://www.transparenttextures.com/patterns/arabesque.png');
                background-repeat: repeat;
            "></div>

            {rows_html}
        </div>
        """
    )

    # ── Pagination Controls ───────────────────────────────────
    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    col_prev, col_info, col_next = st.columns([1, 2, 1])

    with col_prev:
        if start > 0:
            if st.button("◀ Previous", key="prev_page", use_container_width=True):
                new_idx = max(0, start - AYAHS_PER_PAGE)
                st.session_state.current_ayah_index = new_idx
                st.session_state.last_ayah = new_idx
                st.rerun()

    with col_info:
        page_num = (start // AYAHS_PER_PAGE) + 1
        total_pages = (total + AYAHS_PER_PAGE - 1) // AYAHS_PER_PAGE
        st.markdown(
            f'<p style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:0.5rem;">'
            f'Page {page_num} of {total_pages} &nbsp;·&nbsp; Ayahs {start+1}–{end} of {total}</p>',
            unsafe_allow_html=True,
        )

    with col_next:
        if end < total:
            if st.button("Next ▶", key="next_page", use_container_width=True):
                st.session_state.current_ayah_index = end
                st.session_state.last_ayah = end
                st.rerun()
