# AutoBreaking

FastAPI + SQLModel backend (PostgreSQL) and Vue 3 frontend for tracking cars and the parts/stock taken from them.

## Backend

1. Create a virtual environment and install dependencies:

       python -m venv .venv
       source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
       pip install -r requirements.txt

2. Copy `.env.example` to `.env` and set `SECRET_KEY` and the `POSTGRES_*` values
   (or a full `DATABASE_URL`).

3. Create/upgrade the database schema:

       alembic upgrade head

4. Run the server:

       uvicorn app.main:app --reload

On Windows, `launch.ps1` performs steps 1–4 and starts the frontend
(`launch.ps1 -GitSync` additionally pulls the current branch first).

## Frontend

    cd frontend
    npm install
    npm run dev

The API URL defaults to `http://localhost:8000/api`; override it with `VITE_API_URL`.

## Tests

    pip install -r requirements-dev.txt
    DATABASE_URL=sqlite:// pytest

## Endpoints

- `GET /api/cars?page=1&per_page=20&q=search`, `POST /api/cars`
- `GET|PUT|PATCH|DELETE /api/cars/{id}` (deleting a car keeps its parts, unlinked)
- `GET|POST /api/cars/{id}/parts`, `GET|PATCH|DELETE /api/cars/{id}/parts/{part_id}`
- `POST /api/parts`, `GET|PATCH|DELETE /api/parts/{id}` (parts with or without a car)
- `GET /api/inventory?q=search&car_id=1` — searches part name, SKU, category and car make/model

Duplicate VIN/SKU returns `409 Conflict`; validation errors return `422`.
