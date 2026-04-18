import logging
from app.llm.groq_client import llm

logger = logging.getLogger(__name__)


def fertilizer_agent(state: dict) -> dict:
    try:
        farm = state.get("farm_data", {})
        crop = farm.get("crop", "Unknown")
        pH = farm.get("pH", 0)
        fertilizer = farm.get("fertilizer", 0)
        soil = state.get("soil_analysis", "")
        docs = state.get("retrieved_docs", [])

        rag_context = "\n".join(docs) if docs else "No additional knowledge available."

        prompt = (
            f"You are an expert agronomist specializing in fertilizer management. "
            f"Provide concise fertilizer advice (2-4 sentences) for {crop} based on:\n\n"
            f"Soil pH: {pH}\n"
            f"Current Fertilizer Usage (kg/ha): {fertilizer}\n"
            f"Soil Analysis: {soil}\n\n"
            f"Retrieved Knowledge:\n{rag_context}\n\n"
            f"Recommend specific fertilizer types and application rates. "
            f"Be practical and actionable. Do not hallucinate data."
        )

        response = llm.invoke(prompt)
        state["fertilizer_advice"] = response.content.strip()

    except Exception:
        logger.exception("Error in fertilizer_agent")
        state["fertilizer_advice"] = "Unable to generate fertilizer advice."

    return state