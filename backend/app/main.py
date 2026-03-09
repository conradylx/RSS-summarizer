from fastapi import FastAPI
from app.routers import feeds, articles, ws

app = FastAPI(title="RSS Summarizer")
app.include_router(feeds.router)
app.include_router(articles.router)
app.include_router(ws.router)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}
