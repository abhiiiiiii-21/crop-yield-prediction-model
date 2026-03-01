# Intelligent Crop Yield Prediction System

Milestone 1 -- ML-Based System\
Deployed Application:\
https://abhiiiiiii-21-crop-yield-prediction-model-appapp-xywyvd.streamlit.app/

------------------------------------------------------------------------

## Overview

The Intelligent Crop Yield Prediction System is a machine
learning-powered application designed to predict agricultural crop yield
using historical data.

The system models yield prediction as a supervised regression problem
and provides an interactive dashboard for analysis and inference.

This project demonstrates:

-   End-to-end ML pipeline implementation
-   Feature engineering and leakage prevention
-   Model evaluation and selection
-   Inference pipeline design
-   Deployment using Streamlit

------------------------------------------------------------------------

## Problem Statement

Agricultural productivity plays a crucial role in economic stability and
food security.

Crop yield prediction enables:

-   Strategic resource allocation
-   Fertilizer optimization
-   Risk mitigation
-   Revenue forecasting
-   Policy planning

The objective of this project is to design and deploy a machine learning
system capable of predicting crop yield based on agricultural features.

The problem is modeled as:

ŷ = f(X)

Where: - X = Feature matrix (Crop, State, Season, Area, etc.) - ŷ =
Predicted Yield

------------------------------------------------------------------------

## Dataset Description

-   Total Observations: \~19,700
-   Total Features: 10 columns
-   Target Variable: Yield (continuous numerical variable)

Features include:

-   Crop
-   State
-   Season
-   Area
-   Production (removed to prevent leakage)
-   Yield

No missing values were present in the dataset.

------------------------------------------------------------------------

## Feature Engineering & Preprocessing

### Target Leakage Prevention

The `Production` column was removed because:

Yield = Production / Area

Including it would introduce mathematical leakage.

### Categorical Encoding

Applied One-Hot Encoding to:

-   Crop
-   Season
-   State

Using:

pd.get_dummies(drop_first=True)

### Feature Scaling

Applied StandardScaler:

z = (x − μ) / σ

Scaler was fit only on training data to prevent data leakage.

------------------------------------------------------------------------

## Methodology

### Train-Test Split

-   80% Training
-   20% Testing
-   Random State = 42

### Models Implemented

1.  Linear Regression (Baseline)
2.  Decision Tree Regressor
    -   max_depth = 8\
    -   random_state = 42

------------------------------------------------------------------------

## Model Performance (Final Model: Decision Tree)

  Metric        Value
  ------------- ---------
  Train R²      0.989
  Test R²       0.973
  MAE           10.47
  RMSE          147.379
  Adjusted R²   0.9636

Interpretation:

-   High test R² indicates strong generalization.
-   Small train-test gap suggests limited overfitting.
-   Decision Tree outperformed Linear Regression.

------------------------------------------------------------------------

## Inference Pipeline

Artifacts Saved:

-   artifacts/best_model.pkl
-   artifacts/scaler.pkl
-   artifacts/feature_columns.pkl

Prediction Workflow:

1.  Load trained model
2.  Apply identical preprocessing
3.  Align feature schema
4.  Apply scaling
5.  Generate yield prediction

------------------------------------------------------------------------

## System Architecture

Input CSV\
→ Preprocessing (Encoding + Scaling)\
→ Model Prediction\
→ Dashboard Visualization\
→ Yield Forecast Output

The system supports:

-   Default dataset analysis
-   Custom CSV upload
-   KPI dashboard
-   Feature importance visualization

------------------------------------------------------------------------

## Deployment

Live Application:\
https://abhiiiiiii-21-crop-yield-prediction-model-appapp-xywyvd.streamlit.app/

------------------------------------------------------------------------

## Project Structure

    crop-yield-prediction-model/
    │
    ├── app/
    │   └── app.py
    │
    ├── src/
    │   └── model_pipeline.py
    │   └── data_preprocessing.py
    │
    ├── data/
    │   └── crop_yield.csv
    │
    ├── artifacts/           (ignored in Git)
    │
    ├── .streamlit/
    │   └── config.toml
    │
    ├── requirements.txt
    ├── README.md
    └── .gitignore

------------------------------------------------------------------------

## Technologies Used

-   Python
-   Pandas
-   NumPy
-   Scikit-learn
-   Streamlit
-   Plotly

------------------------------------------------------------------------

## Conclusion

The Intelligent Crop Yield Prediction System successfully:

-   Prevents target leakage
-   Implements robust preprocessing
-   Evaluates multiple regression models
-   Selects optimal model based on performance
-   Deploys via an interactive dashboard

The Decision Tree Regressor demonstrated superior capability in
capturing non-linear agricultural relationships.
