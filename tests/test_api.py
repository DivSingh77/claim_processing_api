import os
import sys

from fastapi.testclient import TestClient

# Add backend to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app  # Ensure this import works

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_submit_claim():
    claim_data = {"payer": "InsuranceCo", "amount": 500.0, "procedure_codes": "X123"}
    response = client.post("/claims", params=claim_data)
    assert response.status_code == 200
    assert response.json()["payer"] == "InsuranceCo"

def test_get_claim():
    response = client.get("/claims/1")
    assert response.status_code in [200, 404]  # 404 if claim not found

def test_claim_status():
    response = client.get("/claims/status/1")
    assert response.status_code in [200, 404]
