"""
Hidayah AI — Intent Router Agent
Uses Gemini 2.5 Flash-Lite for fast intent classification of user queries.
Categories: VERSE_LOOKUP, SCHOLARLY_RESEARCH, PDF_ANALYSIS
"""

from google import genai
from utils.config import MODEL_ROUTER, GEMINI_API_KEY, get_gemini_client

ROUTER_SYSTEM_PROMPT = """You are an intent classifier for an Islamic Quranic research application called Hidayah AI.

Classify the user's query into EXACTLY ONE of these categories. Return ONLY the category name, nothing else.

Categories:
- VERSE_LOOKUP: The user wants to look up, read, or hear a specific verse, surah, or juz. Examples: "Show me verse 255 of Al-Baqarah", "Read Surah Al-Fatiha", "What does ayah 183 say?"
- SCHOLARLY_RESEARCH: The user wants tafsir, fiqh rulings, historical context, scholarly opinions, or general Islamic knowledge. Examples: "Explain the fasting rules", "What do scholars say about...", "Historical context of this verse"
- PDF_ANALYSIS: The user wants to analyze, search, or ask questions about an uploaded PDF document. If a PDF is present, assume general questions (like "What is Islam?") should be answered using the PDF. Examples: "What does the PDF say about...", "Summarize the document", "Find references to fasting".

If unsure, default to SCHOLARLY_RESEARCH."""


def classify_intent(query: str, active_pdf_name: str | None = None) -> str:
    """
    Classify user intent using Gemini 2.5 Flash-Lite (fastest model).
    Returns one of: VERSE_LOOKUP, SCHOLARLY_RESEARCH, PDF_ANALYSIS
    """
    client = get_gemini_client()
    if not client:
        return "SCHOLARLY_RESEARCH"

    try:
        system_prompt = ROUTER_SYSTEM_PROMPT
        if active_pdf_name:
            system_prompt += f"\n\nCRITICAL CONTEXT: A PDF named '{active_pdf_name}' is currently uploaded. If the user asks a general question, they PROBABLY want to know the PDF's answer. Strongly bias towards PDF_ANALYSIS unless they explicitly ask for a verse or a wide-ranging web search. If the question is covered by the concept of the document, choose PDF_ANALYSIS."

        response = client.models.generate_content(
            model=MODEL_ROUTER,
            contents=query,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.1,
                max_output_tokens=50,
            ),
        )

        if not response.text:
            print(f"🚦 [ROUTER] Empty response from model. Defaulting to: SCHOLARLY_RESEARCH")
            return "SCHOLARLY_RESEARCH"

        result = response.text.strip().upper()

        # Validate the response is one of the expected categories
        valid_categories = {"VERSE_LOOKUP", "SCHOLARLY_RESEARCH", "PDF_ANALYSIS"}
        if result in valid_categories:
            print(f"🚦 [ROUTER] Classified intent as: {result}")
            return result

        # Fuzzy match (check if category is in result OR result is in category)
        for cat in valid_categories:
            if cat in result or (len(result) >= 3 and result in cat):
                print(f"🚦 [ROUTER] Fuzzy matched intent as: {cat} (from: {result})")
                return cat

        print(f"🚦 [ROUTER] Defaulting to: SCHOLARLY_RESEARCH (parsed unhandled: {result})")
        return "SCHOLARLY_RESEARCH"

    except Exception as e:
        print(f"❌ [ROUTER] Classification error: {e}")
        return "SCHOLARLY_RESEARCH"
