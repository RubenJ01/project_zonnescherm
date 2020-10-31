import serial


class ZonneschermLoader:

    def __init__(self):
        self.__send_CB = None
        self.__remove_CB = None

    def get_zonnescherm_CB(self, cb):
        self.__send_CB = cb

    def remove_zonnescherm_CB(self, cb):
        self.__remove_CB = cb
