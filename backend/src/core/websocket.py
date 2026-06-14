import json
import logging
from typing import Dict, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger("omniflow.websocket")


class ConnectionManager:
    def __init__(self):
        self._active_connections: Dict[str, Set[WebSocket]] = {}
        self._user_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str, user_id: Optional[str] = None):
        await websocket.accept()
        if room not in self._active_connections:
            self._active_connections[room] = set()
        self._active_connections[room].add(websocket)

        if user_id:
            if user_id not in self._user_connections:
                self._user_connections[user_id] = set()
            self._user_connections[user_id].add(websocket)

        logger.info(f"WebSocket connected: room={room}, user={user_id}")

    async def disconnect(self, websocket: WebSocket, room: str, user_id: Optional[str] = None):
        if room in self._active_connections:
            self._active_connections[room].discard(websocket)
            if not self._active_connections[room]:
                del self._active_connections[room]

        if user_id and user_id in self._user_connections:
            self._user_connections[user_id].discard(websocket)
            if not self._user_connections[user_id]:
                del self._user_connections[user_id]

        logger.info(f"WebSocket disconnected: room={room}, user={user_id}")

    async def send_personal(self, websocket: WebSocket, data: Dict[str, Any]):
        try:
            await websocket.send_json(data)
        except Exception:
            logger.error("Failed to send personal message")

    async def broadcast_to_room(self, room: str, data: Dict[str, Any]):
        if room not in self._active_connections:
            return
        disconnected = set()
        for connection in self._active_connections[room]:
            try:
                await connection.send_json(data)
            except Exception:
                disconnected.add(connection)
        for conn in disconnected:
            self._active_connections[room].discard(conn)

    async def send_to_user(self, user_id: str, data: Dict[str, Any]):
        if user_id not in self._user_connections:
            return
        disconnected = set()
        for connection in self._user_connections[user_id]:
            try:
                await connection.send_json(data)
            except Exception:
                disconnected.add(connection)
        for conn in disconnected:
            self._user_connections[user_id].discard(conn)

    def get_room_count(self, room: str) -> int:
        return len(self._active_connections.get(room, set()))

    def get_total_connections(self) -> int:
        return sum(len(conns) for conns in self._active_connections.values())


ws_manager = ConnectionManager()
