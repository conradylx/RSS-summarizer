from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config import ALLOWED_ORIGINS
from app.broadcast import subscribe_articles

router = APIRouter()


@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    origin = websocket.headers.get("origin", "")
    if origin not in ALLOWED_ORIGINS:
        await websocket.close(code=4403)
        return

    await websocket.accept()
    try:
        async for article in subscribe_articles():
            await websocket.send_json(article)
    except WebSocketDisconnect:
        pass
