def test_create_loan_offer(client, auth_headers):
    customer = client.post("/customers", json={
        "name": "Bob Example",
        "email": "bob@example.com"
    }, headers=auth_headers).json()
    customer_id = customer["id"]

    response = client.post("/loanoffers", json={
        "customer_id": customer_id,
        "loan_amount": 10000,
        "interest_rate": 5.0,
        "term_months": 12
    }, headers=auth_headers)
    assert response.status_code == 201
    loan = response.json()
    assert loan["monthly_payment"] == 856.07

def test_create_loan_offer_invalid_customer(client, auth_headers):
    response = client.post("/loanoffers", json={
        "customer_id": 999999,
        "loan_amount": 5000,
        "interest_rate": 5.0,
        "term_months": 12
    }, headers=auth_headers)
    assert response.status_code == 400
    assert "Customer does not exist" in response.json()["detail"]

def test_create_loan_offer_invalid_amount(client, auth_headers):
    customer = client.post("/customers", json={
        "name": "Alice Example",
        "email": "alice@example.com"
    }, headers=auth_headers).json()
    customer_id = customer["id"]

    response = client.post("/loanoffers", json={
        "customer_id": customer_id,
        "loan_amount": -1000,
        "interest_rate": 5.0,
        "term_months": 12
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_loan_offer_invalid_interest(client, auth_headers):
    customer = client.post("/customers", json={
        "name": "Charlie Example",
        "email": "charlie@example.com"
    }, headers=auth_headers).json()
    customer_id = customer["id"]

    response = client.post("/loanoffers", json={
        "customer_id": customer_id,
        "loan_amount": 1000,
        "interest_rate": "five",
        "term_months": 12
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_loan_offer_invalid_term(client, auth_headers):
    customer = client.post("/customers", json={
        "name": "Diana Example",
        "email": "diana@example.com"
    }, headers=auth_headers).json()
    customer_id = customer["id"]

    response = client.post("/loanoffers", json={
        "customer_id": customer_id,
        "loan_amount": 5000,
        "interest_rate": 5.0,
        "term_months": 0
    }, headers=auth_headers)
    assert response.status_code == 422

def test_create_loan_offer_no_auth(client):
    response = client.post("/loanoffers", json={
        "customer_id": 1,
        "loan_amount": 1000,
        "interest_rate": 5.0,
        "term_months": 12
    })
    assert response.status_code == 401

def test_get_loan_offer_no_auth(client):
    response = client.get("/loanoffers/1")
    assert response.status_code == 401

def test_get_loan_offer_not_found(client, auth_headers):
    response = client.get("/loanoffers/999999", headers=auth_headers)
    assert response.status_code == 404