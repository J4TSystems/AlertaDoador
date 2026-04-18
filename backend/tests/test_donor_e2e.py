import pytest

def test_create_donor(client):
    response = client.post(
        "/donors/",
        json={
            "full_name": "John Doe",
            "email": "john@example.com",
            "blood_type": "A+"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["full_name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["blood_type"] == "A+"

def test_get_donors(client):
    # First, create a donor
    client.post(
        "/donors/",
        json={
            "full_name": "John Doe",
            "email": "john@example.com",
            "blood_type": "A+"
        },
    )
    
    response = client.get("/donors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "John Doe"

def test_get_donor_by_id(client):
    # First, create a donor
    response = client.post(
        "/donors/",
        json={
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "blood_type": "O-"
        },
    )
    donor_id = response.json()["id"]
    
    response = client.get(f"/donors/{donor_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Jane Doe"

def test_delete_donor(client):
    # First, we create
    response = client.post(
        "/donors/",
        json={
            "full_name": "Delete Me",
            "email": "delete@example.com",
            "blood_type": "B+"
        },
    )
    donor_id = response.json()["id"]
    
    # Then we delete
    response = client.delete(f"/donors/{donor_id}")
    assert response.status_code == 204
    
    # Check if it was deleted
    response = client.get("/donors/")
    assert len(response.json()) == 0

def test_delete_donor_not_found(client):
    response = client.delete("/donors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Donor not found"

def test_create_donor_duplicate_email(client):
    # First, create a donor
    client.post(
        "/donors/",
        json={
            "full_name": "John Doe",
            "email": "duplicate@example.com",
            "blood_type": "A+"
        },
    )
    
    # Try to create with the same email again
    response = client.post(
        "/donors/",
        json={
            "full_name": "Other Name",
            "email": "duplicate@example.com",
            "blood_type": "B-"
        },
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_create_donor_invalid_blood_type(client):
    response = client.post(
        "/donors/",
        json={
            "full_name": "Invalid Blood",
            "email": "invalid@example.com",
            "blood_type": "X+"
        },
    )
    assert response.status_code == 422 # Pydantic validation error
