Frontend skeleton (Vue 3 + TypeScript + Vite) that connects to the API at http://localhost:8000/api.

To run frontend:

cd frontend
npm install
npm run dev

Notes:
- The CarsListView expects backend endpoint GET /api/cars to return JSON { cars: [ ... ] }.
- Adjust baseURL in src/api/axios.ts if your backend is mounted under /api/v1 or another path.
