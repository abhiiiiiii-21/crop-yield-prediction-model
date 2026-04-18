import logging
from app.llm.groq_client import llm

logger = logging.getLogger(__name__)


def irrigation_agent(state: dict) -> dict:
    try:
        farm = state.get("farm_data", {})
        crop = farm.get("crop", "Unknown")
        rainfall = farm.get("rainfall", 0)
        temperature = farm.get("temperature", 0)
        weather = state.get("weather_analysis", "")

        prompt = (
            f"You are an irrigation and water management specialist. "
            f"Provide concise irrigation advice (2-4 sentences) for {crop} based on:\n\n"
            f"Rainfall (mm): {rainfall}\n"
            f"Temperature (°C): {temperature}\n"
            f"Weather Analysis: {weather}\n\n"
            f"Recommend specific irrigation methods and schedules. "
            f"Be practical and actionable. Do not hallucinate data."
        )

        response = llm.invoke(prompt)
        state["irrigation_advice"] = response.content.strip()

    except Exception:
        logger.exception("Error in irrigation_agent")
        state["irrigation_advice"] = "Unable to generate irrigation advice."

    return state