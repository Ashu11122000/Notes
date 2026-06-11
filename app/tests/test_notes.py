def get_token(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "email": "note@example.com",
            "password": "password123"
        }
    )

    # Login user
    response = client.post(
        "/auth/login",
        json={
            "email": "note@example.com",
            "password": "password123"
        }
    )

    return response.json()["access_token"]


def test_create_note(test_client):
    token = get_token(test_client)

    response = test_client.post(
        "/notes",
        json={
            "title": "Test Note",
            "content": "Hello"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Note"
    assert data["content"] == "Hello"
    assert "id" in data


def test_get_notes(test_client):
    token = get_token(test_client)

    # Create a note first
    test_client.post(
        "/notes",
        json={
            "title": "My Note",
            "content": "Content"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = test_client.get(
        "/notes",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1