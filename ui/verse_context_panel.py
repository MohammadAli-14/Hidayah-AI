"""
Hidayah AI — Verse Context Panel
Renders Tafseer and related Hadith for the currently selected ayah.
"""

import streamlit as st
from utils.config import TAFSEER_LANGUAGE_LABELS, TAFSEER_SOURCE_TARGET_COUNT
from utils.tafsir_api import fetch_multisource_tafseer_for_ayah
from utils.hadith_api import fetch_related_hadith


def _looks_like_raw_api_link(url: str) -> bool:
    if not url:
        return False
    lowered = url.lower()
    return (
        lowered.endswith(".json")
        or "api." in lowered
        or "/v1/" in lowered
        or "/api/" in lowered
    )


def render_verse_context_panel(current_ayah: dict):
    """Render contextual Tafseer + Hadith below the Quran view."""
    if not current_ayah:
        return

    surah_name = current_ayah.get("surah_name", "")
    surah_number = current_ayah.get("surah_number", 0)
    ayah_number = current_ayah.get("number_in_surah", 0)
    ayah_english = current_ayah.get("english", "")

    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

    st.html(
        f"""
        <div style="
            border: 1px solid rgba(148,163,184,0.14);
            border-radius: 2px;
            background: rgba(26,42,64,0.55);
            backdrop-filter: blur(10px);
            padding: 0.75rem 0.85rem;
            font-family: Inter, sans-serif;
        ">
            <p style="margin:0; color:#94a3b8; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.08em; font-weight:700;">Verse Context</p>
            <p style="margin:0.3rem 0 0 0; color:#e2e8f0; font-size:0.82rem; font-weight:600;">{surah_name} ({surah_number}:{ayah_number})</p>
        </div>
        """
    )

    tab_tafsir, tab_hadith = st.tabs(["Tafseer", "Related Hadith"])

    with tab_tafsir:
        selected_language = st.selectbox(
            "Tafseer Language",
            list(TAFSEER_LANGUAGE_LABELS.keys()),
            index=list(TAFSEER_LANGUAGE_LABELS.keys()).index(st.session_state.get("tafsir_language", "en"))
            if st.session_state.get("tafsir_language", "en") in TAFSEER_LANGUAGE_LABELS
            else 0,
            key=f"tafsir_language_{surah_number}_{ayah_number}",
            format_func=lambda key: TAFSEER_LANGUAGE_LABELS.get(key, key.upper()),
        )
        st.session_state.tafsir_language = selected_language

        tafsir_sources = fetch_multisource_tafseer_for_ayah(
            surah_number=surah_number,
            ayah_number=ayah_number,
            language=selected_language,
            max_sources=TAFSEER_SOURCE_TARGET_COUNT,
        )

        if tafsir_sources:
            for tafsir in tafsir_sources:
                st.markdown(
                    f"""
                    <div style="
                        border:1px solid rgba(212,175,55,0.24);
                        background: rgba(212,175,55,0.05);
                        border-radius:2px;
                        padding:0.8rem 0.9rem;
                        margin-top:0.35rem;
                    ">
                        <p style="margin:0; font-size:0.66rem; color:#D4AF37; text-transform:uppercase; letter-spacing:0.08em; font-weight:700;">{tafsir['source_name']}</p>
                        <p style="margin:0.45rem 0 0 0; color:#e2e8f0; line-height:1.75; font-size:0.9rem;">{tafsir['excerpt']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.caption(
                    f"Source: {tafsir['source_name']} • Ref {tafsir['reference']} • "
                    f"Type {(tafsir.get('metadata', {}).get('source_type', 'tafsir') or 'tafsir').upper()} • "
                    f"Lang {tafsir.get('language', '').upper()} • "
                    f"Fallback {'Yes' if tafsir.get('metadata', {}).get('fallback_language_used') else 'No'} • "
                    f"Canonical {tafsir.get('canonical_status', 'unverified')}"
                )
                metadata = tafsir.get("metadata", {})
                human_url = metadata.get("canonical_url_human", "")
                api_url = metadata.get("api_url") or tafsir.get("canonical_url") or ""

                if human_url and not _looks_like_raw_api_link(human_url):
                    st.markdown(f"[Open reference page]({human_url})")

                if api_url:
                    st.markdown(f"[Open raw source (JSON)]({api_url})")
        else:
            st.info("No explanatory sources are available right now for this language.")

    with tab_hadith:
        hadith_items = fetch_related_hadith(
            ayah_text_english=ayah_english,
            surah_name=surah_name,
            ayah_number=ayah_number,
        )

        if hadith_items:
            for item in hadith_items:
                st.markdown(
                    f"""
                    <div style="
                        border:1px solid rgba(148,163,184,0.18);
                        background: rgba(15,23,42,0.55);
                        border-radius:2px;
                        padding:0.75rem 0.85rem;
                        margin-bottom:0.6rem;
                    ">
                        <p style="margin:0; font-size:0.66rem; color:#10B981; text-transform:uppercase; letter-spacing:0.08em; font-weight:700;">{item['source_name']}</p>
                        <p style="margin:0.4rem 0 0 0; color:#e2e8f0; line-height:1.65; font-size:0.85rem;">{item['excerpt']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.caption(
                    f"Source: {item['source_name']} • Ref {item['reference']} • "
                    f"Lang {item.get('language', '').upper()} • "
                    f"Canonical {item.get('canonical_status', 'unverified')}"
                )
                if item.get("url"):
                    st.markdown(f"[Open reference]({item['url']})")
        else:
            st.info("No related Hadith references found right now. Try another ayah or source.")
