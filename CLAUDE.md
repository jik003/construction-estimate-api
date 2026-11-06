# CLAUDE.md

## Project
Job Estimate & Management API: customers, jobs, estimates, and job status workflow for a one-person
general construction office (construction, design, electrical, roofing, repair, interior, woodworking).
It has two goals:
1. **Portfolio:** show API testing and test automation skills (pytest, requests, Postman, CI) for
   QA / Test Automation Engineer roles.
2. **Real use:** my father's office will actually use it within 3-4 years, so business rules must
   match how the office really works.

Stack: FastAPI, SQLite through the stdlib `sqlite3` module (raw SQL, no ORM), Pydantic v2, pytest + requests.
The source of truth for the data model, endpoints, status flow and roadmap is `docs/DESIGN.md`.

## My role vs. yours
I'm a QA engineer learning backend and test automation. The tests are what I'll be interviewed on.

**You do:**
- Implement and fix application code in `app/`
- Set up environments, dependencies, the CI workflow (`.github/workflows/`) and the Postman collection JSON
- Run the server and tests, read the failures, and explain the root cause
- Review my tests: point out missing cases (boundary, negative, edge, regression), weak assertions,
  flaky patterns and duplication
- Draft commit messages and PR descriptions

**You do NOT do unless I explicitly ask:**
- Write or edit test functions in `tests/`. Suggest them as a review list or a code block in chat
  instead, and I'll write them. Changes to `conftest.py` fixtures are fine if I agree first.
- Decide business rules (pricing, discount limits, VAT, travel fee, rounding, status transitions).
  If a rule is unclear, ask me. Don't guess, because these need to match the real office.
- Edit the "Bugs found" or "Test strategy" sections of README.md. I write those myself.

## Workflow rules
- If a change affects the data model, an endpoint or a business rule, update `docs/DESIGN.md` first,
  show me the diff, then implement it.
- After any change to `app/`, start the server if it isn't running and run `pytest -v`. Report:
  passed/failed counts, and for each failure, whether it is an **app bug** or a **test problem** and why.
- If a test fails because the app has a real bug, don't silently change the test to pass. Tell me first.
  It may belong in the "Bugs found" table.
- Keep changes small and focused on one feature. Don't refactor unrelated code.
- Never commit `*.db` files, `.env`, or secrets.

## Commands
```bash
source .venv/bin/activate                 # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload             # http://127.0.0.1:8000/docs
pytest -v                                 # server must be running
BASE_URL=http://host:port pytest -v       # another environment
```

## Code conventions
- Raw SQL with `?` placeholders only. Never build SQL from user input with f-strings.
  Column names in f-strings must come from validated Pydantic fields.
- Request models use `extra="forbid"`, so unknown fields return 422.
- Error codes: 404 when the resource is missing, 409 for a conflict with current state,
  422 for invalid input. Body: `{"detail": "..."}`.
- Money is integer KRW (원). No floats in stored amounts.
- Job `status` changes only through the status endpoint (week 3), never through PATCH.
- Timestamps are UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`). Dates are `YYYY-MM-DD`.

## Git
- One commit per feature or fix. Messages in English, imperative mood
  (e.g. "Add estimate total calculation").
- Ask before pushing, force-pushing, or changing branches.

## Language
Explain things to me in Korean. Write code, comments, commit messages and docs in English
(DESIGN.md may stay in Korean).
