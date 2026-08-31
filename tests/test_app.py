from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_rejects_duplicate_participant():
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_and_unregister_participant():
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        "/activities/Chess Club/signup?email=" + email
    )
    assert signup_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants

    unregister_response = client.delete(
        "/activities/Chess Club/participants/" + email
    )
    assert unregister_response.status_code == 200
    assert "unregistered" in unregister_response.json()["message"].lower()

    updated_response = client.get("/activities")
    updated_participants = updated_response.json()["Chess Club"]["participants"]
    assert email not in updated_participants
