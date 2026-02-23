"""
Hidayah AI — RAG Query Engine
Retrieves relevant PDF chunks and generates answers using Gemini 2.5 Pro.
"""

from google import genai
from utils.config import MODEL_SCHOLAR, GEMINI_API_KEY, get_gemini_client
from rag.vector_store import search_index


RAG_SYSTEM_PROMPT = """You are Hidayah AI, an Islamic research assistant analyzing a user-uploaded PDF document.

Guidelines:
1. Answer ONLY based on the provided PDF context. Do not hallucinate information.
2. If the context doesn't contain relevant information, say so clearly.
3. Quote directly from the PDF when possible, using quotation marks.
4. Maintain a scholarly, respectful tone.
5. If the PDF discusses Islamic topics, apply proper Islamic etiquette in your response.
6. Cite page references or section headers from the context when available."""


def query_pdf(
    question: str,
    index,
    chunks: list[str],
    top_k: int = 5,
) -> str:
    """
    Answer a question using RAG: retrieve relevant chunks then generate an answer.

    Args:
        question: User's question about the PDF
        index: FAISS index
        chunks: Original text chunks
        top_k: Number of chunks to retrieve

    Returns:
        Generated answer string
    """
    client = get_gemini_client()
    if not client:
        return "⚠️ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file."

    if index is None or not chunks:
        return "⚠️ No PDF has been uploaded yet. Please upload a PDF using the attachment button."

    # Retrieve relevant chunks
    relevant_chunks = search_index(question, index, chunks, top_k)

    if isinstance(relevant_chunks, str) and "⚠️ 429" in relevant_chunks:
        return "⚠️ **Scholar Agent is currently resting.** Hidayah AI is receiving a high volume of requests. Please wait a moment and try again."

    if not relevant_chunks:
        return "I couldn't find relevant information in the uploaded PDF for your question. Please try rephrasing."

    # Build context from retrieved chunks
    context = "\n\n---\n\n".join(
        f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(relevant_chunks)
    )

    # Generate answer with Gemini Pro
    try:
        prompt = f"""Based on the following excerpts from the uploaded PDF document, answer the user's question.

PDF Context:
{context}

---

User Question: {question}

Provide a thorough, well-structured answer based strictly on the PDF content above."""

        response = client.models.generate_content(
            model=MODEL_SCHOLAR,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=RAG_SYSTEM_PROMPT,
                temperature=0.4,
                max_output_tokens=2048,
            ),
        )

        return response.text

    except genai.errors.APIError as e:
        if e.code == 429:
            return "⚠️ **Scholar Agent is currently resting.** Hidayah AI is receiving a high volume of requests. Please wait a moment and try again."
        return f"⚠️ **RAG API Error:** {str(e.message) if hasattr(e, 'message') else str(e)}"
    except Exception as e:
        return f"⚠️ **RAG query error:** An unexpected error occurred. Please try again."
