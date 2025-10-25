import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user(client):
    """Create a dummy user only once per test session."""
    user_data = {
        "email": "dummy@example.com",
        "password": "password123",
        "full_name": "Dummy User"
    }
    client.post("/auth/register", json=user_data)
    return user_data

@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    """Return auth headers with JWT for the dummy user."""
    resp = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}