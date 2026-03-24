# Specification

## Goal

Build a minimal full-stack dashboard application using a subset of the NYC Taxi dataset.

The goal is to demonstrate:

- clear problem framing
- practical engineering tradeoffs
- effective AI-assisted development
- ability to deliver a working solution within ~2 hours

Focus is on simplicity, clarity, and decision-making — not feature completeness.

---

## Scope

The application consists of:

- Backend: Python (FastAPI)
- Frontend: React + TypeScript
- Data processing: pandas
- Data source: local Parquet file
- Storage: in-memory (no database)

The app provides a single dashboard page with summary metrics and charts.

---

## Project Structure

project-root/
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── data_loader.py
│ │ ├── schemas.py
│ │ └── services/
│ │ └── analytics.py
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ │ ├── api/
│ │ ├── components/
│ │ ├── pages/
│ │ ├── types/
│ │ ├── App.tsx
│ │ └── main.tsx
│ ├── package.json
│ └── vite.config.ts
│
├── data/
├── prompts/
├── docs/
├── README.md

---

## Dataset

Expected columns:

- tpep_pickup_datetime
- fare_amount
- trip_distance
- PULocationID
- VendorID

---

## Data Processing

- Parse datetime
- Derive hour and date
- Filter invalid rows
- Compute fare_per_mile

---

## Backend Endpoints

GET /summary  
GET /trips-over-time  
GET /fare-vs-distance  
GET /top-zones
GET /top-vendors

---

## Frontend

- Single dashboard page
- Summary cards
- Charts

---

## Non-Goals

- No database
- No authentication
- No real-time processing

---

## Tradeoffs

- In-memory vs database
- Small dataset vs full dataset
- Simplicity vs completeness

---

## README Scope

The README should include:

- project overview
- chosen stack
- setup instructions
- run instructions for backend and frontend
- how to run tests
- how to run linting
- project structure
- architecture summary

---

## CI Scope

Add one basic GitHub Actions workflow that:

- installs dependencies
- runs lint
- runs tests
- builds the frontend
- optionally verifies backend startup or importability

This should be a simple validation workflow only.

Not in scope:

- deployment pipeline
- release automation
- environment promotion
- infrastructure provisioning

---

## Linting Scope

Include lightweight linting/formatting for both backend and frontend.

Suggested direction:

- backend: formatter + linter
- frontend: ESLint or equivalent

The linting setup should be conventional and minimal. No heavy customization is needed.

---

## Testing Scope

Testing should remain intentionally small and focused.

### Backend tests

Include a few tests covering:

- transformation or aggregation logic
- one API smoke test

### Frontend tests

Include a minimal number of tests covering:

- basic render/smoke behavior for the dashboard or key UI component

The goal is to validate the most important paths, not to achieve broad coverage.

Not in scope:

- exhaustive unit coverage
- end-to-end browser automation
- contract testing
- performance testing

---

## Docker Scope

The project will include:

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml` only for local startup

Docker support should be straightforward and local-development focused.

Not in scope:

- Kubernetes
- production container orchestration
- image publishing
- advanced production hardening

---

## Success Criteria

- Working backend
- Functional dashboard
- Clear documentation
