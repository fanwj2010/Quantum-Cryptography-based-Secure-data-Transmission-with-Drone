import asyncio
import socket

from mavsdk import System
from mavsdk.camera import (CameraError, Mode)

address = ('127.0.0.1', 31500)


def controller(p, f):
    drone_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # s = socket.socket()
    drone_s.bind(address)
    drone_s.listen(5)
    ss, addr = drone_s.accept()

    command = ss.recv(1)
    if command == "0":
        p.send(0)
        print(0)
    if command == "1":
        f.send(1)
        print(1)

    ss.send("0".encode())



def photo():
   print("take photo")




async def fly():


    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)

    print("-- Landing")
    await drone.action.land()

if __name__ == "__main__":
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    p = photo()
    f = fly()
    controller(p, f)

