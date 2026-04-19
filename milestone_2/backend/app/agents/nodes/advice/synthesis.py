import logging
from app.llm.groq_client import llm

logger = logging.getLogger(__name__)


def synthesis_node(state: dict) -> dict:
    """
    Combines all advice into a final structured recommendation using LLM.
    """

    try:
        plan = state.get("plan", "")
        fert = state.get("fertilizer_advice", "")
        irr = state.get("irrigation_advice", "")
        risk = state.get("risk_advice", "")
        farm = state.get("farm_data", {})
        crop = farm.get("crop", "Unknown")
        predicted_yield = state.get("predicted_yield", 0.0)

        prompt = (
            f"You are an agricultural advisor helping a farmer growing {crop} "
            f"with predicted yield {round(predicted_yield, 2)}.\n\n"

            f"Based on the following context:\n"
            f"{plan}\n{fert}\n{irr}\n{risk}\n\n"

            f"Generate final recommendations with STRICT rules:\n"
            f"- Exactly 5 bullet points\n"
            f"- Each point must be short (max 8-10 words)\n"
            f"- Start each line ONLY with '✔'\n"
            f"- No numbers, no '-', no '*'\n"
            f"- No long explanations\n"
            f"- Avoid exact numeric values unless necessary\n"
            f"- Keep advice practical and safe\n\n"

            f"Output only bullet points."
        )

        response = llm.invoke(prompt)
        state["final_advice"] = response.content.strip()

    except Exception:
        logger.exception("Error in synthesis_node")
        state["final_advice"] = "Unable to generate final advice."

    return state