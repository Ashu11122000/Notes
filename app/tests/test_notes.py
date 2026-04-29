def get_token(client):
    client.post("/auth/register", json={
        "email": "note@example.com",
        "password": "password123"
    })

    response = client.post("/auth/login", json={
        "email": "note@example.com",
        "password": "password123"
    })

    return response.json()["access_token"]


def test_create_note(test_client):
    token = get_token(test_client)

    response = test_client.post(
        "/notes",
        json={"title": "Test Note", "content": "Hello"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201


def test_get_notes(test_client):
    token = get_token(test_client)

    response = test_client.get(
        "/notes",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200