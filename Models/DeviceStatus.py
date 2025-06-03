class DeviceStatus:
    def __init__(self, device_sn=None, websocket=None, status=None):
        self.device_sn = device_sn
        self.websocket = websocket  # This should be an instance of a WebSocket class
        self.status = status

    def setWebSocket(self, websocket):
        self.websocket = websocket

    def __str__(self):
        return f"DeviceStatus [deviceSn={self.device_sn}, webSocket={self.websocket}, status={self.status}]"

