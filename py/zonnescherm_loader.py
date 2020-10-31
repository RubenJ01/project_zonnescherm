from zonnescherm import *

import serial.tools.list_ports

class ZonneschermLoader:

    def __init__(self):
        self.__zonneschermen = []
        self.__send_CB = None
        self.__remove_CB = None

    def get_zonnescherm_CB(self, cb):
        self.__send_CB = cb

    def remove_zonnescherm_CB(self, cb):
        self.__remove_CB = cb

    def update(self):
        ports = [("Zonnescherm " + port) for port, desc, hwid in serial.tools.list_ports.comports() if "Arduino Uno" in desc]
        added = [port for port in ports if port not in self.__zonneschermen]
        removed = [zonnescherm for zonnescherm in self.__zonneschermen if zonnescherm not in ports]
        for a in added:
            self.__add_zonnescherm(a)

        for r in removed:
            self.__remove_zonnescherm(r)

    def __add_zonnescherm(self, port):
        self.__zonneschermen.append(port)
        zonnescherm = Zonnescherm(port)
        if self.__send_CB is not None:
            self.__send_CB(zonnescherm)
    
    def __remove_zonnescherm(self, port):
        self.__zonneschermen.remove(port)
        if self.__remove_CB is not None:
            self.__remove_CB(port)