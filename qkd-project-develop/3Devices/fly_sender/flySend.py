#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import hashlib
import json, struct
import threading
from socket import *
import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
import time
import os
import sys
import numpy as np
from numpy.linalg import norm

import protocol
import qkd

rasp_port = 20001

receiveer_ip = ''
receiver_port = -1

num_of_qubits = 100
listofBasis = list()
listofBits = list()
listofQubits = list()

recvListofBasis = list()
listofFinalkey = list()
# mission flags
dronefly_flage = False
filename = ''


async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")  # sim
    # await drone.connect(system_address="serial:///dev/ttyUSB0:57600")  # real

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, -3m Down within local coordinate system,face North")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -3.0, 0.0))
    await asyncio.sleep(10)
    # north 5m
    print("-- Go 5m North, 0m East, -3m Down within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(5.0, 0.0, -3.0, 90.0))
    await asyncio.sleep(10)
    # east 5m
    print("-- Go 5m North, 5m East, -3m Down within local coordinate system, turn to face South")
    await drone.offboard.set_position_ned(PositionNedYaw(5.0, 5.0, -3.0, 180.0))
    await asyncio.sleep(15)
    # sourth 5m
    print("-- Go 0m North, 5m East, -3m Down within local coordinate system, turn to face West")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 5.0, -3.0, 270.0))
    await asyncio.sleep(15)
    # west 5m
    print("-- Go 0m North, 0m East, -3m Down within local coordinate system, turn to face North")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -3.0, 0.0))
    await asyncio.sleep(15)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")


def droneFly():
    # global dronefly_flage
    # while True:
    #     if dronefly_flage:
    #         break
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def saveLog(filename, length, listofBasis, listofBits, listofQubits, recvListofBasis):
    if os.path.exists(filename):
        dateTime_p = datetime.datetime.now()
        str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d_%H-%M-%S')
        qubitsStr = qkd.listtoLineStr(qkd.listofQubitstoSymbol(listofQubits))
        bitsStr = qkd.listtoLineStr(qkd.listofBitstoSymbol(listofBits))
        baseStr = qkd.listtoLineStr(qkd.listofBasistoSymbol(listofBasis))
        recvbaseStr = qkd.listtoLineStr(qkd.listofBasistoSymbol(recvListofBasis))
        basisCompare, qber = qkd.compareBasis(listofBasis, recvListofBasis)
        compareBits = qkd.listtoLineStr(qkd.showFinalkeys(listofBits, basisCompare))
        compareBasis = qkd.listtoLineStr(qkd.showSameBasis(listofBits, basisCompare))
        finalKeys = qkd.listtoLineStr(qkd.finalKeys(listofBits, basisCompare))
        with open(filename, 'a+') as filelog:
            filelog.write(str_p + ': \n')
            filelog.write("QBER: " + str(qber*100) + "% \n")
            filelog.write("Length: " + str(length) + "\n")
            filelog.write("Qubits:\t" + qubitsStr + "\n")
            filelog.write("Bits:\t" + bitsStr + " \n")
            filelog.write("basis:\t" + baseStr + " \n")
            filelog.write("recvbasis:\t" + recvbaseStr + " \n")
            filelog.write("compareBits:\t" + compareBits + " \n")
            filelog.write("compareBasis:\t" + compareBasis + " \n")
            filelog.write("final keys:" +str(len(finalKeys))+'\t'+ finalKeys + " \n")
            filelog.write("\n\n\n")

    else:
        print('filename not found')
        return


def tcplink(sock, addr):
    global receiveer_ip
    global receiver_port
    global num_of_qubits
    global listofBits
    global listofBasis
    global listofQubits
    global recvListofBasis
    global listofFinalkey
    print('received from %s:%s' % addr)
    sock.send(b'had connected')  # send
    while True:
        date = sock.recv(2048)  # receive operation code + info
        if not date or date.decode('utf-8') == 'exit':
            break
        operaCode = protocol.parse_request_operaCode(date)
        if operaCode == 4:
            _, receiveer_ip, receiver_port = protocol.parse_recvip_info(date)

        if operaCode == 0:
            print('drone fly')
            # threading.Thread(target=droneFly, args=()).start()
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            asyncio.ensure_future(run())
            loop.run_forever()

        if operaCode == 1:
            pass
        if operaCode == 2:
            _, num_of_qubits = protocol.parse_generate_qubits_request(date)
            listofBasis = qkd.generateRandomBasis(num_of_qubits)
            listofBits = qkd.generateRandomBits(num_of_qubits)
            listofQubits = qkd.generateQubits(listofBasis, listofBits)
            recvListofBasis = list()
            listofFinalkey = list()
            qubitsbytes = qkd.listofQubitstoBytes(listofQubits)
            sock.send(qubitsbytes)  # send qubits

            print(sock.recv(1024).decode())  # recv 'Qubits received'

        if operaCode == 3:
            basisBytes = qkd.listtobytes(listofBasis)
            sc = socket(AF_INET, SOCK_STREAM)
            sc.connect((receiveer_ip, receiver_port))
            sc.send(protocol.make_generate_qubits_request(num_of_qubits))
            print(b'length: ' + sc.recv(1024))  # b'length recv'
            qubitsbytes = qkd.listofQubitstoBytes(listofQubits)
            sc.send(qubitsbytes)

            recvBasisB = sc.recv(num_of_qubits + 256)
            recvListofBasis = qkd.bytestolist(recvBasisB)

            print(b"recvBasisB " + recvBasisB)

            basisCompare, qber = qkd.compareBasis(listofBasis, recvListofBasis)
            print("QBER: ", qber * 100, "%")
            saveLog(filename,num_of_qubits, listofBasis, listofBits, listofQubits, recvListofBasis)
            sc.send(basisBytes)

            print(sc.recv(1024))  # b'Exchange successful'

            sock.send(recvBasisB)

    sock.close()
    print(' %s:%s connection closed。。。。' % addr)


if __name__ == '__main__':
    # create './data'
    if not os.path.exists('./data'):
        os.mkdir('./data')
    dateTime_p = datetime.datetime.now()
    str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d_%H-%M-%S')
    filename = './data/' + str_p + '.txt'
    open(filename, 'w+').close()

    # create a socket
    ss = socket(AF_INET, SOCK_STREAM)
    # bind port
    ss.bind(('', rasp_port))
    # listen port
    ss.listen(5)
    while True:
        sock, addr = ss.accept()
        # start a new thread to deal with TCP connect
        threading.Thread(target=tcplink, args=(sock, addr)).start()
