import os
import sys
import logging
import joblib
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# ─── Resolve path to milestone_1 artifacts ───
# ml_node.py → nodes → agents → app → backend → milestone_2 → project_root
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, "../../../../../"))
_artifacts_dir = os.path.join(_project_root, "milestone_1", "artifacts")

# ─── Load artifacts once at module level ───
try:
    _model = joblib.load(os.path.join(_artifacts_dir, "best_model.pkl"))
    _scaler = joblib.load(os.path.join(_artifacts_dir, "scaler.pkl"))
    _expected_columns = joblib.load(os.path.join(_artifacts_dir, "feature_columns.pkl"))
    logger.info(f"[ML Node] Loaded artifacts from {_artifacts_dir}")
    logger.info(f"[ML Node] Expected columns ({len(_expected_columns)}): {_expected_columns[:8]}...")
except Exception:
    logger.exception(f"[ML Node] FAILED to load artifacts from {_artifacts_dir}")
    _model = None
    _scaler = None
    _expected_columns = None


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def ml_node(state: dict) -> dict:
    """
    ML prediction node for LangGraph pipeline.

    Bypasses predict_yield() to fix two critical preprocessing bugs:
      1. pd.get_dummies(drop_first=True) on a single-row DataFrame drops ALL
         categorical features (every one-hot column becomes 0).
      2. Input field names (Rainfall, Temperature, pH) don't match the training
         column names (Annual_Rainfall, Area, Crop_Year, Pesticide).

    Instead, we manually construct the feature vector to match the exact
    columns the model was trained on.
    """
    try:
        if _model is None or _scaler is None or _expected_columns is None:
            logger.error("[ML Node] Artifacts not loaded — returning 0.0")
            state["predicted_yield"] = 0.0
            return state

        farm_data = state.get("farm_data", {})

        # ─── Extract & normalize inputs ───
        crop = str(farm_data.get("crop", "Unknown")).strip().title()
        season = str(farm_data.get("season", "Rabi")).strip().title()
        state_name = str(farm_data.get("state", "Punjab")).strip().title()

        rainfall = safe_float(farm_data.get("rainfall"))
        temperature = safe_float(farm_data.get("temperature"))
        ph = safe_float(farm_data.get("pH"))
        fertilizer = safe_float(farm_data.get("fertilizer"))

        logger.info(
            f"[ML Node] Input → Crop={crop}, Season={season}, State={state_name}, "
            f"Rainfall={rainfall}, Temp={temperature}, pH={ph}, Fertilizer={fertilizer}"
        )

        # ─── Build feature vector (all zeros initially) ───
        feature_dict = {col: 0.0 for col in _expected_columns}

        # ─── Map numeric features ───
        # Training data columns: Crop_Year, Area, Annual_Rainfall, Fertilizer, Pesticide
        # We map the user-provided fields to the closest training columns:
        #   rainfall   → Annual_Rainfall
        #   fertilizer → Fertilizer
        # Fields without a training equivalent (Temperature, pH) are not in the
        # model's feature set, so they cannot influence predictions. We still
        # set Crop_Year and Area to reasonable defaults.
        numeric_mapping = {
            "Annual_Rainfall": rainfall,
            "Fertilizer": fertilizer,
            "Crop_Year": 2020.0,      # reasonable default
            "Area": 1000.0,           # reasonable default (hectares)
            "Pesticide": 0.0,         # no pesticide data provided
        }

        for col, val in numeric_mapping.items():
            if col in feature_dict:
                feature_dict[col] = val
                logger.info(f"[ML Node]   Numeric: {col} = {val}")

        # ─── Set one-hot encoded categorical features ───
        # Training used pd.get_dummies(drop_first=True), so the first
        # alphabetical category per column is the reference (absent) category.
        # We only need to set the matching column to 1.0 if it exists.
        #
        # Some training columns have trailing whitespace (e.g. "Crop_Coconut "),
        # so we build a fuzzy lookup: stripped_name → actual_name.
        _col_lookup = {col.strip(): col for col in _expected_columns}

        for prefix, value in [("Crop", crop), ("Season", season), ("State", state_name)]:
            col_name = f"{prefix}_{value}"
            # Try exact match first, then stripped match
            actual_col = None
            if col_name in feature_dict:
                actual_col = col_name
            elif col_name.strip() in _col_lookup:
                actual_col = _col_lookup[col_name.strip()]

            if actual_col:
                feature_dict[actual_col] = 1.0
                logger.info(f"[ML Node]   Category: {actual_col!r} = 1")
            else:
                # Could be the dropped reference category, or an unknown value
                logger.warning(
                    f"[ML Node]   Category: '{col_name}' NOT in expected columns "
                    f"(reference category or unseen value)"
                )

        # ─── Create DataFrame in exact column order ───
        input_df = pd.DataFrame([feature_dict])[_expected_columns]

        non_zero = [c for c in _expected_columns if input_df[c].iloc[0] != 0]
        logger.info(f"[ML Node] Non-zero features ({len(non_zero)}): {non_zero}")

        # ─── Scale & predict ───
        X_scaled = _scaler.transform(input_df)
        prediction = _model.predict(X_scaled)[0]

        logger.info(f"[ML Node] ✅ Predicted yield: {prediction}")
        state["predicted_yield"] = float(prediction)

    except Exception:
        logger.exception("[ML Node] Error in ml_node")
        state["predicted_yield"] = 0.0

    return state