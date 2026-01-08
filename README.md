## Tech Stack
- Frontend: React + TypeScript + Vite, React Router, TanStack Query
- Backend: FastAPI + SQLModel (PostgreSQL), Pydantic
- Database: Postgresql
- Local/VPS: Docker + docker-compose
- API prefix: `/api/v1`

## Key MVP Features
- Home (`/`) shows “Latest Runs” cards (includes **place** here only).
- HSR (`/hsr`) shows leaderboard by mode. **No place/rank column** in leaderboard table.
- Expandable leaderboard rows fetch nested team rows **on-demand**.
- Roles concept exists (admin/moderator/user) but **auth is NOT implemented** (UI placeholders only).
- Mode-specific metrics:
  - cycles mode stores **cycles:number**
  - time mode stores **timeMs:number**
  - never store both on one entry

## Run with Docker (recommended)
From repo root:

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (OpenAPI at /docs)
- Postgresql: 

### Seeding
The backend auto-seeds on startup when `ACETARIA_AUTO_SEED=1` (default in compose).
You can also run seeding manually (inside the backend container):

```bash
docker exec -it acetaria_backend python -m app.seed
```

## Run in Dev Mode (without Docker)
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
python -m app.seed
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev -- --host 0.0.0.0 --port 5173
```

## API Endpoints (MVP)

### Meta
- GET `/api/v1/meta/languages`

### Topbar / Global
- GET `/api/v1/challenges?page=1&pageSize=20`
- GET `/api/v1/forums?page=1&pageSize=20`
- GET `/api/v1/help`
- GET `/api/v1/search?q=...&page=1&pageSize=20`

Auth placeholders (no real auth yet):
- POST `/api/v1/auth/login`
- POST `/api/v1/auth/signup`

### Games / Modes
- GET `/api/v1/games`
- GET `/api/v1/games/{gameSlug}/modes`

### Home / Runs
- GET `/api/v1/runs/latest?limit=10`
- POST `/api/v1/runs/submit` (placeholder success)

### Leaderboards
- GET `/api/v1/games/{gameSlug}/leaderboards?mode={modeSlug}&page=1&pageSize=50`
- GET `/api/v1/leaderboard-entries/{entryId}/teams?page=1&pageSize=20`

Leaderboard UI helpers (placeholders):
- GET `/api/v1/games/{gameSlug}/leaderboards/filters?mode={modeSlug}`

### HSR Tabs (dummy API-backed content)
- GET `/api/v1/games/hsr/news?page=1&pageSize=20`
- GET `/api/v1/games/hsr/guides?page=1&pageSize=20`
- GET `/api/v1/games/hsr/resources?page=1&pageSize=20`
- GET `/api/v1/games/hsr/streams?page=1&pageSize=20`
- GET `/api/v1/games/hsr/stats?mode={modeSlug}`

Admin (dummy success responses):
- POST `/api/v1/admin/runs`
- PATCH `/api/v1/admin/runs/{runId}`
- POST `/api/v1/admin/leaderboard-entries`
- PATCH `/api/v1/admin/leaderboard-entries/{entryId}`
- POST `/api/v1/admin/leaderboard-entries/{entryId}/teams`
- PATCH `/api/v1/admin/team-entries/{teamEntryId}`

