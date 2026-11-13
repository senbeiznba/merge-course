# Course Catalog API (Lab 8: FastAPI, Strawberry GraphQL & SQLAlchemy)

Backend application implementing both a REST API and a Code-First GraphQL API using **FastAPI**, **Strawberry**, and **SQLAlchemy**. Optimized for N+1 query elimination via `DataLoader` and compliant with RFC 9457 Problem Details for error handling.

---

## Features

- **Dual Interface:** REST endpoints and a Strawberry GraphQL endpoint (`/graphql`).
- **N+1 Optimization:** Uses 4 custom `DataLoader` instances to fetch enrollments and students efficiently, reducing complex queries to just **3 SQL queries**.
- **Error Handling (RFC 9457):** Standardized `application/problem+json` responses for both business errors (`ServiceError`) and Pydantic validation errors (`RequestValidationError`).
- **Bonus Tasks Implemented:**
  - **Bonus 1:** Problem Details transformation for validation errors.
  - **Bonus 2:** Shared business-layer validation in `services.py` (`INVALID_NAME` check) utilized by both REST and GraphQL mutations (`createStudent`).

---

## Project Structure

- `main.py` — FastAPI application entry point, mounts REST routers and GraphQL app.
- `graphql_api.py` — Strawberry GraphQL schema, queries, mutations, and `DataLoader` context setup.
- `services.py` — Isolated business logic and service-level validations (`create_student`, `enroll`, `like_course`).
- `problem.py` — RFC 9457 error handlers (`ServiceError`, `RequestValidationError`, HTTP exceptions).
- `models.py` — SQLAlchemy database models (`Course`, `Student`, `Enrollment`).
- `try_n_plus_1.py` — Benchmark script verifying N+1 query resolution (checks `x-sql-queries` or query counts).

---

## Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt




