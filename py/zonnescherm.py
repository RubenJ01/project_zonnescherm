import serial
import time

class Zonnescherm:

    def __init__(self, name):
        self.__name = name
        self.__ser = serial.Serial(port=self.__name.split()[1].strip(), baudrate=19200, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
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
        self.__load_settings()

    def open_connection(self):
        self.__ser.flushInput()

    def close_connection(self):
        self.__ser.close()

    def __load_settings(self):
        while self.__ser.inWaiting() == 0:
            self.__send(1)
            time.sleep(2.0) # Wacht 2 seconden
        counter = 0
        try:
            while self.__ser.isOpen() and (self.__ser.inWaiting() > 0 or counter < 27):
                data = ord(self.__ser.read(1))
                print("Load: ", counter, data)
                if counter == 0: # Zet de auto
                    self.__auto = bool(data)
                elif counter == 1: # Zet de status (open of dicht)
                    self.__status = bool(data)
                elif counter == 2: # Zet de oprol_afstand
                    self.__oprol_afstand = data
                elif counter == 3: # Zet de uitrol_afstand
                    self.__uitrol_afstand = data
                elif counter == 4: # Zet de min temperatuur
                    self.__min_temperatuur = data
                elif counter == 5: # Zet de max temperatuur
                    self.__max_temperatuur = data
                elif counter == 6: # Zet de min lichtintensiteit
                    self.__min_lichtintensiteit = data
                elif counter >= 7 and counter <= 16: # Zet de gemiddelde temperaturen in een lijstje
                    self.__queue_temperaturen.append(data-10) # -10 omdat we willen dat de temperatuur ergens ligt tussen -10 en 40 graden
                elif counter >= 17 and counter <= 26: # Zet de gemiddelde lichtintensiteiten in een lijstje
                    self.__queue_lichtintensiteiten.append(data)
                counter = counter+1
        except:
            pass

    def __send(self, data):
        if self.__ser.isOpen():
            print("Send: ", data)
            self.__ser.write(chr(data).encode())

    def receive(self):
        try:
            while self.__ser.isOpen() and self.__ser.inWaiting() > 0:
                data = ord(self.__ser.read(1))
                print("Receive:", data)
                if data <= 1: # Bij een waarde van 1 of lager betekent het dat het om de status gaat van het zonnescherm
                    self.__status = data
                    if self.__status_CB is not None:
                        self.__status_CB(self.__status)
                elif data <= 6: # Bij een waarde van 2 tot en met 6 betekent het dat er een nieuwe gemiddelde lichtintensiteit is
                    self.__queue_lichtintensiteiten.pop(0)
                    self.__queue_lichtintensiteiten.append(data-2)
                    if self.__gem_lichtintensiteit_CB is not None:
                        self.__gem_lichtintensiteit_CB(self.__queue_lichtintensiteiten)
                elif data <= 56: # Bij een waarde van 7 tot en met 56 betekent het dat er een nieuwe gemiddelde temperatuur is
                    self.__queue_temperaturen.pop(0)
                    self.__queue_temperaturen.append(data-7-10) # -10 omdat we willen dat de temperatuur ergens ligt tussen -10 en 40 graden
                    if self.__gem_temperatuur_CB is not None:
                        self.__gem_temperatuur_CB(self.__queue_temperaturen)
        except:
            pass

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
