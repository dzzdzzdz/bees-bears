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