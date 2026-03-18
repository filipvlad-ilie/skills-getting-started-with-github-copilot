import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory DB before each test
    for activity in activities.values():
        activity['participants'].clear()
    activities['Chess Club']['participants'].extend(["michael@mergington.edu", "daniel@mergington.edu"])
    activities['Programming Class']['participants'].extend(["emma@mergington.edu", "sophia@mergington.edu"])
    activities['Gym Class']['participants'].extend(["john@mergington.edu", "olivia@mergington.edu"])
    activities['Basketball Team']['participants'].extend(["marcus@mergington.edu"])
    activities['Tennis Club']['participants'].extend(["sarah@mergington.edu", "alex@mergington.edu"])
    activities['Art Studio']['participants'].extend(["isabella@mergington.edu"])
    activities['Music Band']['participants'].extend(["james@mergington.edu", "lily@mergington.edu"])
    activities['Debate Club']['participants'].extend(["noah@mergington.edu"])
    activities['Science Olympiad']['participants'].extend(["ava@mergington.edu", "ethan@mergington.edu"])


def test_get_activities():
    # Arrange: nothing to set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"].lower().startswith("student already signed up")


def test_signup_full_capacity():
    # Arrange
    activity = "Chess Club"
    # Fill up the activity
    activities[activity]["participants"] = [f"s{i}@mergington.edu" for i in range(activities[activity]["max_participants"])]
    email = "overflow@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "full capacity" in response.json()["detail"].lower()


def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_not_registered():
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()
