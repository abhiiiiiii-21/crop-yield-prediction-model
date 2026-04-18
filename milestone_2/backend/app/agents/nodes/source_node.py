import logging

logger = logging.getLogger(__name__)


def source_node(state: dict) -> dict:
    """
    Extracts and cleans sources from RAG results.
    """

    try:
        sources = state.get("retrieved_sources", [])

        # Remove duplicates while preserving order
        unique_sources = list(dict.fromkeys(sources))

        state["sources"] = unique_sources

    except Exception:
        logger.exception("Error in source_node")
        state["sources"] = []

    return state