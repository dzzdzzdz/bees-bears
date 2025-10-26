import pytest

@pytest.mark.parametrize("page_size", [5, 10])
def test_customers_first_page(client, auth_headers, page_size):
    response = client.get(f"/customers?limit={page_size}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) <= page_size
    assert "next_cursor" in data

def test_customers_second_page(client, auth_headers, seeded_customers):
    # first page
    first_response = client.get("/customers?limit=5", headers=auth_headers)
    assert first_response.status_code == 200
    first_data = first_response.json()
    next_cursor = first_data.get("next_cursor")
    assert next_cursor is not None

    # second page using next_cursor
    second_response = client.get(f"/customers?limit=5&cursor={next_cursor}", headers=auth_headers)
    assert second_response.status_code == 200
    second_data = second_response.json()
    assert "data" in second_data
    assert len(second_data["data"]) <= 5

def test_customers_limit_enforcement(client, auth_headers, seeded_customers):
    # request a large limit
    response = client.get("/customers?limit=1000", headers=auth_headers)
    assert response.status_code == 422

def test_customers_next_cursor(client, auth_headers, seeded_customers):
    response = client.get("/customers?limit=3", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    next_cursor = data.get("next_cursor")
    assert next_cursor is not None

    # use next_cursor to get next page
    next_response = client.get(f"/customers?limit=3&cursor={next_cursor}", headers=auth_headers)
    assert next_response.status_code == 200
    next_data = next_response.json()
    assert "data" in next_data

def test_customers_no_overlap_between_pages(client, auth_headers, seeded_customers):
    # Get first page
    first_response = client.get("/customers?limit=5", headers=auth_headers)
    first_data = first_response.json()
    first_customers = first_data["data"]
    next_cursor = first_data.get("next_cursor")
    assert next_cursor is not None

    # Get second page
    second_response = client.get(f"/customers?limit=5&cursor={next_cursor}", headers=auth_headers)
    second_data = second_response.json()
    second_customers = second_data["data"]

    # Check no overlap in customer ids
    first_ids = {c["id"] for c in first_customers}
    second_ids = {c["id"] for c in second_customers}
    assert first_ids.isdisjoint(second_ids)