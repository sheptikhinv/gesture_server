from fastapi import FastAPI, WebSocket
from .routers import clients

app = FastAPI()

app.include_router(clients.router)