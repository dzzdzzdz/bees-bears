def test_create_and_get_customer(client, auth_headers):
    response = client.post("/customers", json={
        "name": "Alice Example",
        "email": "alice@example.com",
        "phone_number": "1245678"
    }, headers=auth_headers)
    assert response.status_code == 201
    customer = response.json()
    assert customer["name"] == "Alice Example"

    customer_id = customer["id"]
    response = client.get(f"/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 200

def test_create_customer_missing_fields(client, auth_headers):
    response = client.post("/customers", json={
        "email": "aoeu@example.com"
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_customer_invalid_email(client, auth_headers):
    response = client.post("/customers", json={
        "name": "Not Email",
        "email": "not_email"
    }, headers=auth_headers)
    assert response.status_code == 422

def test_get_customer_not_found(client, auth_headers):
    response = client.get("/customers/1")
    assert response.status_code == 401

def test_create_customer_duplicate_email(client, auth_headers):
    payload = {
        "name": "Htns",
        "email": "htns@example.com"
    }
    response1 = client.post("/customers", json=payload, headers=auth_headers)
    assert response1.status_code == 201
    response2 = client.post("/customers", json=payload, headers=auth_headers)
    assert response2.status_code == 400

def test_get_customer_other_user(client, auth_headers):
    customer = client.post("/customers", json={
        "name": "Other User Customer",
        "email": "otheruser@example.com"
    }, headers=auth_headers).json()
    customer_id = customer["id"]

    client.post("/auth/register", json={
        "email": "second@example.com",
        "password": "password123",
        "full_name": "Second User"
    })
    token2 = client.post("/auth/login", json={
        "email": "second@example.com",
        "password": "password123"
    }).json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Second user tries to access first user's customer
    response = client.get(f"/customers/{customer_id}", headers=headers2)
    assert response.status_code == 404

def test_get_customer_no_auth(client):
    response = client.get("/customers/1")
    assert response.status_code == 401

def test_get_customer_invalid_token(client):
    headers = {"Authorization": "Bearer invalid"}
    response = client.get("/customers/1", headers=headers)
    assert response.status_code == 401

def test_create_customer_empty_strings(client, auth_headers):
    response = client.post("/customers", json={
        "name": "",
        "email": "",
        "phone_number": ""
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_customer_long_strings(client, auth_headers):
    long_name = "a" * 300
    long_email = "a" * 250 + "@example.com"
    response = client.post("/customers", json={
        "name": long_name,
        "email": long_email
    }, headers=auth_headers)
    # Depending on your DB constraints, could be 422 or 400
    assert response.status_code in (422, 400)

def test_create_customer_extra_fields(client, auth_headers):
    response = client.post("/customers", json={
        "name": "Extra Fields",
        "email": "extrafields@example.com",
        "foo": "bar"
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert "foo" not in data

def test_create_customer_null_values(client, auth_headers):
    response = client.post("/customers", json={
        "name": "Null Values",
        "email": None,
        "phone_number": None
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_customer_wrong_types(client, auth_headers):
    response = client.post("/customers", json={
        "name": 123,
        "email": ["not", "a", "string"],
        "phone_number": 999999
    }, headers=auth_headers)
    assert response.status_code == 422