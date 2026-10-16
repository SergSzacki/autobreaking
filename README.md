# AutoBreaking - Cars API (FastAPI)

This branch adds a minimal FastAPI CRUD API for a Car resource using SQLModel + SQLite.

Run locally:

1. Create a virtual environment and install dependencies:

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run the server:

   uvicorn app.main:app --reload

Endpoints:
- GET /api/cars?page=1&per_page=20&q=search
- GET /api/cars/{id}
- POST /api/cars
- PUT /api/cars/{id}
- PATCH /api/cars/{id}
- DELETE /api/cars/{id}

Example create payload:

{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2019,
  "vin": "JTDBU4EE9B9123456",
  "mileage": 45000,
  "color": "white",
  "status": "available"
}
