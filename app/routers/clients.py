from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.internal.classes import ConnectionManager

router = APIRouter(prefix="/room")

rooms = {}


# TODO: ВЗАИМОДЕЙСТВИЕ КЛИЕНТОВ ANDROID + DESKTOP


@router.get("/{room_id}")
async def return_room(room_id: str):
    if room_id in rooms:
        return {"status": 200, "message": "Ok!"}
    else:
        return {"status": 404, "message": "Неверный код комнаты!"}


@router.websocket("/{room_id}")
async def websocket_room(websocket: WebSocket, room_id: str):
    try:
        manager = rooms[room_id]
    except KeyError as e:
        rooms[room_id] = ConnectionManager()
        manager = rooms[room_id]
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "disabled" and len(manager.active_connections) != 2:
                await manager.send_personal_message(websocket, {"status": 400, "message": "Комната пустая!"})
                await websocket.close()
            try:
                await manager.broadcast(data)
            except:
                pass
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
        if len(manager.active_connections) == 0:
            del (rooms[room_id])
