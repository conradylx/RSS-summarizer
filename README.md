# 📰 RSS Summarizer

A full-stack application that aggregates RSS feeds and generates AI-powered summaries in real time. Add any RSS source, and the app automatically fetches articles in the background, summarizes them using a local LLM, and pushes updates to the UI via WebSockets — no page refresh needed.

![Python](https://img.shields.io/badge/Python-3.14-red)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green)
![React](https://img.shields.io/badge/React-19-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-6.0-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

## ✨ Features

- **RSS aggregation** — add any RSS/Atom feed URL and articles are fetched automatically
- **AI summarization** — each article gets a 3-4 sentence summary via local Ollama (llama3.2:1b)
- **Real-time updates** — new articles pushed to the browser via WebSocket, no polling
- **Background processing** — Celery workers handle fetching and summarizing asynchronously
- **Scheduled sync** — Beat scheduler refreshes all feeds every 10 minutes automatically
- **Fully containerized** — one command to run everything locally

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, FastAPI, SQLAlchemy 2.0 (async) |
| Task Queue | Celery 5, Redis 7 |
| Database | PostgreSQL 17, Alembic (migrations) |
| Real-time | WebSockets, Redis Pub/Sub |
| Frontend | React 19, TypeScript, Vite, TailwindCSS |
| AI | Ollama (llama3.2:1b, local) |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions, GHCR, Trivy (security scan) |
| Testing | pytest, pytest-asyncio, httpx |

When a feed is added via the API, a Celery task immediately fetches and summarizes its articles. Beat scheduler re-runs all feeds every 10 minutes. New articles are published to a Redis channel and pushed to all connected WebSocket clients in real time.

##  Getting Started

### Prerequisites

- Docker & Docker Compose

### Run locally

```bash
git clone https://github.com/conradylx/RSS-summarizer.git
cd RSS-summarizer
cp .env.example .env   # fill in your values
docker compose up --build
```

> First run will take a few minutes — Ollama needs to pull the llama3.2:1b model (~1.3 GB).

The app will be available at:
- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API docs**: http://localhost:8000/docs

### Run database migrations

```bash
docker compose exec api alembic upgrade head
```

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
POSTGRES_USER=rss_user
POSTGRES_PASSWORD=rss_user
POSTGRES_DB=rss_user
DATABASE_URL=postgresql+asyncpg://rss_user:rss_user@postgres:5432/rss_user
REDIS_URL=redis://redis:6379/0
OLLAMA_URL=http://ollama:11434/v1
```

## 🧪 Running Tests

```bash
docker compose exec api pytest -v
```

Or locally:

```bash
cd backend
poetry install
poetry run pytest -v
```

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app, CORS, router registration
│   │   ├── config.py               # Pydantic settings from .env
│   │   ├── database.py             # Async SQLAlchemy engine and session
│   │   ├── models.py               # Feed and Article ORM models
│   │   ├── schemas.py              # Pydantic request/response schemas
│   │   ├── worker.py               # Celery app and beat schedule
│   │   ├── tasks.py                # fetch_feed and fetch_all_feeds tasks
│   │   ├── broadcast.py            # Redis Pub/Sub publish and subscribe
│   │   ├── celery_utils.py         # Celery helper utilities
│   │   ├── routers/
│   │   │   ├── feeds.py            # CRUD endpoints for feeds
│   │   │   ├── articles.py         # Read endpoints for articles
│   │   │   └── ws.py               # WebSocket endpoint
│   │   └── services/
│   │       └── summarizer.py       # Ollama/OpenAI summarization
│   ├── alembic/                    # Database migrations
│   └── tests/                      # pytest test suite
├── frontend/
│   └── src/
│       ├── App.tsx                 # Main UI component
│       ├── api.ts                  # REST API calls
│       ├── useWebsocket.ts         # WebSocket hook with auto-reconnect
│       └── types.ts                # TypeScript types
├── k8s/
│   ├── base/
│   │   ├── backend-deployment.yml  # Backend API deployment
│   │   ├── backend-service.yml     # Backend ClusterIP service
│   │   ├── beat.yml                # Celery Beat scheduler deployment
│   │   ├── configmap.yml           # Non-secret environment config
│   │   ├── frontend-deployment.yml # Frontend deployment
│   │   ├── frontend-service.yml    # Frontend ClusterIP service
│   │   ├── ingress.yml             # Ingress rules
│   │   ├── kustomization.yml       # Base Kustomize manifest list
│   │   ├── network-policies.yml    # Pod-to-pod traffic rules
│   │   ├── postgres-deployment.yml # PostgreSQL stateful deployment
│   │   ├── redis-deployment.yml    # Redis stateful deployment
│   │   ├── secrets-example.yml     # Secret template (commit-safe)
│   │   ├── secrets.yml             # Actual secrets (gitignored)
│   │   └── worker-deployment.yml   # Celery worker deployment
│   └── overlays/
│       ├── dev/
│       │   └── kustomization.yml   # Dev overrides (replicas, image tags)
│       └── prod/
│           └── kustomization.yml   # Prod overrides (replicas, resources)
├── monitoring/
│   ├── prometheus.yml              # Scrape targets and alerting rules
│   └── promtail.yml                # Log collection and Loki shipping
├── docker-compose.yml              # Development environment
├── docker-compose.prod.yml         # Production environment
└── .github/
    └── workflows/
        ├── ci.yml                  # Lint, test, security scan
        └── publish-images.yml      # Build and push to GHCR
```

##  Production Deployment

A production-ready compose file is included with resource limits and pinned image versions:

```bash
docker compose -f docker-compose.yml up -d
```

Images are automatically built and published to GitHub Container Registry on every push to `main`.

## 📄 License

MIT