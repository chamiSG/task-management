# Tasks Management

A full-stack tasks management application: React SPA frontend, FastAPI backend, and MongoDB persistence. Supports running via Docker Compose or locally for development.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Client (browser)                             │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Frontend (React + Vite + Ant Design)                                    │
│  - SPA with React Router; auth via JWT in localStorage                   │
│  - In Docker: nginx serves static build and proxies /api/* to backend   │
│  - Local dev: Vite dev server with proxy /api → http://127.0.0.1:8000   │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ /api/v1/* (REST + Bearer token)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Backend (FastAPI)                                                       │
│  - REST API under /api/v1; JWT auth; request logging & correlation IDs   │
│  - Task CRUD, audit logging (background), health check                  │
│  - Motor (async MongoDB driver) with connection pooling                  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ mongodb://...
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  MongoDB 7                                                              │
│  - Database: tasks_management                                           │
│  - Collections: tasks (with indexes), audit_logs                         │
└─────────────────────────────────────────────────────────────────────────┘
```

- **Docker Compose:** All three components run in containers; frontend talks to backend via nginx proxy (`/api` → backend:8000); backend talks to MongoDB on the Docker network.
- **Local development:** Run MongoDB (local or Docker), backend (e.g. `uvicorn` from `backend/`), and frontend (`npm run dev` in `frontend/`). Frontend uses Vite’s proxy so `/api` hits the local backend.

---

## API Design

- **Base URL:** `/api/v1` (e.g. `http://localhost:8000/api/v1` when running backend locally, or `https://your-domain/api/v1` when frontend is served and proxied).
- **Authentication:** JWT Bearer. Obtain a token via `POST /api/v1/auth/login` with `{"username":"...","password":"..."}`. Send `Authorization: Bearer <token>` on all protected requests.
- **Content type:** JSON request/response bodies; `Content-Type: application/json`.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/auth/login` | No | Login; returns `{ "access_token": "...", "token_type": "bearer" }`. |
| `GET`  | `/health` | No | Health check; returns `{ "status": "ok", "service": "...", "environment": "..." }`. |
| `POST` | `/tasks` | Bearer | Create task. Body: `title`, `description` (optional), `status` (optional, default `todo`), `owner_id` (UUID). |
| `GET`  | `/tasks` | Bearer | List tasks. Query: `owner_id`, `status`, `limit` (default 50), `skip` (default 0). Returns `{ "items": [...], "total", "limit", "skip" }`. |
| `GET`  | `/tasks/{task_id}` | Bearer | Get one task by UUID. |
| `PUT`  | `/tasks/{task_id}` | Bearer | Update task (partial). Body: optional `title`, `description`, `status`. Valid status flow: `todo` → `in_progress` → `done`. |
| `DELETE` | `/tasks/{task_id}` | Bearer | Delete task. Returns 204. |

**Task model:** `id` (UUID), `title`, `description`, `status` (`todo` | `in_progress` | `done`), `owner_id` (UUID), `created_at`, `updated_at` (UTC). Create/update enforce status transitions and field lengths (e.g. title 1–200 chars).

**Docs:** When the backend is running, OpenAPI docs are at `/docs` and ReDoc at `/redoc`.

---

## Local Setup

### Prerequisites

- **MongoDB** (local install or Docker) on port 27017 (or adjust `backend/.env`).
- **Python 3.11+** (backend), **Node 18+** and npm (frontend).

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Create or edit backend/.env (see Environment variables above). Set MONGODB_URL and JWT_SECRET_KEY as needed.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: `http://localhost:8000`. Docs: `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

App: `http://localhost:3000`. Vite proxies `/api` to `http://127.0.0.1:8000`, so the SPA uses `/api/v1/...` and the backend serves it.

### Docker (all-in-one)

From the **repository root**:

```bash
cp .env.example .env
# Optional: set JWT_SECRET_KEY, DEMO_USERNAME, DEMO_PASSWORD in .env
docker compose up --build
```

- Frontend: `http://localhost:3000` (nginx; proxies `/api` to backend).
- Backend: `http://localhost:8000`.
- MongoDB: host port 27018 (container 27017). See `docker-compose.yml` and [DOCKER.md](DOCKER.md) if you hit port conflicts or permission issues.

---

## Environment Variables

### Root `.env` (Docker Compose)

Used when running `docker compose up`. Copy from `.env.example`.

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | Secret for signing JWTs (min 32 chars). | (required; example in `.env.example`) |
| `DEMO_USERNAME` | Demo login username. | `admin` |
| `DEMO_PASSWORD` | Demo login password (plaintext). | `admin` |
| `DEBUG` | Backend debug mode. | `false` |

MongoDB URL and database name for the stack are set in `docker-compose.yml` (`MONGODB_URL`, `MONGODB_DATABASE_NAME`).

### Backend `backend/.env` (local run)

Used when starting the backend **outside Docker** (e.g. `uvicorn` in `backend/`).

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name. | `Tasks Management API` |
| `DEBUG` | Debug mode / reload. | `false` |
| `ENVIRONMENT` | Environment label. | `development` |
| `HOST` | Bind address. | `0.0.0.0` |
| `PORT` | HTTP port. | `8000` |
| `API_V1_PREFIX` | API prefix. | `/api/v1` |
| `MONGODB_URL` | MongoDB connection URL. | `mongodb://localhost:27017` |
| `MONGODB_DATABASE_NAME` | Database name. | `tasks_management` |
| `MONGODB_MIN_POOL_SIZE` / `MONGODB_MAX_POOL_SIZE` | Connection pool. | `10` / `100` |
| `MONGODB_MAX_IDLE_TIME_MS` | Idle timeout (ms). | `30000` |
| `MONGODB_SERVER_SELECTION_TIMEOUT_MS` | Server selection timeout (ms). | `5000` |
| `JWT_SECRET_KEY` | JWT signing key (min 32 chars). | (must be set for auth) |
| `JWT_ALGORITHM` | JWT algorithm. | `HS256` |
| `ACCESS_TOKEN_EXPIRES_MINUTES` | Token TTL. | `60` |
| `DEMO_USERNAME` / `DEMO_PASSWORD` | Demo credentials. | `admin` / `admin` |

### Frontend (optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | API base URL for fetch (empty = relative `/api`). | `` |

For local dev with Vite proxy, leave empty. For a separate backend origin, set e.g. `http://localhost:8000`. In Docker, the built app uses relative `/api`, which nginx proxies to the backend.

---

## Future Improvements

- **Auth & users:** Replace single demo user with a real user store (DB table or external IdP), registration, password reset, and optional OAuth2/OIDC.
- **Authorization:** Per-task or per-owner checks so users only access their own tasks (or shared tasks) instead of listing all.
- **Pagination & filtering:** Cursor-based or keyset pagination for large lists; full-text search on title/description.
- **Rate limiting & security:** Per-IP or per-user rate limits, CORS locked down per environment, and security headers (CSP, HSTS).
- **Observability:** Structured logs to a central sink; metrics (e.g. request latency, error rate); distributed tracing for requests across frontend → nginx → backend → MongoDB.
- **Testing:** Backend unit/integration tests (e.g. pytest + TestClient); frontend tests (e.g. Vitest + React Testing Library); optional E2E (Playwright).
- **CI/CD:** Lint/test on PR; build and push images; deploy to staging/production with env-specific config.
- **Audit:** Expose audit log via API (with auth) and/or retention/archival policy.

---

## Trade-offs

| Area | Choice | Trade-off |
|------|--------|-----------|
| **Auth** | Single demo user via env (username/password). | Simple to run and demo; not suitable for production. No real user DB or RBAC. |
| **API** | REST, JSON, JWT in header. | Familiar and tool-friendly; no built-in refresh tokens or session revocation. |
| **Data** | MongoDB with Motor (async). | Flexible schema and pooling; no SQL-style transactions or relational constraints. |
| **Frontend** | SPA, Ant Design, React Query. | Fast UX and rich components; SEO and no-JS support limited. |
| **Deploy** | Docker Compose (single host). | Easy to run and reason about; not a clustered or multi-region setup. |
| **Config** | Env vars + pydantic-settings. | Clear and 12-factor; secrets in env need to be managed (e.g. vault or platform secrets). |
| **Logging** | Structlog, correlation ID middleware. | Good for debugging and parsing; no built-in aggregation or alerting. |
