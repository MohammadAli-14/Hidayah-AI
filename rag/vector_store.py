"""
Hidayah AI — FAISS Vector Store
Embeds text chunks using Gemini text-embedding-004 and stores in a FAISS index.
"""

import numpy as np
from google import genai
from utils.config import MODEL_EMBEDDING, GEMINI_API_KEY, get_gemini_client


def embed_texts(texts: list[str], task_type: str = "retrieval_document") -> np.ndarray | None:
    """
    Embed a list of text chunks using Gemini text-embedding-004.

    Args:
        texts: List of text strings to embed
        task_type: "retrieval_document" for indexing, "retrieval_query" for searching

    Returns:
        numpy array of shape (n, dim) or None on failure
    """
    client = get_gemini_client()
    if not client or not texts:
        return None

    try:
        embeddings = []
        # Process in batches of 100 (API limit)
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            # google-genai SDK: embed_content accepts a single string via contents
            # For batches, embed one at a time for reliability
            for text in batch:
                result = client.models.embed_content(
                    model=MODEL_EMBEDDING,
                    contents=text,
                )
                # result.embeddings is a list; single input → one element
                if result.embeddings:
                    embeddings.append(result.embeddings[0].values)

        if not embeddings:
            return None

        return np.array(embeddings, dtype=np.float32)

    except genai.errors.APIError as e:
        if e.code == 429:
            return "⚠️ 429"
        print(f"[VectorStore] Embedding API error: {e}")
        return None
    except Exception as e:
        print(f"[VectorStore] Embedding error: {e}")
        return None


def build_index(chunks: list[str]):
    """
    Build a FAISS index from text chunks.

    Args:
        chunks: List of text chunks

    Returns:
        Tuple of (faiss.Index, np.ndarray) or (None, None) on failure
    """
    if not chunks:
        return None, None

    embeddings = embed_texts(chunks, task_type="retrieval_document")
    if isinstance(embeddings, str) and "⚠️ 429" in embeddings:
        return "⚠️ 429", None
    if embeddings is None:
        return None, None

    try:
        import faiss

        # Normalize for cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        normalized = embeddings / norms

        # Build index
        dimension = normalized.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner product on normalized = cosine similarity
        index.add(normalized)

        return index, embeddings

    except ImportError:
        print("[VectorStore] FAISS not installed. Run: pip install faiss-cpu")
        return None, None
    except Exception as e:
        print(f"[VectorStore] Index build error: {e}")
        return None, None


def search_index(query: str, index, chunks: list[str], top_k: int = 5) -> list[str]:
    """
    Search the FAISS index for chunks most similar to the query.

    Args:
        query: Search query string
        index: FAISS index
        chunks: Original text chunks (aligned with index)
        top_k: Number of results to return

    Returns:
        List of most relevant text chunks
    """
    if index is None or not chunks:
        return []

    query_embedding = embed_texts([query], task_type="retrieval_query")
    if isinstance(query_embedding, str) and "⚠️ 429" in query_embedding:
        return "⚠️ 429"
    if query_embedding is None:
        return []

    try:
        import faiss

        # Normalize query embedding
        norm = np.linalg.norm(query_embedding, axis=1, keepdims=True)
        if norm[0][0] == 0:
            return []
        query_normalized = query_embedding / norm

        # Search
        scores, indices = index.search(query_normalized, min(top_k, len(chunks)))

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(chunks):
                results.append(chunks[idx])

        return results

    except Exception as e:
        print(f"[VectorStore] Search error: {e}")
        return []
