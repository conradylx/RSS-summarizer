from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import feeds, articles, ws
from app.config import ALLOWED_ORIGINS


app = FastAPI(title="RSS Summarizer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(feeds.router)
app.include_router(articles.router)
app.include_router(ws.router)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}
