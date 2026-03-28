import asyncio
import websockets

async def test():
    try:
        async with websockets.connect('ws://127.0.0.1:8000/ws/pose-detection/') as websocket:
            print("Connected!")
            await websocket.send('{"test": "hello"}')
            response = await websocket.recv()
            print(f"Received: {response}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())