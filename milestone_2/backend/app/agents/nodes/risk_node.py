import logging

logger = logging.getLogger(__name__)


def risk_node(state: dict) -> dict:
    """
    Converts predicted yield into risk level using improved thresholds.
    Adds explainability via risk_reason.
    """

    try:
        y = state.get("predicted_yield", 0)

        # Safety fallback
        if y is None:
            y = 0

        # 🔥 Improved thresholds (based on typical ML output range ~1–3)
        if y < 1.5:
            risk = "HIGH"
            reason = "Predicted yield is very low, indicating poor growing conditions."

        elif y < 2.5:
            risk = "MEDIUM"
            reason = "Predicted yield is moderate but can be improved with better practices."

        else:
            risk = "LOW"
            reason = "Predicted yield is good under current conditions."

        # Update state
        state["yield_risk"] = risk
        state["risk_reason"] = reason

    except Exception:
        logger.exception("Error in risk_node")

        state["yield_risk"] = "UNKNOWN"
        state["risk_reason"] = "Unable to determine risk due to system error."

    return state
