import logging
from app.llm.groq_client import llm

logger = logging.getLogger(__name__)


def weather_agent(state: dict) -> dict:
    try:
        farm = state.get("farm_data", {})
        rainfall = farm.get("rainfall", 0)
        temperature = farm.get("temperature", 0)
        crop = farm.get("crop", "Unknown")
        season = farm.get("season", "Unknown")

        prompt = (
            f"You are an agricultural weather analyst. Analyze the following weather conditions "
            f"for {crop} cultivation during the {season} season and provide a concise assessment (2-3 sentences).\n\n"
            f"Rainfall (mm): {rainfall}\n"
            f"Temperature (°C): {temperature}\n\n"
            f"Focus on: impact on crop growth, risks from extreme conditions, and seasonal suitability. "
            f"Be specific and actionable. Do not hallucinate data."
        )

        response = llm.invoke(prompt)
        state["weather_analysis"] = response.content.strip()

    except Exception:
        logger.exception("Error in weather_agent")
        state["weather_analysis"] = "Unable to analyze weather."

    return state