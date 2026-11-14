# Construction Estimate & Management API

![tests](https://github.com/jik003/construction-estimate-api/actions/workflows/tests.yml/badge.svg)

A backend for a one-person general construction business (construction, design, electrical, roofing,
repair, interior, woodworking): customers, jobs, estimates, and job status workflow — with an
automated API test suite.

**Stack:** FastAPI · SQLite · pytest + requests · Postman · GitHub Actions

> Week 1 of 4 — customers & jobs CRUD. See [docs/DESIGN.md](docs/DESIGN.md) for the data model and roadmap.

## Run locally

```bash
git clone https://github.com/jik003/construction-estimate-api.git
cd construction-estimate-api

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload      # API docs at http://127.0.0.1:8000/docs
```

## Run tests

In a second terminal (server must be running):

```bash
pytest -v
```

Use `BASE_URL=http://host:port pytest` to test another environment.

## Run the Postman collection

1. In Postman, **Import** both files in [`postman/`](postman/).
2. Select the **local** environment (`base_url` = `http://127.0.0.1:8000`).
3. With the server running, right-click the **Customers** folder → **Run**.

## CI

GitHub Actions ([`.github/workflows/tests.yml`](.github/workflows/tests.yml)) runs on every push to `main`
and every pull request: it starts the API server, waits for `/health`, then runs `pytest -v`.

## Troubleshooting notes

| Problem | Cause | Fix |
|---------|-------|-----|

## Test strategy

_(Week 4: describe how cases are split into happy path / negative / edge / regression, and list bugs found.)_

## Bugs found

| # | Endpoint | Steps | Expected | Actual | Severity | Status |
|---|----------|-------|----------|--------|----------|--------|
