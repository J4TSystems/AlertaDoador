def test_create_donor(client):
    """
    Test creating a donor with valid data.
    """
    # Arrange
    donor_payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "blood_type": "A+",
    }

    # Act
    response = client.post("/donors/", json=donor_payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["full_name"] == donor_payload["full_name"]
    assert data["email"] == donor_payload["email"]
    assert data["blood_type"] == donor_payload["blood_type"]


def test_get_donors(client):
    """
    Test retrieving all donors.
    """
    # Arrange
    donor_payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "blood_type": "A+",
    }
    client.post("/donors/", json=donor_payload)

    # Act
    response = client.get("/donors/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["full_name"] == donor_payload["full_name"]


def test_get_donor_by_id(client):
    """
    Test retrieving a donor by their ID.
    """
    # Arrange
    donor_payload = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "blood_type": "O-",
    }
    create_response = client.post("/donors/", json=donor_payload)
    donor_id = create_response.json()["id"]

    # Act
    response = client.get(f"/donors/{donor_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["full_name"] == donor_payload["full_name"]


def test_delete_donor(client):
    """
    Test deleting a donor.
    """
    # Arrange
    donor_payload = {
        "full_name": "Delete Me",
        "email": "delete@example.com",
        "blood_type": "B+",
    }
    create_response = client.post("/donors/", json=donor_payload)
    donor_id = create_response.json()["id"]

    # Act
    delete_response = client.delete(f"/donors/{donor_id}")

    # Assert
    assert delete_response.status_code == 204
    # Verify deletion
    get_response = client.get("/donors/")
    assert len(get_response.json()) == 0


def test_delete_donor_not_found(client):
    """
    Test deleting a donor that does not exist.
    """
    # Act
    response = client.delete("/donors/999")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Donor not found"


def test_create_donor_duplicate_email(client):
    """
    Test that creating a donor with a duplicate email fails.
    """
    # Arrange
    donor_payload = {
        "full_name": "John Doe",
        "email": "duplicate@example.com",
        "blood_type": "A+",
    }
    client.post("/donors/", json=donor_payload)

    # Act
    response = client.post(
        "/donors/",
        json={
            "full_name": "Other Name",
            "email": "duplicate@example.com",
            "blood_type": "B-",
        },
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_create_donor_invalid_blood_type(client):
    """
    Test that creating a donor with an invalid blood type fails.
    """
    # Act
    response = client.post(
        "/donors/",
        json={
            "full_name": "Invalid Blood",
            "email": "invalid@example.com",
            "blood_type": "X+",
        },
    )

    # Assert
    assert response.status_code == 422  # Pydantic validation error
