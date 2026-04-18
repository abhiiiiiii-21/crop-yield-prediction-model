import logging

logger = logging.getLogger(__name__)

def output_node(state: dict) -> dict:
    """
    Formats final structured output:
    - Status
    - Advice
    - Sources
    - Disclaimer
    """

    try:
        crop = state.get("farm_data", {}).get("crop", "Unknown")
        yield_value = state.get("predicted_yield", 0)
        risk = state.get("yield_risk", "UNKNOWN")
        advice = state.get("final_advice", "")
        sources = state.get("sources", [])

        # 🔹 STATUS
        status = (
            f"Crop: {crop}\n"
            f"Predicted Yield: {round(yield_value, 2)}\n"
            f"Risk Level: {risk}"
        )

        # 🔹 DISCLAIMER
        disclaimer = (
            "This advisory is AI-generated based on available data. "
            "Please consult local agricultural experts before making decisions."
        )

        # 🔹 FINAL OUTPUT
        state["final_output"] = {
            "Status": status,
            "Advice": advice,
            "Sources": sources,
            "Disclaimer": disclaimer
        }

    except Exception:
        logger.exception("Error in output_node")

        state["final_output"] = {
            "Status": "Error generating status",
            "Advice": "No advice available",
            "Sources": [],
            "Disclaimer": "System error occurred"
        }

    return state