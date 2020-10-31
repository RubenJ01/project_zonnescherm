class Zonnescherm:

    def __init__(self, name):
        self.__gem_temperatuur_CB = None
        self.__gem_lichtintensiteit_CB = None
        self.__status_CB = None
        self.__name = name
        self.__queue_temperaturen = []
        self.__queue_lichtintensiteiten = []
        self.__oprol_afstand = 0
        self.__uitrol_afstand = 0
        self.__min_temperatuur = 0
        self.__max_temperatuur = 0
        self.__min_lichtintensiteit = 0
        self.__status = False
        self.__auto = True

    def __load_settings(self):
        pass

    def __send(self, char):
        pass

    def __receive(self):
        pass

    def set_gem_temperatuur_CB(self, callback):
        self.__gem_temperatuur_CB = callback

    def set_gem_lichtintensiteit_CB(self, callback):
        self.__gem_lichtintensiteit_CB = callback

    def set_status_CB(self, callback):
        self.__status_CB = callback

    def set_auto(self, auto):
        self.__auto = auto

    def set_status(self, status):
        self.__status = status

    def set_oprol(self, oprolafstand):
        self.__oprol_afstand = oprolafstand

    def set_uitrol(self, uitrolafstand):
        self.__uitrol_afstand = uitrolafstand

    def set_min_temperatuur(self, mintemperatuur):
        self.__min_temperatuur = mintemperatuur

    def set_max_temperatuur(self, maxtemperatuur):
        self.__max_temperatuur = maxtemperatuur

    def set_licht(self, minlichtintensiteit):
        self.__min_lichtintensiteit = minlichtintensiteit

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
