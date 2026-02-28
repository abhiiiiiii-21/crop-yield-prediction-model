import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def preprocess_data(df, is_training=True, expected_columns=None):
    df = df.copy()

    if "Production" in df.columns:
        df = df.drop(columns=["Production"])

    if "Season" in df.columns:
        df["Season"] = df["Season"].str.strip()

    categorical_cols = ["Crop", "Season", "State"]
    df = pd.get_dummies(df, columns=[c for c in categorical_cols if c in df.columns], drop_first=True)

    if not is_training and expected_columns is not None:
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_columns]

    return df


def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    y_pred = model.predict(X_test)

    train_r2 = r2_score(y_train, model.predict(X_train))
    test_r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"--- {model_name} Evaluation ---")
    print(f"Train R²: {train_r2:.4f}")
    print(f"Test  R²: {test_r2:.4f}")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print("-" * 40)

    return test_r2


def train_and_evaluate(data_path):
    df = pd.read_csv(data_path)
    df_processed = preprocess_data(df, is_training=True)

    X = df_processed.drop(columns=["Yield"])
    y = df_processed["Yield"]

    artifacts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    joblib.dump(X.columns.tolist(), os.path.join(artifacts_dir, "feature_columns.pkl"))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, os.path.join(artifacts_dir, "scaler.pkl"))

    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)

    dt_model = DecisionTreeRegressor(max_depth=8, random_state=42)
    dt_model.fit(X_train_scaled, y_train)

    lr_r2 = evaluate_model(lr_model, X_train_scaled, X_test_scaled, y_train, y_test, "Linear Regression")
    dt_r2 = evaluate_model(dt_model, X_train_scaled, X_test_scaled, y_train, y_test, "Decision Tree (depth=8)")

    best_model, best_name = (dt_model, "Decision Tree") if dt_r2 >= lr_r2 else (lr_model, "Linear Regression")

    print(f"\nBest model: {best_name} (R² = {max(lr_r2, dt_r2):.4f}). Saving...")
    joblib.dump(best_model, os.path.join(artifacts_dir, "best_yield_model.pkl"))
    print("Model training and evaluation completed. Artifacts saved to:", artifacts_dir)


def predict_yield(new_data_df):
    artifacts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../artifacts")
    try:
        model = joblib.load(os.path.join(artifacts_dir, "best_yield_model.pkl"))
        scaler = joblib.load(os.path.join(artifacts_dir, "scaler.pkl"))
        expected_columns = joblib.load(os.path.join(artifacts_dir, "feature_columns.pkl"))
    except FileNotFoundError as e:
        raise FileNotFoundError("Artifacts not found. Run train_and_evaluate() first.") from e

    processed_df = preprocess_data(new_data_df, is_training=False, expected_columns=expected_columns)
    X_scaled = scaler.transform(processed_df)

    predictions = model.predict(X_scaled)

    result_df = new_data_df.copy()
    result_df["Predicted_Yield"] = predictions

    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame({
            "Feature": expected_columns,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=False).reset_index(drop=True)
    elif hasattr(model, "coef_"):
        importance_df = pd.DataFrame({
            "Feature": expected_columns,
            "Importance": model.coef_
        }).sort_values("Importance", ascending=False).reset_index(drop=True)
    else:
        importance_df = pd.DataFrame(columns=["Feature", "Importance"])

    result_df.reset_index(drop=True, inplace=True)
    return result_df, importance_df


if __name__ == "__main__":
    DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/raw/crop_yield.csv")

    if os.path.exists(DATA_PATH):
        train_and_evaluate(DATA_PATH)

        print("\n--- Testing predict_yield with sample data ---")
        df_raw = pd.read_csv(DATA_PATH)
        sample_df = df_raw.head(5)

        result_df, importance_df = predict_yield(sample_df)
        print(result_df[["Crop", "State", "Yield", "Predicted_Yield"]])
        print("\nTop 10 Important Features:")
        print(importance_df.head(10))
    else:
        print(f"Data file not found at {DATA_PATH}. Please check the path.")
