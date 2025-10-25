# Bees & Bears Backend Assingment

This is my submission for the Bees & Bears Backend Bonanza

## Features

- **User Authentication**: JWT-based authentication system with registration and login
- **Customer Management**: Create and retrieve customer information
- **Loan Offer Management**: Create and retrieve loan offers with automatic monthly payment calculation
- **Loan Amortization**: Standard loan amortization formula implementation
- **Input Validation**: Comprehensive validation for all API endpoints
- **Testing**: Full test coverage including unit tests and integration tests

## Technology Stack

- **Framework**: FastAPI - Modern, fast web framework for building APIs with Python
- **Database**: SQLAlchemy with SQLite - ORM for database operations
- **Authentication**: JWT tokens with PassLib for password hashing
- **Validation**: Pydantic for request/response validation
- **Testing**: Pytest with FastAPI TestClient
- **Documentation**: Automatic OpenAPI/Swagger documentation

### Design Choices

- **FastAPI**: Chosen for its automatic API documentation, type hints support, and excellent performance
- **SQLAlchemy**: Provides robust ORM capabilities with relationship management
- **SQLite**: Simple file-based database for easy setup and development
- **JWT Authentication**: Stateless authentication suitable for API services
- **Pydantic Models**: Type-safe data validation and serialization

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Authenticate user and receive JWT token

### Customers

- `POST /customers` - Create a new customer (requires authentication)
- `GET /customers/{id}` - Retrieve customer details (requires authentication)

### Loan Offers

- `POST /loanoffers` - Create a loan offer for a customer (requires authentication)
- `GET /loanoffers/{id}` - Retrieve a loan offer (requires authentication)

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/dzzdzzdz/bees-bears.git
   cd bees-bears
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive API Documentation: `http://localhost:8000/docs`
   - Alternative Documentation: `http://localhost:8000/redoc`

## Usage Examples

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "installer@example.com",
    "password": "securepassword123",
    "full_name": "John Installer"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "installer@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create a Customer

```bash
curl -X POST "http://localhost:8000/customers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Jane Customer",
    "email": "jane@example.com",
    "phone_number": "+1234567890"
  }'
```

### 4. Create a Loan Offer

```bash
curl -X POST "http://localhost:8000/loanoffers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "customer_id": 1,
    "loan_amount": 25000.00,
    "interest_rate": 4.5,
    "term_months": 240
  }'
```

## Loan Amortization Logic

The system implements the standard loan amortization formula:

```
M = P * [r(1 + r)^n] / [(1 + r)^n - 1]
```

Where:

- M = Monthly payment
- P = Principal loan amount
- r = Monthly interest rate (annual rate / 12 / 100)
- n = Number of payments (term in months)

### Special Cases

- **Zero Interest**: When interest rate is 0%, monthly payment = principal / number of months
- **Input Validation**: Ensures positive loan amounts, non-negative interest rates, and positive terms

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_amortization.py

# Run with coverage
pytest --cov=app
```

### Test Coverage

The test suite includes:

- **Unit Tests**: Loan amortization calculations with various scenarios
- **Integration Tests**: Full API endpoint testing
- **Authentication Tests**: User registration and login flows
- **Customer Management Tests**: CRUD operations for customers
- **Loan Offer Tests**: Creation and retrieval of loan offers
- **Error Handling Tests**: Validation and error response testing

### Test Categories

- `test_amortization.py` - Loan calculation logic tests
- `test_auth.py` - Authentication flow tests
- `test_customers.py` - Customer management tests
- `test_loanoffers.py` - Loan offer management tests

## Project Structure

```
bees&bears/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database configuration
│   ├── models/                 # SQLAlchemy models
│   │   ├── customer.py
│   │   ├── loanoffer.py
│   │   └── user.py
│   ├── repositories/           # Data access layer
│   │   ├── customer_repo.py
│   │   ├── loanoffer_repo.py
│   │   └── user_repo.py
│   ├── routes/                 # API route handlers
│   │   ├── auth_routes.py
│   │   ├── customer_routes.py
│   │   └── loanoffer_routes.py
│   ├── schemas/               # Pydantic models for validation
│   │   ├── customer.py
│   │   ├── loanoffer.py
│   │   └── user.py
│   ├── services/              # Business logic layer
│   │   ├── auth_service.py
│   │   ├── customer_service.py
│   │   └── loan_service.py
│   └── utils.py               # Utility functions
├── tests/                      # Test suite
│   ├── conftest.py            # Test configuration and fixtures
│   ├── test_amortization.py   # Loan calculation tests
│   ├── test_auth.py           # Authentication tests
│   ├── test_customers.py      # Customer management tests
│   └── test_loanoffers.py     # Loan offer tests
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data or validation errors
- **401 Unauthorized**: Missing or invalid authentication
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Pydantic validation errors

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Input Validation**: All inputs are validated using Pydantic models
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection attacks

## Development Notes

### Assumptions Made

- JWT tokens with 24-hour expiration
- Single user can create multiple customers and loan offers
- Loan amounts and interest rates are stored as floats (consider using Decimal for production)

### Out of Scope Enhancements

- Database migration system (Alembic)
- Rate limiting for API endpoints
- Comprehensive logging and monitoring
- Database connection pooling
- Environment-based configuration
- Docker containerization
