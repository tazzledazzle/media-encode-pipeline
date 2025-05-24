# tests/test_api.py
from fastapi.testclient import TestClient
import pytest
import sys
import os

# Add the pipeline-api directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pipeline-api'))

from app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_submit_job_success(client):
    """Test successful job submission"""
    payload = {
        "input_url": "s3://bucket/test.mp4",
        "profiles": [{"name": "720p"}, {"name": "480p"}]
    }
    response = client.post("/encode-job", json=payload)
    assert response.status_code == 200
    assert "job_id" in response.json()
    assert len(response.json()["profiles"]) == 2

def test_submit_job_invalid_url(client):
    """Test job submission with invalid S3 URL"""
    payload = {
        "input_url": "invalid-url",
        "profiles": [{"name": "720p"}]
    }
    response = client.post("/encode-job", json=payload)
    assert response.status_code == 400
    assert "error" in response.json()

def test_submit_job_invalid_profile(client):
    """Test job submission with invalid profile"""
    payload = {
        "input_url": "s3://bucket/test.mp4",
        "profiles": [{"name": "invalid-profile"}]
    }
    response = client.post("/encode-job", json=payload)
    assert response.status_code == 400
    assert "error" in response.json()

def test_get_job_status(client):
    """Test getting job status"""
    # First create a job
    payload = {
        "input_url": "s3://bucket/test.mp4",
        "profiles": [{"name": "720p"}]
    }
    response = client.post("/encode-job", json=payload)
    job_id = response.json()["job_id"]

    # Get status
    response = client.get(f"/encode-job/{job_id}")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "profiles" in response.json()

def test_get_nonexistent_job(client):
    """Test getting status of non-existent job"""
    response = client.get("/encode-job/nonexistent")
    assert response.status_code == 404
    assert "error" in response.json()