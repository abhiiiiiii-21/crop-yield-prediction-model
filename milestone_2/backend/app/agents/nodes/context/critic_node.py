import logging

logger = logging.getLogger(__name__)


def critic_node(state: dict) -> int:
    """
    Evaluates quality of multi-agent analysis.
    Returns score (0-10).
    """

    try:
        soil = state.get("soil_analysis", "")
        weather = state.get("weather_analysis", "")
        crop = state.get("crop_analysis", "")

        score = 0

        # Basic scoring logic
        if soil:
            score += 3
        if weather:
            score += 3
        if crop:
            score += 3

        # Bonus if analysis is meaningful
        if "optimal" in soil.lower():
            score += 1

        state["analysis_score"] = score

        return score

    except Exception:
        logger.exception("Error in critic_node")
        return 0