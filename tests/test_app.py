from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_rejects_duplicate_participant():
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={duplicate_email}"
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_and_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    activities_response = client.get("/activities")
    participants_after_signup = activities_response.json()[activity_name]["participants"]

    unregister_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert email in participants_after_signup
    assert unregister_response.status_code == 200
    assert "unregistered" in unregister_response.json()["message"].lower()
    assert email not in updated_participants
