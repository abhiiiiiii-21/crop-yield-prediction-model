import os
import logging
import traceback

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
    logger.info(f"[ML Node] ✅ Loaded artifacts from {_artifacts_dir}")
    logger.info(f"[ML Node] Expected columns ({len(_expected_columns)}): {_expected_columns[:8]}...")
except Exception:
    logger.exception(f"[ML Node] ❌ FAILED to load artifacts from {_artifacts_dir}")
    _model = None
    _scaler = None
    _expected_columns = None


# ═══════════════════════════════════════════════════════════════════════════════
#  CATEGORY LOOKUP TABLES  (built once from the training columns)
# ═══════════════════════════════════════════════════════════════════════════════

def _build_known_categories(columns):
    """Extract the known crop / season / state values from the expected columns."""
    crops, seasons, states = set(), set(), set()
    for col in columns:
        if col.startswith("Crop_") and col != "Crop_Year":
            crops.add(col[len("Crop_"):].strip())
        elif col.startswith("Season_"):
            seasons.add(col[len("Season_"):].strip())
        elif col.startswith("State_"):
            states.add(col[len("State_"):].strip())
    return crops, seasons, states


if _expected_columns:
    _KNOWN_CROPS, _KNOWN_SEASONS, _KNOWN_STATES = _build_known_categories(_expected_columns)
    # Build a lowercase→canonical lookup for every known value
    _CROP_LOWER = {c.lower(): c for c in _KNOWN_CROPS}
    _SEASON_LOWER = {s.lower(): s for s in _KNOWN_SEASONS}
    _STATE_LOWER = {s.lower(): s for s in _KNOWN_STATES}
    # Stripped column lookup to handle trailing whitespace in training columns
    _COL_LOOKUP = {col.strip(): col for col in _expected_columns}
else:
    _KNOWN_CROPS = _KNOWN_SEASONS = _KNOWN_STATES = set()
    _CROP_LOWER = _SEASON_LOWER = _STATE_LOWER = {}
    _COL_LOOKUP = {}


# ═══════════════════════════════════════════════════════════════════════════════
#  ALIAS MAPS  — common user inputs → training category names
# ═══════════════════════════════════════════════════════════════════════════════

CROP_ALIASES = {
    # Common English vs Indian names
    "corn": "Maize",
    "maize": "Maize",
    "paddy": "Rice",
    "rice": "Rice",
    "wheat": "Wheat",
    "soybean": "Soyabean",
    "soya bean": "Soyabean",
    "soyabean": "Soyabean",
    "mustard": "Rapeseed &Mustard",
    "rapeseed": "Rapeseed &Mustard",
    "sugarcane": "Sugarcane",
    "sugar cane": "Sugarcane",
    "cotton": "Cotton(lint)",
    "groundnut": "Groundnut",
    "peanut": "Groundnut",
    "potato": "Potato",
    "onion": "Onion",
    "banana": "Banana",
    "coconut": "Coconut ",   # note: trailing space in training data
    "tobacco": "Tobacco",
    "turmeric": "Turmeric",
    "ginger": "Ginger",
    "garlic": "Garlic",
    "sunflower": "Sunflower",
    "barley": "Barley",
    "jowar": "Jowar",
    "sorghum": "Jowar",
    "ragi": "Ragi",
    "finger millet": "Ragi",
    "bajra": "Bajra",
    "pearl millet": "Bajra",
    "jute": "Jute",
    "linseed": "Linseed",
    "sesamum": "Sesamum",
    "sesame": "Sesamum",
    "tapioca": "Tapioca",
    "cassava": "Tapioca",
    "sweet potato": "Sweet potato",
    "black pepper": "Black pepper",
    "pepper": "Black pepper",
    "cardamom": "Cardamom",
    "cashew": "Cashewnut",
    "cashewnut": "Cashewnut",
    "castor": "Castor seed",
    "castor seed": "Castor seed",
    "coriander": "Coriander",
    "arhar": "Arhar/Tur",
    "tur": "Arhar/Tur",
    "toor": "Arhar/Tur",
    "pigeon pea": "Arhar/Tur",
    "moong": "Moong(Green Gram)",
    "mung": "Moong(Green Gram)",
    "green gram": "Moong(Green Gram)",
    "urad": "Urad",
    "black gram": "Urad",
    "gram": "Gram",
    "chickpea": "Gram",
    "chana": "Gram",
    "masoor": "Masoor",
    "lentil": "Masoor",
    "safflower": "Safflower",
    "small millets": "Small millets",
    "arecanut": "Arecanut",
    "dry chillies": "Dry chillies",
    "chilli": "Dry chillies",
    "chili": "Dry chillies",
}

SEASON_ALIASES = {
    "kharif": "Kharif",
    "rabi": "Rabi",
    "summer": "Summer",
    "winter": "Winter",
    "whole year": "Whole Year",
    "annual": "Whole Year",
    "autumn": "Autumn",    # reference/dropped category
    "zaid": "Summer",
}

STATE_ALIASES = {
    # Handle common alternate spellings / abbreviations
    "ap": "Andhra Pradesh",  # dropped reference, still useful
    "andhra pradesh": "Andhra Pradesh",
    "up": "Uttar Pradesh",
    "uttar pradesh": "Uttar Pradesh",
    "mp": "Madhya Pradesh",
    "madhya pradesh": "Madhya Pradesh",
    "hp": "Himachal Pradesh",
    "himachal pradesh": "Himachal Pradesh",
    "j&k": "Jammu and Kashmir",
    "j & k": "Jammu and Kashmir",
    "jammu and kashmir": "Jammu and Kashmir",
    "jammu & kashmir": "Jammu and Kashmir",
    "tamil nadu": "Tamil Nadu",
    "tamilnadu": "Tamil Nadu",
    "west bengal": "West Bengal",
    "wb": "West Bengal",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "chhattisgarh": "Chhattisgarh",
    "chattisgarh": "Chhattisgarh",
    "jharkhand": "Jharkhand",
    "uttarakhand": "Uttarakhand",
    "uttaranchal": "Uttarakhand",
    "telangana": "Telangana",
    "delhi": "Delhi",
    "new delhi": "Delhi",
    "pondicherry": "Puducherry",
    "puducherry": "Puducherry",
    "punjab": "Punjab",
    "haryana": "Haryana",
    "bihar": "Bihar",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "maharashtra": "Maharashtra",
    "gujarat": "Gujarat",
    "goa": "Goa",
    "assam": "Assam",
    "sikkim": "Sikkim",
    "nagaland": "Nagaland",
    "mizoram": "Mizoram",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "tripura": "Tripura",
    "arunachal pradesh": "Arunachal Pradesh",
}


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def safe_float(value, default=0.0):
    """Safely convert a value to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _resolve_category(raw_value, alias_map, lower_lookup, known_set, category_name):
    """
    Resolve a user-provided category string to the exact training category.

    Resolution order:
        1. Alias map (e.g. "corn" → "Maize")
        2. Lowercase exact match against known categories
        3. Fallback: first known category (with a warning)
    """
    raw_lower = raw_value.strip().lower()

    # 1. Check alias map
    if raw_lower in alias_map:
        resolved = alias_map[raw_lower]
        logger.info(f"[ML Node]   {category_name}: '{raw_value}' → '{resolved}' (alias)")
        return resolved

    # 2. Check lowercase exact match against known categories
    if raw_lower in lower_lookup:
        resolved = lower_lookup[raw_lower]
        logger.info(f"[ML Node]   {category_name}: '{raw_value}' → '{resolved}' (exact match)")
        return resolved

    # 3. Substring / fuzzy match — check if user input is contained in any known value
    for known_lower, known_canonical in lower_lookup.items():
        if raw_lower in known_lower or known_lower in raw_lower:
            logger.warning(
                f"[ML Node]   {category_name}: '{raw_value}' → '{known_canonical}' (fuzzy match)"
            )
            return known_canonical

    # 4. Fallback — use first known value (sorted for determinism)
    if known_set:
        fallback = sorted(known_set)[0]
        logger.warning(
            f"[ML Node]   ⚠️ {category_name}: '{raw_value}' NOT recognized. "
            f"Falling back to '{fallback}'"
        )
        return fallback

    logger.error(f"[ML Node]   ❌ {category_name}: '{raw_value}' — no known categories at all!")
    return raw_value


def _set_one_hot(feature_dict, prefix, value):
    """
    Set the correct one-hot column to 1.0, handling trailing whitespace in
    the training column names.

    Returns True if a matching column was found (i.e. this is NOT the
    dropped reference category).
    """
    col_name = f"{prefix}_{value}"

    # Try exact match
    if col_name in feature_dict:
        feature_dict[col_name] = 1.0
        logger.info(f"[ML Node]   ✅ One-hot: '{col_name}' = 1")
        return True

    # Try stripped match (training columns may have trailing whitespace)
    stripped = col_name.strip()
    if stripped in _COL_LOOKUP:
        actual_col = _COL_LOOKUP[stripped]
        feature_dict[actual_col] = 1.0
        logger.info(f"[ML Node]   ✅ One-hot: '{actual_col}' = 1 (via stripped match)")
        return True

    # Try with trailing space (known issue in training data)
    col_with_space = col_name + " "
    if col_with_space in feature_dict:
        feature_dict[col_with_space] = 1.0
        logger.info(f"[ML Node]   ✅ One-hot: '{col_with_space}' = 1 (trailing space)")
        return True

    # Not found — this is the dropped reference category (e.g., Arecanut, Andhra Pradesh, Autumn)
    logger.info(
        f"[ML Node]   ℹ️  One-hot: '{col_name}' not in columns "
        f"(likely the dropped reference category — this is correct)"
    )
    return False


# ═══════════════════════════════════════════════════════════════════════════════
#  ML NODE  (main function)
# ═══════════════════════════════════════════════════════════════════════════════

def ml_node(state: dict) -> dict:
    """
    ML prediction node for LangGraph pipeline.

    Constructs the feature vector manually to match the exact columns the model
    was trained on.  Handles:
      - Category name normalization (aliases, casing)
      - Numeric feature scaling to match training data magnitudes
      - Trailing whitespace in training column names
      - Detailed debug logging at every step
      - Proper error handling with traceback
    """
    try:
        # ── Guard: artifacts must be loaded ──
        if _model is None or _scaler is None or _expected_columns is None:
            logger.error("[ML Node] ❌ Artifacts not loaded — returning 0.0")
            state["predicted_yield"] = 0.0
            return state

        farm_data = state.get("farm_data", {})
        logger.info(f"[ML Node] ═══ Starting prediction ═══")
        logger.info(f"[ML Node] Raw farm_data: {farm_data}")

        # ── Extract raw inputs ──
        raw_crop = str(farm_data.get("crop", "Rice")).strip()
        raw_season = str(farm_data.get("season", "Kharif")).strip()
        raw_state = str(farm_data.get("state", "Punjab")).strip()

        rainfall = safe_float(farm_data.get("rainfall"), 1200.0)
        temperature = safe_float(farm_data.get("temperature"), 25.0)
        ph = safe_float(farm_data.get("pH"), 6.5)
        fertilizer_user = safe_float(farm_data.get("fertilizer"), 100.0)

        logger.info(
            f"[ML Node] Raw inputs → crop='{raw_crop}', season='{raw_season}', "
            f"state='{raw_state}', rainfall={rainfall}, temp={temperature}, "
            f"pH={ph}, fertilizer={fertilizer_user}"
        )

        # ── Resolve categorical inputs ──
        crop = _resolve_category(raw_crop, CROP_ALIASES, _CROP_LOWER, _KNOWN_CROPS, "Crop")
        season = _resolve_category(raw_season, SEASON_ALIASES, _SEASON_LOWER, _KNOWN_SEASONS, "Season")
        state_name = _resolve_category(raw_state, STATE_ALIASES, _STATE_LOWER, _KNOWN_STATES, "State")

        logger.info(
            f"[ML Node] Resolved → Crop='{crop}', Season='{season}', State='{state_name}'"
        )

        # ── Build feature vector (all zeros initially) ──
        feature_dict = {col: 0.0 for col in _expected_columns}

        # ── Map numeric features ──
        # CRITICAL: The training data has these columns at very different scales
        # than what a user might provide:
        #
        #   Fertilizer:  training mean ≈ 24,000,000  (state-level aggregate in kg)
        #   Pesticide:   training mean ≈ 49,000      (state-level aggregate)
        #   Area:        training mean ≈ 180,000      (hectares)
        #   Crop_Year:   range 1997-2020
        #   Annual_Rainfall: range 300-6500           (mm, this matches user input)
        #
        # The user provides fertilizer as kg per hectare (e.g. 50-300).
        # We need to scale it to approximately match the training distribution.
        # Using a multiplier that maps user-scale (~50-300 kg/ha) to training-scale (~1M-50M).
        # A factor of ~100,000 maps 100 kg/ha → 10,000,000 (near training median of ~1.2M).
        #
        # Similarly for Pesticide and Area, we use sensible defaults that place
        # the prediction within the training distribution.

        # ── Improved Scaling ──
        FERTILIZER_SCALE = 5000
        PESTICIDE_DEFAULT = 1000.0
        AREA_DEFAULT = 5000.0

        numeric_mapping = {
            "Annual_Rainfall": rainfall,
            "Fertilizer": fertilizer_user * FERTILIZER_SCALE,
            "Crop_Year": 2020.0,
            "Area": AREA_DEFAULT,
            "Pesticide": PESTICIDE_DEFAULT,
        }

        for col, val in numeric_mapping.items():
            if col in feature_dict:
                feature_dict[col] = val

        if "Temperature" in feature_dict:
            feature_dict["Temperature"] = temperature

        if "pH" in feature_dict:
            feature_dict["pH"] = ph

        # 🔥 Feature Engineering
        if "Temp_Rainfall_Interaction" in feature_dict:
            feature_dict["Temp_Rainfall_Interaction"] = temperature * rainfall

        if "pH_Adjusted" in feature_dict:
            feature_dict["pH_Adjusted"] = abs(ph - 6.5)

        # ── Set one-hot encoded categorical features ──
        _set_one_hot(feature_dict, "Crop", crop)
        _set_one_hot(feature_dict, "Season", season)
        _set_one_hot(feature_dict, "State", state_name)

        # ── Create DataFrame in exact column order ──
        input_df = pd.DataFrame([feature_dict])[_expected_columns]

        # ── Debug: show all non-zero features ──
        non_zero = {c: input_df[c].iloc[0] for c in _expected_columns if input_df[c].iloc[0] != 0}
        logger.info(f"[ML Node] Non-zero features ({len(non_zero)}):")
        for col, val in non_zero.items():
            logger.info(f"[ML Node]     {col} = {val}")

        if len(non_zero) <= 5:
            # Only numeric features are non-zero → all categorical columns are 0
            # This means the categorical input matched a dropped reference category
            # OR the resolution failed. Either way, the prediction is valid but
            # may be dominated by numeric features.
            logger.warning(
                "[ML Node] ⚠️ Very few non-zero features. Categorical columns may all "
                "be matching the dropped reference category."
            )

        # ── Scale & predict ──
        X_scaled = _scaler.transform(input_df)
        prediction = _model.predict(X_scaled)[0]

        # 🔥 Clamp prediction (realistic range)
        prediction = max(0.5, min(float(prediction), 10.0))

        logger.info(f"[ML Node] ✅ Predicted yield: {prediction:.4f}")
        state["predicted_yield"] = prediction

    except Exception as e:
        logger.error(f"[ML Node] ❌ Exception in ml_node: {type(e).__name__}: {e}")
        logger.error(f"[ML Node] Traceback:\n{traceback.format_exc()}")
        state["predicted_yield"] = 0.0

    return state