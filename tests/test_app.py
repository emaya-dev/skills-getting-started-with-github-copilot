
from fastapi.testclient import TestClient
import pytest
from urllib.parse import quote

# Note: The AAA (Arrange-Act-Assert) pattern is used in each test.

def test_get_activities(client):
    # Arrange
    # (client fixture provides a fresh TestClient)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Art Club" in data
    assert "participants" in data["Art Club"]

def test_signup_success(client):
    # Arrange
    email = "testuser@example.com"
    activity = "Art Club"
    encoded_activity = quote(activity)

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"].startswith("Signed up")
    # Confirm participant is added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_signup_duplicate(client):
    # Arrange
    email = "duplicate@example.com"
    activity = "Art Club"
    encoded_activity = quote(activity)
    client.post(f"/activities/{encoded_activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_nonexistent_activity(client):
    # Arrange
    email = "ghost@example.com"
    activity = "Nonexistent"
    encoded_activity = quote(activity)

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
