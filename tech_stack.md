# Hidayah AI Technical Specification

## Core Frameworks
- **Frontend:** Streamlit (Python)
- **Styling:** Tailwind CSS injected via `st.markdown(unsafe_allow_html=True)`
- **LLM:** Google Gemini 1.5 Flash (via `google-generativeai`)

## Key Skills & Logic
1. **Agent Router Logic:** - Function: `classify_intent(query)`
   - Categories: [VERSE_LOOKUP, SCHOLARLY_RESEARCH, PDF_ANALYSIS]
   
2. **Web Search Tool:** - API: Tavily (use `tavily-python`)
   - Purpose: Fetching historical context and modern scholarly fatwas.

3. **Audio Engine:**
   - API: AlQuran.cloud (Endpoint: `https://api.alquran.cloud/v1/juz/{juz}/ar.alafasy`)
   - Translation Sync: Fetch `ur.jalandhry` for Urdu and `en.asad` for English.

4. **RAG (Document Analysis):**
   - Libraries: `PyPDF2` for parsing, `FAISS` for vector storage.
   - Flow: Extract PDF text -> Create chunks -> Embed using Gemini -> Query when intent is PDF_ANALYSIS.

5. **State Management:**
   - Use `st.session_state` to track current Juz, playback time, and chat history.