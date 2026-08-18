from pathlib import Path
import joblib
import numpy as np
import pandas as pd

# ==============================================================================
# Load Saved Objects
# ==============================================================================

MODEL_PATH = Path(__file__).parent / "artifacts" / "model_data.joblib"
saved_objects = joblib.load(MODEL_PATH)

model = saved_objects["model"]
scaler = saved_objects["scaler"]
features = saved_objects["features"]
cols_to_scale = saved_objects["cols_to_scale"]


# ==============================================================================
# Credit Rating
# ==============================================================================

def get_rating(score):
    """
    Convert credit score into a credit rating.
    """

    if 300 <= score < 500:
        return "Poor"

    elif 500 <= score < 650:
        return "Average"

    elif 650 <= score < 750:
        return "Good"

    elif 750 <= score <= 900:
        return "Excellent"

    return "Undefined"


# ==============================================================================
# Input Preparation
# ==============================================================================

def prepare_input(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    avg_dpd_per_delinquency,
    delinquency_ratio,
    credit_utilization_ratio,
    num_open_accounts,
    residence_type,
    loan_purpose,
    loan_type
):

    # --------------------------------------------------------------------------
    # Engineered Feature
    # --------------------------------------------------------------------------

    loan_to_income = (
        loan_amount / income
        if income > 0
        else 0
    )

    # --------------------------------------------------------------------------
    # Base Input
    # --------------------------------------------------------------------------

    input_dict = {
        "age": age,
        "loan_tenure_months": loan_tenure_months,
        "number_of_open_accounts": num_open_accounts,
        "credit_utilization_ratio": credit_utilization_ratio,
        "loan_to_income": loan_to_income,
        "delinquency_ratio": delinquency_ratio,
        "avg_dpd_per_delinquency": avg_dpd_per_delinquency,

        "residence_type_Owned": 0,
        "residence_type_Rented": 0,

        "loan_purpose_Education": 0,
        "loan_purpose_Home": 0,
        "loan_purpose_Personal": 0,

        "loan_type_Unsecured": 0
    }

    # --------------------------------------------------------------------------
    # One-Hot Encoding
    # --------------------------------------------------------------------------

    if residence_type == "Owned":
        input_dict["residence_type_Owned"] = 1

    elif residence_type == "Rented":
        input_dict["residence_type_Rented"] = 1

    if loan_purpose == "Education":
        input_dict["loan_purpose_Education"] = 1

    elif loan_purpose == "Home":
        input_dict["loan_purpose_Home"] = 1

    elif loan_purpose == "Personal":
        input_dict["loan_purpose_Personal"] = 1

    if loan_type == "Unsecured":
        input_dict["loan_type_Unsecured"] = 1

    input_df = pd.DataFrame([input_dict])

    # --------------------------------------------------------------------------
    # Create Temporary DataFrame for Scaling
    # --------------------------------------------------------------------------

    temp_df = pd.DataFrame(columns=cols_to_scale)

    for col in cols_to_scale:
        temp_df[col] = [0]

    # Populate available columns
    available_values = {
        "age": age,
        "loan_tenure_months": loan_tenure_months,
        "number_of_open_accounts": num_open_accounts,
        "credit_utilization_ratio": credit_utilization_ratio,
        "loan_to_income": loan_to_income,
        "delinquency_ratio": delinquency_ratio,
        "avg_dpd_per_delinquency": avg_dpd_per_delinquency
    }

    for col, value in available_values.items():
        if col in temp_df.columns:
            temp_df[col] = value

    # Scale numerical features
    temp_df[cols_to_scale] = scaler.transform(temp_df)

    # Copy scaled values back
    for col in temp_df.columns:
        if col in input_df.columns:
            input_df[col] = temp_df[col]

    # Keep only model features
    input_df = input_df[features]

    return input_df

# ==============================================================================
# Prediction
# ==============================================================================

def predict(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    avg_dpd_per_delinquency,
    delinquency_ratio,
    credit_utilization_ratio,
    num_open_accounts,
    residence_type,
    loan_purpose,
    loan_type
):
    """
    Predict default probability, credit score, and credit rating.
    """

    input_df = prepare_input(
        age,
        income,
        loan_amount,
        loan_tenure_months,
        avg_dpd_per_delinquency,
        delinquency_ratio,
        credit_utilization_ratio,
        num_open_accounts,
        residence_type,
        loan_purpose,
        loan_type
    )

    # --------------------------------------------------------------------------
    # Calculate Default Probability using Logistic Regression Equation
    # --------------------------------------------------------------------------

    x = np.dot(input_df.values, model.coef_.T) + model.intercept_

    probability = 1 / (1 + np.exp(-x))

    probability = probability.flatten()[0]

    # --------------------------------------------------------------------------
    # Calculate Credit Score (300–900)
    # --------------------------------------------------------------------------

    credit_score = int((1 - probability) * 600 + 300)

    # --------------------------------------------------------------------------
    # Determine Credit Rating
    # --------------------------------------------------------------------------

    rating = get_rating(credit_score)

    return probability, credit_score, rating