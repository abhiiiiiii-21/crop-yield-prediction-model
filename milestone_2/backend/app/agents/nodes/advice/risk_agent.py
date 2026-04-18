import logging
from app.llm.groq_client import llm

logger = logging.getLogger(__name__)


def risk_agent(state: dict) -> dict:
    try:
        farm = state.get("farm_data", {})
        crop = farm.get("crop", "Unknown")
        yield_risk = state.get("yield_risk", "UNKNOWN")
        risk_reason = state.get("risk_reason", "")
        predicted_yield = state.get("predicted_yield", 0.0)

        prompt = (
            f"You are an agricultural risk management expert. "
            f"Provide concise risk mitigation advice (2-4 sentences) for {crop} based on:\n\n"
            f"Yield Risk Level: {yield_risk}\n"
            f"Risk Reason: {risk_reason}\n"
            f"Predicted Yield: {predicted_yield}\n\n"
            f"Recommend specific, prioritized actions to mitigate identified risks. "
            f"Be practical and actionable. Do not hallucinate data."
        )

        response = llm.invoke(prompt)
        state["risk_advice"] = response.content.strip()

    except Exception:
        logger.exception("Error in risk_agent")
        state["risk_advice"] = "Unable to generate risk mitigation advice."

    return state