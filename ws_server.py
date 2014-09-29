import asyncio
import websockets
from math import sin, pi

class bogusData:
    def __init__(self):
        self.next_val = 0.0

    def get_data(self):
        result = sin(self.next_val * pi)
        if (self.next_val >= 2.0):
            self.next_val = 0.0
        else:
            self.next_val += 0.01
        return result

@asyncio.coroutine
def ws_handler(websocket, path):
    sensor = bogusData()
    while True:
        yield from asyncio.sleep(0.05)
        value = sensor.get_data()
        if not websocket.open:
            break 
        yield from websocket.send(str(value))
    print("Socket Closed!")

start_server = websockets.serve(ws_handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
