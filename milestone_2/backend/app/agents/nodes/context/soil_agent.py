import logging
from app.llm.groq_client import llm

logger = logging.getLogger(__name__)


def soil_agent(state: dict) -> dict:
    try:
        farm = state.get("farm_data", {})
        pH = farm.get("pH", 0)
        fertilizer = farm.get("fertilizer", 0)
        soil_type = farm.get("soil_type", "Unknown")
        crop = farm.get("crop", "Unknown")

        prompt = (
            f"You are an agricultural soil expert. Analyze the following soil conditions "
            f"for {crop} cultivation and provide a concise assessment (2-3 sentences).\n\n"
            f"Soil Type: {soil_type}\n"
            f"Soil pH: {pH}\n"
            f"Fertilizer Usage (kg/ha): {fertilizer}\n\n"
            f"Focus on: soil suitability, pH implications, and fertilizer adequacy. "
            f"Be specific and actionable. Do not hallucinate data."
        )

        response = llm.invoke(prompt)
        state["soil_analysis"] = response.content.strip()

    except Exception:
        logger.exception("Error in soil_agent")
        state["soil_analysis"] = "Unable to analyze soil."

    return state