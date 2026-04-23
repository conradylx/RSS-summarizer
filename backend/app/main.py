from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import feeds, articles, ws
from app.config import settings

app = FastAPI(title="RSS Summarizer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(feeds.router, prefix="/api")
app.include_router(articles.router, prefix="/api")
app.include_router(ws.router, prefix="/api")


@app.get("/api/healthcheck")
def healthcheck():
    return {"status": "healthy"}
