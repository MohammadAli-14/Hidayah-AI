"""
Hidayah AI — Scholar Agent
Uses Gemini 2.5 Pro for deep scholarly reasoning, tafsir, and research synthesis.
Routes to appropriate data source based on classified intent.
"""

from google import genai
from utils.config import MODEL_SCHOLAR, GEMINI_API_KEY, get_gemini_client
from agents.web_search import search_web

SCHOLAR_SYSTEM_PROMPT = """You are Hidayah AI, an Islamic scholarly research assistant. You are knowledgeable, respectful, and precise.

Guidelines:
1. Begin responses with "Assalamu Alaykum" when appropriate.
2. Cite sources clearly: Quran verses (Surah:Ayah), Hadith collections, and scholarly names.
3. When discussing fiqh, mention the relevant madhab perspectives where applicable.
4. Use a warm, scholarly tone — like a knowledgeable teacher.
5. If uncertain, say so clearly. Never fabricate scholarly opinions.
6. End with a reminder: "Please verify with qualified scholars for fiqh rulings."
7. Support both English and Urdu — respond in the language the user asks in.
8. When referencing Quranic text, include the Arabic if relevant.

You serve as a bridge between classical Islamic scholarship and modern seekers of knowledge."""


def get_scholar_response(
    query: str,
    intent: str,
    ayahs_context: list[dict] | None = None,
    pdf_context: str | None = None,
) -> str:
    """
    Generate a scholarly response using Gemini 2.5 Pro.

    Args:
        query: User's question
        intent: Classified intent (VERSE_LOOKUP, SCHOLARLY_RESEARCH, PDF_ANALYSIS)
        ayahs_context: Current ayahs being viewed (for verse context)
        pdf_context: Retrieved PDF chunks (for RAG answers)

    Returns:
        Formatted response string
    """
    client = get_gemini_client()
    if not client:
        return "⚠️ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file."

    try:
        # Build context based on intent
        context_parts = []

        if intent == "VERSE_LOOKUP" and ayahs_context:
            # Provide current verse context
            verses_text = "\n".join(
                f"[{a['surah_name']} {a['number_in_surah']}] Arabic: {a['arabic']}\n"
                f"English: {a['english']}\nUrdu: {a['urdu']}"
                for a in ayahs_context[:10]  # Limit context size
            )
            context_parts.append(f"Currently viewing these Quranic verses:\n{verses_text}")

        elif intent == "SCHOLARLY_RESEARCH":
            # Fetch web results for additional context
            web_results = search_web(f"Islamic scholarly {query}")
            if web_results:
                web_text = "\n\n".join(
                    f"Source: {r['title']}\nURL: {r['url']}\n{r['content']}"
                    for r in web_results[:3]
                )
                context_parts.append(f"Web research results:\n{web_text}")

        elif intent == "PDF_ANALYSIS" and pdf_context:
            context_parts.append(f"Relevant excerpts from the uploaded PDF:\n{pdf_context}")

        # Assemble the full prompt
        full_prompt = query
        if context_parts:
            context_str = "\n\n---\n\n".join(context_parts)
            full_prompt = f"Context:\n{context_str}\n\n---\n\nUser Question: {query}"

        response = client.models.generate_content(
            model=MODEL_SCHOLAR,
            contents=full_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=SCHOLAR_SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=2048,
            ),
        )

        return response.text

    except genai.errors.APIError as e:
        if e.code == 429:
            return "⚠️ **Scholar Agent is busy**. The Google Gemini API free-tier quota has been temporarily exhausted. Please wait a few moments and try again."
        return f"⚠️ **API Error:** {str(e.message) if hasattr(e, 'message') else str(e)}"
    except Exception as e:
        return f"⚠️ **Scholar Agent error:** An unexpected error occurred. Please try again."
