import logging

from app.rag.data.knowledge_base import KNOWLEDGE_BASE

logger = logging.getLogger(__name__)


def rag_node(state: dict) -> dict:
    """
    Simple retrieval based on keyword matching.
    Later replace with vector DB (Chroma).
    """

    try:
        query = state.get("user_query", "").lower()
        farm = state.get("farm_data", {})

        results = []
        sources = []

        # 🔹 Simple keyword-based retrieval
        for doc in KNOWLEDGE_BASE:

            content = doc["content"].lower()

            if (
                "rain" in query and "rainfall" in content
                or "soil" in query and "soil" in content
                or "fertilizer" in query and "fertilizer" in content
                or "temperature" in query and "temperature" in content
            ):
                results.append(doc["content"])
                sources.append(doc["source"])

        # 🔹 Fallback if nothing found
        if not results:
            results = [doc["content"] for doc in KNOWLEDGE_BASE[:2]]
            sources = [doc["source"] for doc in KNOWLEDGE_BASE[:2]]

        state["retrieved_docs"] = results
        state["retrieved_sources"] = sources

    except Exception:
        logger.exception("Error in rag_node")

        state["retrieved_docs"] = []
        state["retrieved_sources"] = []

    return state