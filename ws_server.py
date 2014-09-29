import asyncio
import websockets
from math import sin, pi

# This class generates the values of sine
# from 0 - 2pi radians in 200 steps
class bogusData:
    def __init__(self):
        self.next_val = 0.0

    # calculate the next value and return it,
    # incrementing the multiplier by 0.01
    def get_data(self):
        result = sin(self.next_val * pi)
        if (self.next_val >= 2.0):
            self.next_val = 0.0
        else:
            self.next_val += 0.01
        return result

# the handler for WebSockets
# loops while the websocket is open,
# getting data from the generator and
# sending it to the client
@asyncio.coroutine
def ws_handler(websocket, path):
    sensor = bogusData()      # instantiate the generator
    while True:
        yield from asyncio.sleep(0.05)  # limit the speed of generation
        value = sensor.get_data()       # get the next value
        if not websocket.open:
            break  # break the loop if the socket closed
        yield from websocket.send(str(value)) # send the value to the client
    print("Socket Closed!")

# assigning a function to a variable name.  Awesome.
start_server = websockets.serve(ws_handler, 'localhost', 8765)

# the event loops
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
