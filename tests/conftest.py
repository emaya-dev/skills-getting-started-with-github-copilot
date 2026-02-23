import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    # Arrange: create a fresh TestClient for each test
    return TestClient(app)
