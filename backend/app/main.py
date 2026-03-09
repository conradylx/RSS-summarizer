from fastapi import FastAPI
from app.routers import feeds

app = FastAPI(title="RSS Summarizer")
app.include_router(feeds.router)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}
