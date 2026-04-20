import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


# =========================
# PREPROCESSING
# =========================
def preprocess_data(df, is_training=True, expected_columns=None):
    df = df.copy()

    if "Production" in df.columns:
        df = df.drop(columns=["Production"])

    if "Season" in df.columns:
        df["Season"] = df["Season"].str.strip()

    categorical_cols = ["Crop", "Season", "State"]
    df = pd.get_dummies(
        df,
        columns=[c for c in categorical_cols if c in df.columns],
        drop_first=True
    )

    if not is_training and expected_columns is not None:
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_columns]

    return df


# =========================
# TRAIN MODEL
# =========================
def train_and_evaluate(data_path):

    df = pd.read_csv(data_path)

    if "Yield" not in df.columns:
        raise ValueError("Dataset must contain 'Yield' column.")

    df_processed = preprocess_data(df, is_training=True)

    X = df_processed.drop(columns=["Yield"])
    y = df_processed["Yield"]

    artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../artifacts"))
    os.makedirs(artifacts_dir, exist_ok=True)

    joblib.dump(X.columns.tolist(), os.path.join(artifacts_dir, "feature_columns.pkl"))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, os.path.join(artifacts_dir, "scaler.pkl"))

    # Train Models
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42
    )

    model.fit(X_train_scaled, y_train)

    joblib.dump(model, os.path.join(artifacts_dir, "best_model.pkl"))

    y_pred = model.predict(X_test_scaled)

    metrics = {
        "R2": r2_score(y_test, y_pred),
        "MAE": mean_absolute_error(y_test, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred))
    }

    return "Random Forest", metrics
    


# =========================
# PREDICTION
# =========================
def predict_yield(new_data_df):

    artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../artifacts"))

    if not os.path.exists(artifacts_dir):
        raise FileNotFoundError(f"Artifacts not found at {artifacts_dir}")

    model = joblib.load(os.path.join(artifacts_dir, "best_model.pkl"))
    scaler = joblib.load(os.path.join(artifacts_dir, "scaler.pkl"))
    expected_columns = joblib.load(os.path.join(artifacts_dir, "feature_columns.pkl"))

    processed_df = preprocess_data(new_data_df, False, expected_columns)
    X_scaled = scaler.transform(processed_df)

    predictions = model.predict(X_scaled)

    result_df = new_data_df.copy()
    result_df["Predicted_Yield"] = predictions

    # Feature Importance
    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
    else:
        importance = model.coef_

    importance_df = pd.DataFrame({
        "Feature": expected_columns,
        "Importance": importance
    }).sort_values("Importance", ascending=False)

    return result_df, importance_df