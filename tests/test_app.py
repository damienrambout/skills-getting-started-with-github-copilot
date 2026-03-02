def test_root_redirect(client):
    # Arrange: client fixture

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200


def test_get_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow(client):
    # Arrange
    activity = "Chess Club"
    email = "alice.test@example.com"

    # Precondition: ensure email not already signed up
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants

    # Act: sign up
    signup = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: signup succeeded and participant added
    assert signup.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act: unregister
    unregister = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert: unregister succeeded and participant removed
    assert unregister.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_signup_existing_student_returns_400(client):
    # Arrange
    activity = "Chess Club"
    # use an existing participant from seed data
    existing_email = "michael@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": existing_email})

    # Assert
    assert resp.status_code == 400


def test_invalid_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "nobody@example.com"

    # Act
    resp_signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    resp_unregister = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert resp_signup.status_code == 404
    assert resp_unregister.status_code == 404
