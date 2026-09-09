import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "UP"}


def test_version():
    client = app.test_client()

    response = client.get("/version")

    assert response.status_code == 200
    assert response.get_json() == {"version": "1.0.0"}


def test_environment():
    client = app.test_client()

    response = client.get("/environment")

    assert response.status_code == 200
    assert "environment" in response.get_json()
