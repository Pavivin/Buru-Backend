from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from services.connect_manager import ConnectionManager


chat_router = APIRouter


manager = ConnectionManager()


@chat_router.get("/chat")
async def get_chat():
    with open('src/templates/chat.html', 'r') as f:
        html = f.read()
    return HTMLResponse(html)


@chat_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
