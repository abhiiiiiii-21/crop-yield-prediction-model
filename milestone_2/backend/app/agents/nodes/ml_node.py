import os
import sys
import logging
import pandas as pd

logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../../../"))

if project_root not in sys.path:
    sys.path.append(project_root)

from milestone_1.src.model_pipeline import predict_yield



def safe_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def ml_node(state: dict) -> dict:
    try:
        farm_data = state.get("farm_data", {})

        season = farm_data.get("season") or "Rabi"
        state_value = farm_data.get("state") or "Punjab"

        input_data = {
            "Crop": farm_data.get("crop", "Unknown"),
            "Season": season,
            "State": state_value,
            "Rainfall": safe_float(farm_data.get("rainfall")),
            "Temperature": safe_float(farm_data.get("temperature")),
            "pH": safe_float(farm_data.get("pH")),
            "Fertilizer": safe_float(farm_data.get("fertilizer")),
        }

        input_df = pd.DataFrame([input_data])

        result_df, _ = predict_yield(input_df)
        predicted_value = result_df["Predicted_Yield"].iloc[0]

        state["predicted_yield"] = float(predicted_value)

    except Exception:
        logger.exception("Error in ml_node")
        state["predicted_yield"] = 0.0

    return state