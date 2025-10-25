from datetime import datetime, timedelta, timezone
from jose import jwt
from app.services.auth_service import SECRET_KEY, ALGORITHM

def test_register_and_login(client):
    # registration
    response = client.post("/auth/register", json={
        "email": "testuser@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

    # login
    response = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_user(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "password123",
        "full_name": "Dupe User"
    }
    
    first = client.post("/auth/register", json=payload)
    assert first.status_code == 201
    dup = client.post("/auth/register", json=payload)
    assert dup.status_code in (400, 409)
    assert "detail" in dup.json()

def test_login_invalid_password(client, test_user):
    response = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "Invalid" in response.json()["detail"]

def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={
        "email": "ghost@example.com",
        "password": "fakenews"
    })
    assert response.status_code == 401
    assert "Invalid" in response.json()["detail"]

def test_register_missing_fields(client):
    response = client.post("/auth/register", json={
        "email": "missing@example.com"
    })
    assert response.status_code == 422

def test_register_invalid_email_format(client):
    response = client.post("/auth/register", json={
        "email": "not_email",
        "password": "password123",
        "full_name": "Not Email"
    })
    assert response.status_code == 422

def test_expired_token(client, test_user):
    payload = {"sub": str(1), "exp": datetime.now(tz=timezone.utc) - timedelta(minutes=1)}
    expired_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    headers = {"Authorization": f"Bearer {expired_token}"}

    response = client.get("/customers/1", headers=headers)
    assert response.status_code == 401
    assert "Could not validate" in response.json()["detail"]

def test_tampered_token(client, auth_headers):
    token = auth_headers["Authorization"].split()[1]
    parts = token.split(".")
    tampered_payload = parts[1][::-1]
    tampered_token = f"{parts[0]}.{tampered_payload}.{parts[2]}"
    headers = {"Authorization": f"Bearer {tampered_token}"}

    response = client.get("/customers/1", headers=headers)
    assert response.status_code == 401
    assert "Could not validate" in response.json()["detail"]