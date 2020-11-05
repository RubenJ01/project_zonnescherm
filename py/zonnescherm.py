import serial

class Zonnescherm:

    def __init__(self, name):
        self.__name = name
        self.__ser = None
        self.__gem_temperatuur_CB = None
        self.__gem_lichtintensiteit_CB = None
        self.__status_CB = None
        self.__queue_temperaturen = []
        self.__queue_lichtintensiteiten = []
        self.__oprol_afstand = 0
        self.__uitrol_afstand = 0
        self.__min_temperatuur = 0
        self.__max_temperatuur = 0
        self.__min_lichtintensiteit = 0
        self.__status = False
        self.__auto = True

    def open_connection(self):
        self.__ser = serial.Serial(port=self.__name.split()[1].strip(), baudrate=19200, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        self.__ser.flushInput()

    def close_connection(self):
        self.__ser.close()

    def __load_settings(self):
        pass

    def __send(self, data):
        if self.__ser.isOpen():
            print("Send: ", data)
            self.__ser.write(chr(data).encode())
            #self.__ser.flushOutput()

    def receive(self):
        try:
            while self.__ser.isOpen() and self.__ser.inWaiting() > 0:
                print(ord(self.__ser.read(1)))
            #self.__ser.flushInput()
        except:
            print("receive failed")

    def set_gem_temperatuur_CB(self, callback):
        self.__gem_temperatuur_CB = callback

    def set_gem_lichtintensiteit_CB(self, callback):
        self.__gem_lichtintensiteit_CB = callback

    def set_status_CB(self, callback):
        self.__status_CB = callback

    def set_auto(self, auto):
        self.__auto = auto
        self.__send(2)
        self.__send(self.__auto)

    def set_status(self, status):
        self.__status = status
        self.__send(3)
        self.__send(self.__status)

    def set_oprol(self, oprolafstand):
        self.__oprol_afstand = oprolafstand
        self.__send(4)
        self.__send(self.__oprol_afstand)

    def set_uitrol(self, uitrolafstand):
        self.__uitrol_afstand = uitrolafstand
        self.__send(5)
        self.__send(self.__uitrol_afstand)

    def set_min_temperatuur(self, mintemperatuur):
        self.__min_temperatuur = mintemperatuur
        self.__send(6)
        self.__send(self.__min_temperatuur)

    def set_max_temperatuur(self, maxtemperatuur):
        self.__max_temperatuur = maxtemperatuur
        self.__send(7)
        self.__send(self.__max_temperatuur)

    def set_licht(self, minlichtintensiteit):
        self.__min_lichtintensiteit = minlichtintensiteit
        self.__send(8)
        self.__send(self.__min_lichtintensiteit)

    def get_name(self):
        return self.__name

    def get_temperaturen(self):
        return self.__queue_temperaturen

    def get_lichtintensiteiten(self):
        return self.__queue_lichtintensiteiten

    def get_oprol_afstand(self):
        return self.__oprol_afstand

    def get_uitrol_afstand(self):
        return self.__uitrol_afstand

    def get_min_temperatuur(self):
        return self.__min_temperatuur

    def get_max_temperatuur(self):
        return self.__max_temperatuur

    def get_lichtintensiteit(self):
        return self.__min_lichtintensiteit

    def get_status(self):
        return self.__status

    def get_auto(self):
        return self.__auto
