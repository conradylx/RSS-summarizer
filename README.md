# 📰 RSS Summarizer
![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green)
![React](https://img.shields.io/badge/React-19-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-6.0-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)


A full-stack application that aggregates RSS feeds and generates AI-powered summaries using OpenAI. Built with **FastAPI**, **React + TypeScript**, **Celery**, **Redis**, and **PostgreSQL** — fully containerized with Docker.

## ✨ Features

- **RSS aggregation** — add any RSS/Atom feed URL and articles are fetched automatically
- **AI summarization** — each article gets a 3-4 sentence summary via local Ollama (llama3.2:1b)
- **Real-time updates** — new articles pushed to the browser via WebSocket, no polling
- **Background processing** — Celery workers handle fetching and summarizing asynchronously
- **Scheduled sync** — Beat scheduler refreshes all feeds every 10 minutes automatically
- **Fully containerized** — one command to run everything locally

## 🛠️ Tech Stack

 Layer | Technology |
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
 



## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/conradylx/RSS-summarizer.git
cd RSS-summarizer
```

### 2. Configure environment variables

```bash
vi .env
# Edit .env and add your OPENAI_API_KEY and database credentials
```
Example .env file:
```env
POSTGRES_USER=pgadmin
POSTGRES_PASSWORD=pgadmin
POSTGRES_DB=rsssummerizer
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://pgadmin:pgadmin@postgres:5432/rsssummerizer
REDIS_URL=redis://redis:6379/0
ALLOWED_ORIGINS=["http://localhost","http://localhost:8080","http://localhost:5173"]
```


### 3. Run with Docker Compose

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.yml up --build
```

> First run will take a few minutes — Ollama needs to pull the llama3.2:1b model (~1.3 GB).
 
The app will be available at:
- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API docs**: http://localhost:8000/docs

### 4. Run database migrations

```bash
docker-compose exec backend alembic upgrade head
```

## 🧪 Running Tests

```bash
docker-compose exec backend pytest
```


## 📄 License

MIT
