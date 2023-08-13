from fastapi import WebSocket


class Client:
    def __init__(self, websocket: WebSocket, client_type=None):
        self.websocket = websocket
        self.client_type = client_type
