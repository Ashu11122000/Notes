def test_register(test_client):
    response = test_client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 201


def test_login(test_client):
    # First register
    test_client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "password123"
    })

    # Then login
    response = test_client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()