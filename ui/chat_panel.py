"""
Hidayah AI — Chat Panel Component
Renders the Scholar Agent right panel: chat history, input area, PDF upload, and intent routing.
"""

import streamlit as st
from datetime import datetime
from utils.config import GOLD, GEMINI_API_KEY, get_logo_base64
from agents.router import classify_intent
from agents.scholar import get_scholar_response
from rag.pdf_loader import extract_and_chunk
from rag.vector_store import build_index
from rag.query import query_pdf


def _render_chat_header():
    """Render the Scholar Agent header."""
    st.html(
        f"""
        <div style="
            display: flex; align-items: center; justify-content: space-between;
            padding: 0.75rem 1rem;
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--glass-border);
            border-radius: var(--sharp-radius) var(--sharp-radius) 0 0;
            font-family: Inter, sans-serif;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="
                    width: 2rem; height: 2rem; border-radius: 50%;
                    background-image: url('{get_logo_base64()}');
                    background-size: cover;
                    background-position: center;
                    border: 1.5px solid var(--gold);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                ">
                </div>
                <div>
                    <p style="font-size: 0.8rem; font-weight: 700; color: white; margin: 0; letter-spacing: 0.5px;">Scholar AI</p>
                    <span style="font-size: 0.55rem; color: #10b981; display: flex; align-items: center; gap: 0.25rem; font-weight: 600; text-transform: uppercase;">
                        <span style="width: 5px; height: 5px; border-radius: 50%; background: #10b981; display: inline-block; box-shadow: 0 0 5px #10b981;"></span>
                        {"Online" if GEMINI_API_KEY else "Config Required"}
                    </span>
                </div>
            </div>
        </div>
        """
    )


def _render_message(role: str, content: str, timestamp: str, intent_badge: str = ""):
    """Render a single chat message bubble."""

    if role == "assistant":
        st.html(
            f"""
            <div class="animate-reveal" style="margin-bottom: 1.25rem; font-family: Inter, sans-serif;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.4rem; margin-left: 0.25rem;">
                    <span style="font-size: 0.65rem; font-weight: 800; color: var(--gold); text-transform: uppercase; letter-spacing: 1px;">Hidayah AI</span>
                    <span style="font-size: 0.6rem; color: #64748b;">{timestamp}</span>
                    {f'<span style="font-size:0.55rem; color:#10b981; border:1px solid rgba(16,185,129,0.3); padding:0.1rem 0.5rem; border-radius: var(--sharp-radius); background:rgba(16,185,129,0.05); font-weight:700;">{intent_badge}</span>' if intent_badge else ''}
                </div>
                <div style="
                    background: rgba(30, 41, 59, 0.4);
                    border: 1px solid var(--glass-border);
                    padding: 0.85rem 1.1rem;
                    border-radius: var(--sharp-radius);
                    font-size: 0.85rem; line-height: 1.7; color: #cbd5e1;
                    max-width: 95%;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                ">
                    {content}
                </div>
            </div>
            """
        )
    else:
        st.html(
            f"""
            <div class="animate-reveal" style="margin-bottom: 1.25rem; display: flex; flex-direction: column; align-items: flex-end; font-family: Inter, sans-serif;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.4rem; margin-right: 0.25rem;">
                    <span style="font-size: 0.65rem; color: #94a3b8; font-weight: 600;">YOU</span>
                    <span style="font-size: 0.6rem; color: #64748b;">{timestamp}</span>
                </div>
                <div style="
                    background: rgba(212, 175, 55, 0.08);
                    border: 1px solid rgba(212, 175, 55, 0.2);
                    padding: 0.85rem 1.1rem;
                    border-radius: var(--sharp-radius);
                    font-size: 0.85rem; line-height: 1.7; color: #e2e8f0;
                    max-width: 90%;
                ">
                    {content}
                </div>
            </div>
            """
        )


def _process_query(query: str, ayahs: list[dict]):
    """Process a user query: classify intent → route → generate response."""

    timestamp = datetime.now().strftime("%I:%M %p")

    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": query,
        "timestamp": timestamp,
        "intent_badge": "",
    })

    # Classify intent
    active_pdf_name = st.session_state.get("uploaded_pdf_name")
    intent = classify_intent(query, active_pdf_name=active_pdf_name)

    # Map intent to human-readable badge
    badge_map = {
        "VERSE_LOOKUP": "📖 Verse Lookup",
        "SCHOLARLY_RESEARCH": "🔍 Web Research",
        "PDF_ANALYSIS": "📄 PDF Analysis",
    }
    badge = badge_map.get(intent, "")

    # Generate response based on intent
    if intent == "PDF_ANALYSIS":
        # Use RAG pipeline
        index = st.session_state.get("faiss_index")
        chunks = st.session_state.get("pdf_chunks", [])
        if index is not None and chunks:
            response = query_pdf(query, index, chunks)
        else:
            response = "⚠️ No PDF uploaded yet. Please upload a PDF using the 📎 button below."
    else:
        # Use scholar agent (handles both VERSE_LOOKUP and SCHOLARLY_RESEARCH)
        response = get_scholar_response(
            query=query,
            intent=intent,
            ayahs_context=ayahs[:10] if ayahs else None,
        )

    # Add assistant response to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime("%I:%M %p"),
        "intent_badge": badge,
    })


def render_chat_panel(ayahs: list[dict]):
    """Render the full Scholar Agent chat panel."""

    _render_chat_header()

    # ── Chat Input (placed FIRST so it's always visible) ──────
    st.markdown(
        """
        <style>
        [data-testid="stChatInput"] {
            border: 1px solid var(--gold) !important;
            border-radius: var(--sharp-radius) !important;
            background: rgba(15, 23, 42, 0.9) !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
            margin-bottom: 1.5rem !important;
        }
        [data-testid="stChatInput"] textarea {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    query = st.chat_input(
        placeholder="Ask about this verse, research, or query your PDF...",
        key="scholar_chat_input",
    )

    if query:
        _process_query(query, ayahs)
        st.rerun()

    # ── Chat History ──────────────────────────────────────────
    chat_container = st.container(height=420)

    with chat_container:
        if not st.session_state.chat_history:
            # Welcome message
            _render_message(
                "assistant",
                "Assalamu Alaykum! I'm your AI Scholar companion. Ask me about any verse, "
                "request scholarly research, or upload a PDF for analysis. How can I help you today?",
                datetime.now().strftime("%I:%M %p"),
            )
        else:
            for msg in st.session_state.chat_history:
                _render_message(
                    msg["role"],
                    msg["content"],
                    msg["timestamp"],
                    msg.get("intent_badge", ""),
                )

    # ── PDF Upload (collapsible) ──────────────────────────────
    with st.expander("📎 Research PDF Analysis", expanded=False):
        uploaded_file = st.file_uploader(
            "Upload scholarly PDF",
            type=["pdf"],
            key="pdf_uploader",
            label_visibility="visible",
        )

        if uploaded_file and uploaded_file.name != st.session_state.get("uploaded_pdf_name"):
            with st.spinner("📄 Processing PDF..."):
                chunks = extract_and_chunk(uploaded_file)
                if chunks:
                    index, embeddings = build_index(chunks)
                    if index is not None:
                        st.session_state.faiss_index = index
                        st.session_state.pdf_chunks = chunks
                        st.session_state.pdf_embeddings = embeddings
                        st.session_state.uploaded_pdf_name = uploaded_file.name
                        st.success(f"✅ PDF loaded: {uploaded_file.name} ({len(chunks)} chunks indexed)")
                    else:
                        st.error("❌ Embedding failed. Check your `GEMINI_API_KEY` in your configuration (Secrets or .env).")
                else:
                    st.error("❌ Failed to extract text from PDF.")

        if st.session_state.get("uploaded_pdf_name"):
            st.markdown(
                f'<p style="font-size:0.7rem;color:#10b981;margin:0;">📄 Active: {st.session_state.uploaded_pdf_name}</p>',
                unsafe_allow_html=True,
            )

    # ── Disclaimer ────────────────────────────────────────────
    st.html(
        '<p style="text-align:center; font-size:0.6rem; color:#64748b; margin-top:0.25rem; font-family:Inter,sans-serif;">'
        'AI can make mistakes. Verify with qualified scholars.</p>'
    )
