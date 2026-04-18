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
            f"You are a senior agricultural consultant preparing a final advisory report for a farmer "
            f"growing {crop} with a predicted yield of {predicted_yield}.\n\n"
            f"Synthesize the following into a clear, unified advisory (4-6 sentences):\n\n"
            f"Farming Plan:\n{plan}\n\n"
            f"Fertilizer Advice:\n{fert}\n\n"
            f"Irrigation Advice:\n{irr}\n\n"
            f"Risk Management:\n{risk}\n\n"
            f"Combine these into a coherent, actionable summary. Avoid repeating the same point. "
            f"Prioritize the most impactful recommendations. Do not hallucinate data."
        )

        response = llm.invoke(prompt)
        state["final_advice"] = response.content.strip()

    except Exception:
        logger.exception("Error in synthesis_node")
        state["final_advice"] = "Unable to generate final advice."

    return state