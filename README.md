# NYC Taxi Dashboard

A minimal full-stack analytics dashboard over the NYC Yellow Taxi dataset.

## Stack

| Layer    | Technology                          |
| -------- | ----------------------------------- |
| Backend  | Python 3.12, FastAPI, pandas        |
| Frontend | React 18, TypeScript, Vite          |
| Charts   | Recharts                            |
| Data     | Parquet file, in-memory DataFrame   |
| Linting  | ruff (backend), ESLint (frontend)   |
| Testing  | pytest (backend), Vitest (frontend) |

## Architecture

```
Browser → React SPA (Vite / nginx)
              ↓  HTTP (CORS)
         FastAPI backend
              ↓
         pandas DataFrame (in-memory)
              ↓
         .parquet file (local disk)
```

The Parquet file is loaded once on the first request, cleaned, and held in memory for the lifetime of the process. No database is used.

---

## Setup

### 1. Download the dataset

Download a NYC Yellow Taxi monthly Parquet file and place it in the `data/` directory:

```bash
curl -L -o data/yellow_tripdata_2024-01.parquet \
  https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API available at <http://localhost:8000>.  
Interactive docs at <http://localhost:8000/docs>.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard available at <http://localhost:5173>.

---

## Running Tests

### Backend

```bash
cd backend
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

### Frontend

```bash
cd frontend
npm test
```

---

## Linting

### Backend

```bash
cd backend
ruff check .          # lint
ruff format --check . # format check
ruff format .         # auto-format
```

### Frontend

```bash
cd frontend
npm run lint
```

---

## Docker (local)

```bash
docker-compose up --build
```

- Backend: <http://localhost:8000>
- Frontend: <http://localhost:3000>

> Ensure `data/*.parquet` is present before starting.

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app & route handlers
│   │   ├── data_loader.py     # Parquet loading, cleaning, in-memory cache
│   │   ├── schemas.py         # Pydantic response models
│   │   └── services/
│   │       └── analytics.py   # Aggregation / query functions
│   ├── tests/
│   │   ├── test_analytics.py  # Unit tests for analytics logic
│   │   └── test_api.py        # API smoke tests
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pyproject.toml         # ruff & pytest config
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/client.ts      # Typed fetch wrapper
│   │   ├── components/        # Individual chart components
│   │   ├── pages/Dashboard.tsx
│   │   ├── test/              # Vitest + React Testing Library tests
│   │   └── types/index.ts     # Shared TypeScript interfaces
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── data/                      # Place .parquet file here
├── docker-compose.yml
├── .github/workflows/ci.yml
└── README.md
```

---

## API Endpoints

| Method | Path                | Description                              |
| ------ | ------------------- | ---------------------------------------- |
| GET    | `/summary`          | Total trips, avg fare, distance, fare/mi |
| GET    | `/trips-over-time`  | Daily trip counts                        |
| GET    | `/fare-vs-distance` | 500-point sample for scatter chart       |
| GET    | `/top-zones`        | Top 10 pickup zones by trip count        |
| GET    | `/top-vendors`      | Trip counts per vendor                   |

---

## Design Decisions

- **In-memory storage** — the DataFrame is loaded once and cached globally. Avoids all database complexity; acceptable for a read-only prototype over a single monthly file (~100 MB).
- **Scatter sampling** — `/fare-vs-distance` returns 500 random rows (seeded) to keep payload small while preserving the visual distribution.
- **Outlier filtering** — rows with `fare_amount <= 0`, `trip_distance <= 0`, `fare_amount >= 500`, or `trip_distance >= 100` are dropped during the cleaning step, which removes erroneous entries common in the raw TLC data.
- **No auth / no DB** — explicitly out of scope per the spec.
