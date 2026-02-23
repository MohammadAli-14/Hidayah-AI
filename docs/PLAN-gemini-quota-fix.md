# Project Plan: Gemini Quota Fix

## 1. Context Check (Phase -1)
- **Problem**: The Scholar Agent is currently throwing a raw `429 RESOURCE_EXHAUSTED` error directly into the UI. The root cause is that `gemini-2.5-pro` has strict/zero quota limits for the user's current Google GenAI free tier.
- **Constraints**: We must ensure the app remains fully functional on a free-tier API key while handling backend errors gracefully without breaking the frontend UX.

## 2. Task Breakdown (Phase 1)
To fix this robustly, we need to address both the root cause (the model tier) and the symptom (raw unhandled exceptions in the UX).

### Step 1: Model Configuration Updates
- [ ] In `utils/config.py`, change `MODEL_SCHOLAR` from `"gemini-2.5-pro"` to `"gemini-2.5-flash"`. The Flash model has vastly higher free-tier limits (15 RPM / 1M TPM) and is exceptionally fast for RAG and scholarly queries.
- [ ] In `utils/config.py`, change `MODEL_ROUTER` from `"gemini-2.5-flash-lite"` to `"gemini-2.5-flash"` for better consistency and reliability.

### Step 2: Graceful Exception Handling
- [ ] In `agents/scholar.py` (or wherever the `google-genai` call is made), wrap the `client.models.generate_content` call in a `try...except` block.
- [ ] Catch `google.genai.errors.APIError` (or generic Exception) specifically looking for `429`.
- [ ] Return a user-friendly, formatted error message instead of raw JSON. Example: `"⚠️ **Scholar Agent Error**: The API quota has been exceeded. Please try again in a few seconds or check your API key settings."`

## 3. Verification Criteria (Phase 4)
- **Test 1**: Verify `config.py` is updated to standard Flash models.
- **Test 2**: Temporarily trigger a simulated 429 error to ensure the UI catches it cleanly.
- **Test 3**: The chat panel should display the graceful warning instead of a raw JSON blob.

---
**Agent Assignment**: `frontend-specialist` (Graceful UI), `backend-specialist` (Error Handling & Config changes).
