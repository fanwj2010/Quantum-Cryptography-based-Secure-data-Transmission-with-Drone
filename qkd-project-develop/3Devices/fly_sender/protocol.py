#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
opera_code: 
    0: drone fly
    1: take photo
    2: generate qubits
    3: send qubits and exchange basis
    4: send receiver's ip and port
"""
import json
import struct


def parse_request_operaCode(msg):
    opera_code = struct.unpack('!I', msg[:4])[0]
    return opera_code


def make_dronefly_info(mission):
    """

    :param mission: list
    :return: bytes
    """
    opera_code = 0
    header = struct.pack("!I", opera_code)
    info_json = json.dumps(mission).encode()
    infolen = struct.pack("!I", len(info_json))
    return header + infolen + info_json


def parse_dronefly_info(msg):
    opera_code = struct.unpack('!I', msg[:4])[0]
    infolen = struct.unpack('!I', msg[4:8])[0]
    missioninfo = json.loads(msg[8:8 + infolen].decode())
    return opera_code, missioninfo


def make_recvip_info(ip,port):
    opera_code = 4
    header = struct.pack("!I", opera_code)
    var=list()
    var.append(ip)
    var.append(port)
    info_json = json.dumps(var).encode()
    infolen = struct.pack("!I", len(info_json))
    return header + infolen + info_json


def parse_recvip_info(msg):
    """
    :param msg:
    :return: operation code ,ip ,port
    """
    opera_code = struct.unpack('!I', msg[:4])[0]
    infolen = struct.unpack('!I', msg[4:8])[0]
    ipinfo = json.loads(msg[8:8 + infolen].decode())
    return opera_code, ipinfo[0], ipinfo[1]


def make_snap_request():
    opera_code = 1
    header = struct.pack("!I", opera_code)
    # info_json = filename.encode()
    # infolen = struct.pack("!I", len(info_json))
    infolen = struct.pack("!I", 0)
    return header + infolen


def parse_snap_request(msg):
    opera_code = struct.unpack('!I', msg[:4])[0]
    # infolen = struct.unpack('!I', msg[4:8])[0]
    return opera_code


def make_generate_qubits_request(length):
    opera_code = 2
    header = struct.pack("!I", opera_code)
    lengthB= str(length).encode()
    infolen = struct.pack("!I", len(lengthB))
    return header + infolen + lengthB


def parse_generate_qubits_request(msg):
    opera_code = struct.unpack('!I', msg[:4])[0]
    infolen = struct.unpack('!I', msg[4:8])[0]
    length = json.loads(msg[8:8 + infolen].decode())
    return opera_code, length


def make_send_qubits_request():
    opera_code = 3
    header = struct.pack("!I", opera_code)
    # info = filename.encode()
    # infolen = struct.pack("!I", len(info))
    infolen = struct.pack("!I", 0)
    return header + infolen


def parse_send_qubits_request(msg):
    opera_code = struct.unpack('!I', msg[:4])[0]
    # infolen = struct.unpack('!I', msg[4:8])[0]
    # filename = msg[8:8 + infolen].decode()
    return opera_code

# def make_file_news(filename, news):
#     filenews = [news[0], news[1], news[2], news[3], filename]
#     # filenews.append(filename)
#     opera_code = 9
#     header = struct.pack("!I", opera_code)
#     info_json = json.dumps(filenews).encode()
#     infolen = struct.pack("!I", len(info_json))
#     return header + infolen + info_json
#
#
# def parse_file_news(msg):
#     opera_code = struct.unpack('!I', msg[:4])[0]
#     infolen = struct.unpack('!I', msg[4:8])[0]
#     filenews = json.loads(msg[8:8 + infolen].decode())
#     return opera_code, filenews
#
#
# def make_error_info(errorInfo):
#     opera_code = 0
#     header = struct.pack("!I", opera_code)
#     info_json = json.dumps(errorInfo).encode()
#     infolen = struct.pack("!I", len(info_json))
#     return header + infolen + info_json

# def parse_error_info(msg):
#     opera_code=struct.unpack('!I',msg[:4])[0]
#     infolen=struct.unpack('!I',msg[4:8])[0]
#     fileinfo=json.loads(msg[8:8+infolen].decode())
#     return opera_code, fileinfo
