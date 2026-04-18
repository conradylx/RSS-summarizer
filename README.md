# 📰 RSS Summarizer

A full-stack application that aggregates RSS feeds and generates AI-powered summaries using OpenAI. Built with **FastAPI**, **React + TypeScript**, **Celery**, **Redis**, and **PostgreSQL** — fully containerized with Docker.

## ✨ Features

- 📡 Fetch and parse RSS feeds from multiple sources
- 🤖 AI-generated summaries via OpenAI API
- ⚡ Asynchronous task processing with Celery + Redis
- 🔄 Real-time updates via WebSockets
- 🗄️ Persistent storage with PostgreSQL + Alembic migrations
- 🐳 Docker Compose setup for both development and production
- ✅ Async test suite with pytest + pytest-asyncio

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, FastAPI, SQLAlchemy 2.0 |
| Task Queue | Celery 5, Redis 7 |
| Database | PostgreSQL, Alembic (migrations) |
| Frontend | React 18, TypeScript, Vite |
| Containerization | Docker, Docker Compose |
| AI | OpenAI API |
| Testing | pytest, pytest-asyncio, httpx |
| Code Quality | black, pylint |


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
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and database credentials
```

### 3. Run with Docker Compose

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build
```

The app will be available at:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

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
