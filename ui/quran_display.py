"""
Hidayah AI — Quran Display Component
Renders the dual-pane view: Arabic text (RTL) on the left, English + Urdu translations on the right.
"""

import streamlit as st
from utils.config import GOLD, MIDNIGHT_BLUE
from ui.verse_context_panel import render_verse_context_panel

AYAHS_PER_PAGE = 5


def render_quran_view(ayahs: list[dict], current_index: int = 0):
    """
    Render the dual-pane Quran display with pagination.
    Shows AYAHS_PER_PAGE ayahs at a time starting from current_index.
    """

    if not ayahs:
        last = st.session_state.get("last_ayah", 0)
        resume_html = ""
        if last > 0:
            # We use a Streamlit button for actual interaction, so we close the HTML div,
            # render the button, and then open another if needed.
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.html(
                    """
                    <div style="text-align: center; margin-top: 2rem;">
                        <p style="font-size: 2rem; margin-bottom: 0.5rem;">📖</p>
                        <p style="color: #94a3b8; font-size: 1.1rem; font-family: Inter, sans-serif;">Select a Juz from the sidebar to begin reading</p>
                        <div style="margin: 1.5rem 0; font-size: 0.85rem; color: #cbd5e1;">— OR —</div>
                    </div>
                    """
                )
                if st.button("► Resume Your Reading", key="main_resume_btn", use_container_width=True):
                    st.session_state.current_ayah_index = last
                    st.session_state.is_playing = True
                    st.rerun()
            return

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
    st.session_state.visible_ayah_window = page_ayahs

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
        <div class="verse-row" style="
            display: grid;
            grid-template-columns: 1fr 1fr;
            border-bottom: 1px solid rgba(148,163,184,0.08);
            position: relative;
            transition: all 0.4s ease;
        ">
            <!-- Arabic Pane (Left) -->
            <div class="arabic-pane" style="
                padding: 2rem;
                display: flex; align-items: center; justify-content: center;
                border-right: 1px solid rgba(148,163,184,0.08);
                background: rgba(255,255,255,0.01);
                {playing_border_rtl}
            ">
                <div style="text-align: center; width: 100%;">
                    <p style="
                        font-family: 'Amiri', serif; font-size: 1.85rem; line-height: 2.3;
                        color: #f8fafc; direction: rtl; text-align: center;
                        margin: 0; text-shadow: 0 4px 20px rgba(0,0,0,0.3);
                    ">{ayah.get('arabic', '')}</p>
                    <div style="display:flex; align-items:center; justify-content:center; gap:0.5rem; margin-top:1rem;">
                        <span style="
                            display:inline-flex; align-items:center; justify-content:center;
                            min-width: 1.8rem; height: 1.8rem;
                            border: 1px solid var(--gold); color: var(--gold);
                            font-size: 0.7rem; font-weight: 700;
                            border-radius: var(--sharp-radius);
                            background: rgba(212,175,55,0.05);
                        ">{ayah_num}</span>
                    </div>
                </div>
            </div>

            <!-- Translation Pane (Right) -->
            <div class="translation-pane" style="
                padding: 2rem;
                display: flex; flex-direction: column; justify-content: center;
                background: rgba(26,42,64,0.2);
                {playing_border}
            ">
                <div style="margin-bottom: 1.5rem;">
                    <span style="
                        color: var(--gold); font-size: 0.6rem; font-weight: 700;
                        text-transform: uppercase; letter-spacing: 0.2em; opacity: 0.7;
                    ">English</span>
                    <p style="
                        font-family: 'Playfair Display', serif; font-size: 1.05rem; line-height: 1.8;
                        color: #cbd5e1; margin: 0.25rem 0 0 0;
                    ">{ayah.get('english', '')}</p>
                </div>

                <div>
                    <span style="
                        color: var(--gold); font-size: 0.6rem; font-weight: 700;
                        text-transform: uppercase; letter-spacing: 0.2em; opacity: 0.7;
                    ">Urdu</span>
                    <p style="
                        font-family: 'Amiri', serif; font-size: 1.15rem; line-height: 2;
                        color: #94a3b8; direction: rtl; text-align: right; margin: 0.25rem 0 0 0;
                    ">{ayah.get('urdu', '')}</p>
                </div>
            </div>
        </div>
        """

    # Wrap in the glass panel container with arabesque background
    st.html(
        f"""
        <style>
            @media (max-width: 992px) {{
                .verse-row {{
                    grid-template-columns: 1fr !important;
                }}
                .arabic-pane {{
                    border-right: none !important;
                    border-bottom: 1px solid rgba(148,163,184,0.08) !important;
                }}
            }}
        </style>
        <div style="
            border-radius: var(--sharp-radius);
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

    # ── Tafseer + Hadith Context Panel ───────────────────────
    active_idx = min(st.session_state.get("current_ayah_index", 0), len(ayahs) - 1)
    render_verse_context_panel(ayahs[active_idx])
