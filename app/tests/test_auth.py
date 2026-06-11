def test_register(test_client):
    response = test_client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "message" in data
    assert "user_id" in data


def test_login(test_client):
    # Register User
    test_client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    # Login
    response = test_client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"