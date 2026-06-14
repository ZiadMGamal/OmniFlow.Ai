import json
import logging
from uuid import UUID
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.websocket import ws_manager
from src.core.security import decode_token

logger = logging.getLogger("omniflow.chat")

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.websocket("/ws/{conversation_id}")
async def chat_websocket(
    websocket: WebSocket,
    conversation_id: str,
    token: str,
    session: AsyncSession = Depends(get_session),
):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
    except Exception as e:
        await websocket.close(code=1008, reason=f"Invalid token: {e}")
        return

    await ws_manager.connect(websocket, room=f"conv_{conversation_id}", user_id=user_id)

    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                
                # Echo back for now until agents are connected
                response = {
                    "event": "message_chunk",
                    "data": {
                        "content": f"Received: {message_data.get('content', '')}",
                        "is_complete": True
                    }
                }
                await ws_manager.send_personal(websocket, response)
                
            except json.JSONDecodeError:
                await ws_manager.send_personal(websocket, {"error": "Invalid JSON format"})
                
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, room=f"conv_{conversation_id}", user_id=user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await ws_manager.disconnect(websocket, room=f"conv_{conversation_id}", user_id=user_id)
