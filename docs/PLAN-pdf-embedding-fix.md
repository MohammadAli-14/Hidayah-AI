# Project Plan: PDF Embedding Model Fix

## 1. Context Check (Phase -1)
- **Problem**: When a user attempts to upload a PDF for the Scholar Agent to analyze, the embedding pipeline crashes with a `404 NOT_FOUND` error. The error specifically states: `models/text-embedding-004 is not found for API version v1beta, or is not supported for embedContent`.
- **Root Cause**: The application was recently migrated to the unified `google-genai` SDK architecture. Under this specific free-tier API key and API version (`v1beta`), the model string `text-embedding-004` is no longer exposed or supported for the `embedContent` call. 
- **Investigation**: By programmatically querying the SDK's available models (`client.models.list()`), we identified that the fully supported, production-ready embedding model for this tier is actually `gemini-embedding-001`.

## 2. Task Breakdown (Phase 1)
We will address the configuration and verify the end-to-end vector pipeline.

### Step 1: Update Global Model Configuration
- [ ] Open `utils/config.py`.
- [ ] Locate the `MODEL_EMBEDDING` constant.
- [ ] Change the value from `"models/text-embedding-004"` to `"gemini-embedding-001"`. This targets the correct, supported embedding model in the Google GenAI backend.

### Step 2: Validate the Vector Pipeline
- [ ] Ensure `rag/vector_store.py` still operates seamlessly with the new model string. (We ran an isolated python script that proved `client.models.embed_content(model='gemini-embedding-001', ...)` returns success).

## 3. Verification Criteria (Phase 4)
- **Test 1**: `config.py` is compiled successfully.
- **Test 2**: Upload a PDF in the Streamlit UI. The system should successfully chunk the document, hit the `gemini-embedding-001` endpoint, build the FAISS index, and report success without crashing.

---
**Agent Assignment**: `backend-specialist` (API Integration & Vector DB operations).
