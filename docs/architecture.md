# Architecture Overview

This document describes the system architecture, key design decisions, and tradeoffs for the NYC Taxi dashboard application.

## Goals

The architecture is designed to:

- remain simple and easy to understand
- support rapid development within a limited timeframe (~1–2 hours)
- demonstrate clear separation between frontend and backend
- avoid unnecessary infrastructure and overengineering
- focus on data insights rather than system complexity

---

## High-Level Architecture

The system follows a simple full-stack architecture:

Frontend (React)
        ↓
Backend API (FastAPI)
        ↓
In-memory dataset (pandas)

### Components

- Frontend: React + TypeScript dashboard
- Backend: FastAPI service exposing REST endpoints
- Data Layer: Parquet file loaded into memory and processed using pandas

---

## Data Flow

1. The backend loads the dataset at application startup
2. Data is preprocessed and stored in memory
3. The frontend sends requests to backend API endpoints
4. The backend computes or retrieves aggregated metrics
5. The frontend renders charts and summary components

---

## Backend Architecture

The backend is intentionally structured in a minimal and clear way:

backend/
├── app/
│   ├── main.py
│   ├── data_loader.py
│   ├── schemas.py
│   └── services/
│       └── analytics.py

### Design Principles

- separation of concerns (loading vs processing vs API)
- minimal abstraction
- readability over flexibility

### API Design

- /summary
- /trips-over-time
- /fare-vs-distance
- /top-zones
- /top-vendors

---

## Frontend Architecture

frontend/
├── src/
│   ├── api/
│   ├── components/
│   ├── pages/
│   └── types/

### Design Principles

- single-page dashboard
- component-based UI
- minimal state management
- direct consumption of backend APIs

---

## Data Handling Strategy

### Approach

- dataset stored as a local Parquet file
- loaded and preprocessed at application startup
- stored in memory using pandas

### Preprocessing Steps

- parse datetime fields
- derive hour and date
- filter invalid rows
- compute derived metrics (e.g. fare per mile)

---

## Key Design Decisions and Tradeoffs

### FastAPI vs Flask

Decision: FastAPI  
Reasoning:
- built-in validation and type support
- automatic API documentation

Tradeoff:
- slightly more structured than Flask

---

### React vs Streamlit

Decision: React + TypeScript  
Reasoning:
- better separation of frontend and backend
- more realistic architecture

Tradeoff:
- more setup

---

### In-Memory Processing vs Database

Decision: in-memory processing  
Reasoning:
- small dataset
- no persistence needed

Tradeoff:
- not scalable
- repeated loading on startup

---

### Preprocessing Strategy

Decision: preprocess at startup  
Reasoning:
- simpler request handling
- faster API responses

Tradeoff:
- increased startup time
- duplicated preprocessing across instances
- higher memory usage

---

## Summary

The architecture prioritizes:

- simplicity over scalability
- clarity over completeness
- fast implementation over infrastructure complexity
