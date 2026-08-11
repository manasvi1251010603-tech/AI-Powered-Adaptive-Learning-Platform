# AI-Powered Adaptive Learning Platform Backend

This is the FastAPI backend foundation for the AI-Powered Adaptive Learning Platform. It currently includes only the base application, environment configuration, PostgreSQL connection setup, Alembic migration setup, CORS for local frontend development, basic error handling, logging, and health checks.

Future product features such as authentication, learner profiles, assessments, knowledge graph logic, AI tutor, recommendations, video processing, analytics, and billing are intentionally not implemented yet.

## 1. Create the Python environment

From the `backend` folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Python 3.12 is not installed, install Python 3.12 or newer, then run the commands again.

## 2. Install dependencies

```powershell
py -m pip install -e ".[dev]"
```

## 3. Configure environment variables

Copy the example file:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and set values for your local environment. Do not commit real secrets.

For PostgreSQL, use a URL like:

```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/adaptive_learning
```

If `DATABASE_URL` is empty, `/ready` will report the database as `not_configured` and still return `ready` because no database dependency has been configured yet.

## 4. Run the FastAPI server

```powershell
py -m uvicorn app.main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

## 5. Check health

Open this URL or call it with PowerShell:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing
```

Expected JSON:

```json
{"status":"ok"}
```

Check readiness:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/ready -UseBasicParsing
```

## 6. Run tests

```powershell
py -m pytest
```

## 7. Run Alembic

Check the current migration state:

```powershell
py -m alembic current
```

Create a future migration after models exist:

```powershell
py -m alembic revision --autogenerate -m "create initial tables"
```

Apply migrations:

```powershell
py -m alembic upgrade head
```

No application tables or migrations are included yet because the foundation task intentionally avoids future feature models.
