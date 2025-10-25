from app.services.loan_service import calculate_monthly_payment

def test_basic_amortization():
    amount = 10000
    annual_rate = 5.0
    term_months = 12
    monthly = calculate_monthly_payment(amount, annual_rate, term_months)

    r = annual_rate / 12 / 100
    n = term_months
    expected = amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    expected = round(expected, 2)

    assert monthly == expected

def test_zero_interest():
    amount = 1200
    annual_rate = 0.0
    term_months = 12
    monthly = calculate_monthly_payment(amount, annual_rate, term_months)

    expected = round(amount / term_months, 2)
    assert monthly == expected

def test_large_loan():
    amount = 1_000_000
    annual_rate = 3.5
    term_months = 360  # 30 years
    monthly = calculate_monthly_payment(amount, annual_rate, term_months)

    r = annual_rate / 12 / 100
    n = term_months
    expected = round(amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1), 2)
    assert monthly == expected

def test_short_term_loan():
    amount = 500
    annual_rate = 12
    term_months = 1
    monthly = calculate_monthly_payment(amount, annual_rate, term_months)

    r = annual_rate / 12 / 100
    n = term_months
    expected = round(amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1), 2)
    assert monthly == expected