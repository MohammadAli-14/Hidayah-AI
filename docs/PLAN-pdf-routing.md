# Project Plan: PDF Contextual Routing

## 1. Context Check (Phase -1)
- **Problem**: When a user uploads a PDF and asks a question, the Intent Router (Gemini 2.5 Flash) evaluates the query in isolation without knowing a PDF is active. Consequently, questions like "What is Islam?" default to web research rather than querying the loaded document.
- **Goal**: Implement "Contextual AI Routing" (Option A). The router must prioritize the PDF if one is loaded, but still retain the intelligence to perform verse lookups or web searches if the user's prompt strongly suggests bypassing the document.

## 2. Task Breakdown (Phase 1)

### Step 1: Update Router Logic
- [ ] Modify `classify_intent` in `agents/router.py` to accept a new optional argument: `active_pdf_name: str | None = None`.
- [ ] Dynamically inject an instruction into the `ROUTER_SYSTEM_PROMPT` if `active_pdf_name` is provided. Example: "A PDF named '{active_pdf_name}' is currently uploaded. If the user asks a general question, strongly bias towards PDF_ANALYSIS unless they explicitly ask for a verse or web search."

### Step 2: Update UI Integration
- [ ] In `ui/chat_panel.py`, modify the `_process_query` function.
- [ ] Retrieve `st.session_state.get("uploaded_pdf_name")`.
- [ ] Pass this value into `classify_intent`.

## 3. Verification Criteria (Phase 4)
- **Test 1**: With a PDF loaded, a generic question like "What is Islam?" should route to `PDF_ANALYSIS`.
- **Test 2**: With a PDF loaded, a specific lookup like "Show me verse 255 of Al-Baqarah" should route to `VERSE_LOOKUP`.
- **Test 3**: The terminal traces should show the correct routing decisions.

---
**Agent Assignment**: `backend-specialist` (Prompt Engineering & Logic Flow).
