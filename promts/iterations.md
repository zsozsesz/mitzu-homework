# Iterations and Decision Log

This document captures the key decisions made during development, including tradeoffs, alternatives considered, and how the implementation evolved.

---

## 1. Backend Framework Choice (FastAPI)

### Decision

Chose FastAPI for the backend.

### Reasoning

- Built-in support for response modeling
- Automatic API documentation (OpenAPI)
- Clean and minimal syntax for defining endpoints
- Strong fit for small JSON-based APIs

### Alternative Considered

- Flask

### Tradeoff

- FastAPI introduces slightly more structure
- Flask would be simpler but requires more manual handling

### Outcome

FastAPI allowed faster development of well-structured endpoints with minimal boilerplate.

---

## 2. Frontend Choice (React)

### Decision

Chose React with TypeScript for the frontend.

### Reasoning

- Existing familiarity → faster development
- Component-based structure fits dashboard UI well
- Easy integration with REST APIs

### Alternative Considered

- Streamlit (single-layer app)

### Tradeoff

- React + FastAPI introduces more setup
- Streamlit would be faster but less representative of real-world architecture

### Outcome

Chose React to better demonstrate full-stack separation and frontend skills.

---

## 3. In-Memory Processing vs Database

### Decision

Used pandas with in-memory data instead of a database.

### Reasoning

- Dataset is small enough to fit in memory
- Avoids schema design and database setup
- Reduces development time significantly

### Alternative Considered

- PostgreSQL or other database

### Tradeoff

- Not scalable for large datasets
- No persistence layer

### Outcome

Simplified implementation and kept focus on data analysis and API design.

---

## 4. Dataset Scope Reduction

### Decision

Used a small subset of the NYC Taxi dataset.

### Reasoning

- Full dataset is too large for quick iteration
- Faster loading and processing
- Better fit for local development

### Tradeoff

- Results are less comprehensive
- Some patterns may not fully represent real-world data

### Outcome

Improved development speed and responsiveness.

---

## 5. Data Preprocessing Strategy

### Decision

Performed minimal preprocessing at application startup.

### Steps

- parsed datetime
- derived hour and date
- filtered invalid rows
- computed fare_per_mile

### Alternative Considered

- preprocessing on each request
- building a preprocessing pipeline

### Tradeoff

- higher memory usage
- data not dynamically updated

### Outcome

Simpler endpoint logic and faster response times.

---

## 6. API Design (Aggregated Endpoints)

### Decision

Returned aggregated data instead of raw datasets.

### Reasoning

- smaller payloads
- faster frontend rendering
- easier to visualize

### Alternative Considered

- returning full raw data

### Tradeoff

- less flexibility on frontend
- limits custom filtering

### Outcome

Cleaner API and better performance for this use case.

---

## 7. Frontend Scope Simplification

### Decision

Built a single dashboard page.

### Reasoning

- limited time (2 hours)
- focus on core functionality

### Alternative Considered

- multiple pages
- advanced filters

### Tradeoff

- reduced feature set
- simpler UX

### Outcome

Delivered a complete and usable UI within time constraints.

---

## 8. Avoiding Overengineering

### Decision

Explicitly avoided:

- authentication
- background jobs
- complex architecture
- real-time updates

### Reasoning

- not required for assignment
- would reduce focus on core problem

### Outcome

Maintained a small, understandable codebase.

---

## 9. AI Usage Iterations

### Initial Approach

- Generated initial structure and API design using AI

### Adjustments

- Simplified overly complex suggestions
- Removed unnecessary abstractions
- Reduced scope of data processing

### Key Learning

AI tends to:

- overengineer by default
- add unnecessary layers

### Correction Strategy

- explicitly constrained scope in prompts
- focused on minimal viable solution

---

## 10. Project Structure Refinement

### Initial Idea

- loosely structured files

### Adjustment

- introduced separation:
  - data loading
  - API layer
  - frontend components

- kept everything in a **single repository** instead of splitting into backend and frontend repos

### Reasoning

- simpler setup for reviewers (single clone, single README)
- easier to run locally without coordinating multiple repos
- faster development within time constraints
- sufficient separation achieved via folder structure

### Alternative Considered

- separate repositories for backend and frontend

### Tradeoff

- less realistic for large-scale production systems
- shared versioning instead of independent deployments

### Outcome

Improved clarity without adding complexity, while keeping the project easy to run and review.

---

## 11. Data Loading on Application Bootstrap

### Decision

Moved Parquet file loading from lazy (first request) to eager (application startup) using FastAPI's `lifespan` hook.

### Reasoning

- the first HTTP request would otherwise block while reading and cleaning the full dataset
- fail-fast behaviour: if the parquet file is missing the server errors immediately on boot rather than surfacing a 503 on the first user request
- consistent with how the preprocessing was already described (section 5)

### Implementation

Used FastAPI's `@asynccontextmanager lifespan` pattern:

```python
@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_data()  # eagerly load and cache on startup
    yield

app = FastAPI(lifespan=lifespan)
```

### Alternative Considered

- lazy loading on first request (original approach)

### Tradeoff

- server start takes slightly longer (dataset load time)
- no requests are served until data is ready

### Outcome

Eliminated cold-start latency on the first request and made startup failures immediately visible.

---

## Summary

The main guiding principle throughout development was:

> maximize clarity and completeness within strict time constraints, while avoiding unnecessary complexity.

Key patterns:

- prefer simple over scalable
- prefer complete over feature-rich
- prefer explicit over abstract
