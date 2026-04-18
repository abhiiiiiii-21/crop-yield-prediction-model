import logging
from app.llm.groq_client import llm

logger = logging.getLogger(__name__)


def crop_agent(state: dict) -> dict:
    try:
        farm = state.get("farm_data", {})
        crop = farm.get("crop", "Unknown")
        season = farm.get("season", "Unknown")
        state_name = farm.get("state", "Unknown")
        yield_risk = state.get("yield_risk", "UNKNOWN")
        predicted_yield = state.get("predicted_yield", 0.0)

        prompt = (
            f"You are an agricultural crop specialist. Analyze the viability of growing {crop} "
            f"under the following conditions and provide a concise assessment (2-3 sentences).\n\n"
            f"Region: {state_name}\n"
            f"Season: {season}\n"
            f"Predicted Yield: {predicted_yield}\n"
            f"Yield Risk Level: {yield_risk}\n\n"
            f"Focus on: crop suitability for region/season, yield expectations, and risk implications. "
            f"Be specific and actionable. Do not hallucinate data."
        )

        response = llm.invoke(prompt)
        state["crop_analysis"] = response.content.strip()

    except Exception:
        logger.exception("Error in crop_agent")
        state["crop_analysis"] = "Unable to analyze crop."

    return state