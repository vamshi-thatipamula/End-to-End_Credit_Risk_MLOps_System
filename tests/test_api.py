import sys

from unittest.mock import MagicMock
from fastapi.testclient import TestClient


# Mock the prediction_helper module before importing the FastAPI application.
mock_prediction_helper = MagicMock()
mock_prediction_helper.predict.return_value = (0.25, 750, "Excellent")

sys.modules["fastapi_app.prediction_helper"] = mock_prediction_helper

from fastapi_app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Credit Risk Modelling API is running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_validation():
    response = client.post(
        "/predict",
        json={}
    )

    assert response.status_code == 422

def test_predict():
    request_data = {
        "age": 35,
        "income": 800000,
        "loan_amount": 300000,
        "loan_tenure_months": 36,
        "avg_dpd_per_delinquency": 5,
        "delinquency_ratio": 10,
        "credit_utilization_ratio": 30,
        "num_open_accounts": 2,
        "residence_type": "Owned",
        "loan_purpose": "Home",
        "loan_type": "Secured"
    }

    response = client.post(
        "/predict",
        json=request_data
    )

    assert response.status_code == 200

    result = response.json()

    assert "default_probability" in result
    assert "credit_score" in result
    assert "credit_rating" in result

    assert result["default_probability"] == 0.25
    assert result["credit_score"] == 750
    assert result["credit_rating"] == "Excellent"