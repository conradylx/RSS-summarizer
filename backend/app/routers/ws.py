from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.broadcast import subscribe_articles

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for article in subscribe_articles():
            await websocket.send_json(article)
    except WebSocketDisconnect:
        pass
