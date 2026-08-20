# ==============================================================================
# No application logic change.
# This comment is added only to create a test commit for verifying the CI/CD pipeline.
# ==============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from fastapi_app.prediction_helper import predict


# ==============================================================================
# FastAPI Application
# ==============================================================================

app = FastAPI(
    title="Credit Risk Modelling API",
    description="API for predicting credit default probability, credit score, and credit rating.",
    version="1.0.0"
)


# ==============================================================================
# Prediction Request Schema
# ==============================================================================

class CreditRiskRequest(BaseModel):

    age: int = Field(
        ...,
        ge=18,
        le=100,
        description="Applicant age"
    )

    income: float = Field(
        ...,
        gt=0,
        description="Annual income in INR"
    )

    loan_amount: float = Field(
        ...,
        gt=0,
        description="Loan amount in INR"
    )

    loan_tenure_months: int = Field(
        ...,
        ge=1,
        description="Loan tenure in months"
    )

    avg_dpd_per_delinquency: float = Field(
        ...,
        ge=0,
        description="Average days past due per delinquency"
    )

    delinquency_ratio: float = Field(
        ...,
        ge=0,
        le=100,
        description="Delinquency ratio (%)"
    )

    credit_utilization_ratio: float = Field(
        ...,
        ge=0,
        le=100,
        description="Credit utilization ratio (%)"
    )

    num_open_accounts: int = Field(
        ...,
        ge=1,
        le=4,
        description="Number of open credit accounts"
    )

    residence_type: str = Field(
        ...,
        description="Residence type: Owned, Rented, or Mortgage"
    )

    loan_purpose: str = Field(
        ...,
        description="Loan purpose: Education, Home, Auto, or Personal"
    )

    loan_type: str = Field(
        ...,
        description="Loan type: Secured or Unsecured"
    )


# ==============================================================================
# Root Endpoint
# ==============================================================================

@app.get("/")
def home():

    return {
        "message": "Credit Risk Modelling API is running",
        "model": "Credit Risk Model",
        "model_alias": "champion"
    }


# ==============================================================================
# Health Check
# ==============================================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "Credit Risk Model",
        "alias": "champion"
    }


# ==============================================================================
# Prediction Endpoint
# ==============================================================================

@app.post("/predict")
def predict_credit_risk(request: CreditRiskRequest):

    try:

        probability, credit_score, rating = predict(
            request.age,
            request.income,
            request.loan_amount,
            request.loan_tenure_months,
            request.avg_dpd_per_delinquency,
            request.delinquency_ratio,
            request.credit_utilization_ratio,
            request.num_open_accounts,
            request.residence_type,
            request.loan_purpose,
            request.loan_type
        )

        return {
            "default_probability": round(float(probability), 4),
            "credit_score": credit_score,
            "credit_rating": rating
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Please try again later."
        )