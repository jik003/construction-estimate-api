# Job Estimate & Management API

A backend for a one-person general construction business (construction, design, electrical, roofing,
repair, interior, woodworking): customers, jobs, estimates, and job status workflow — with an
automated API test suite.

**Stack:** FastAPI · SQLite · pytest + requests · Postman · GitHub Actions

> Week 1 of 4 — customers & jobs CRUD. See [docs/DESIGN.md](docs/DESIGN.md) for the data model and roadmap.

## Run locally

```bash
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

## Test strategy

_(Week 4: describe how cases are split into happy path / negative / edge / regression, and list bugs found.)_
