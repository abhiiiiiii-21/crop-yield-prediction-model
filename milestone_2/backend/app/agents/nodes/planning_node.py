import logging
from app.llm.groq_client import llm

logger = logging.getLogger(__name__)


def planning_node(state: dict) -> dict:
    """
    Generates a structured farming plan using LLM reasoning over
    multi-agent analysis and RAG-retrieved knowledge.
    """

    try:
        soil = state.get("soil_analysis", "")
        weather = state.get("weather_analysis", "")
        crop = state.get("crop_analysis", "")
        risk = state.get("yield_risk", "UNKNOWN")
        docs = state.get("retrieved_docs", [])
        farm = state.get("farm_data", {})
        crop_name = farm.get("crop", "Unknown")

        rag_context = "\n".join(docs) if docs else "No additional knowledge available."

        prompt = (
            f"You are a senior agricultural planner. Create a concise, actionable farming plan "
            f"for {crop_name} based on the following analysis.\n\n"
            f"Soil Analysis: {soil}\n"
            f"Weather Analysis: {weather}\n"
            f"Crop Analysis: {crop}\n"
            f"Yield Risk: {risk}\n\n"
            f"Retrieved Knowledge:\n{rag_context}\n\n"
            f"Provide a numbered plan with 3-5 specific steps. Each step should be one sentence. "
            f"Prioritize actions by urgency. Do not hallucinate data."
        )

        response = llm.invoke(prompt)
        state["plan"] = response.content.strip()

    except Exception:
        logger.exception("Error in planning_node")
        state["plan"] = "Unable to generate plan."

    return state