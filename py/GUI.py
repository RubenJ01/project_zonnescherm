from zonnescherm import *

from tkinter import *
from tkinter import _setit


class GUI:

    def __init__(self):
        self.__zonneschermen = []
        self.__selected_zonnescherm = None

        # Callbacks
        self.__zonneschermCB = None
        self.__autoCB = None
        self.__open_sluitCB = None
        self.__oprolCB = None
        self.__uitrolCB = None
        self.__min_temperatuurCB = None
        self.__max_temperatuurCB = None
        self.__lichtCB = None
        # Variables
        self.__auto = True
        self.__is_open = True
        # The root(TK)
        self.__root = Tk()
        self.__root.title('Project 2.1')
        self.__root.resizable(False, False)
        # Top frame
        self.__frameTop = Frame(self.__root)
        self.__frameTop.pack(side=TOP, expand=YES, fill=X)
        # Canvas
        self.__canvas = Canvas(self.__root, width=1200, height=600, bg='white')
        self.__canvas.pack(expand=YES, fill=BOTH)
        # Bottom frame
        self.__frameBottom = Frame(self.__root)
        self.__frameBottom.pack(side=BOTTOM, expand=YES, fill=X)
        # Drop down voor selecteren zonnescherm
        self.__devices = ["Geen zonnescherm"]
        self.__selected_device = StringVar()
        self.__selected_device.set(self.__devices[0])
        self.__zonnescherm_opties = OptionMenu(self.__frameTop, self.__selected_device, *self.__devices,
                                               command=self.__select_zonnescherm)
        self.__zonnescherm_opties.pack(side=LEFT)
        # Automatisch button
        self.__auto_button = Button(self.__frameTop, text='Zet automatisch uit', command=self.__set_auto)
        self.__auto_button.pack(side=LEFT)
        # Dicht open button
        self.__open_sluit_button = Button(self.__frameTop, text='Open zonnescherm',
                                          command=self.__set_status)
        self.__open_sluit_button.pack(side=LEFT)
        self.__status_zonnescherm_label = Label(self.__frameTop, text="Status: zonnescherm is dicht")
        self.__status_zonnescherm_label.pack(side=LEFT)
        # Op en uitrol afstand
        self.__entryOprolAfstand = Entry(self.__frameBottom, bg='grey')
        self.__entryOprolAfstand.pack(side=LEFT)
        Button(self.__frameBottom, text='Zet oprol afstand', command=self.__set_oprol).pack(side=LEFT)
        self.__entryUitrolAfstand = Entry(self.__frameBottom, bg='grey')
        self.__entryUitrolAfstand.pack(side=LEFT)
        Button(self.__frameBottom, text='Zet uitrol afstand', command=self.__set_uitrol).pack(side=LEFT)
        # Minimum en maxim temperatuur
        self.__entryMinTemperatuur = Entry(self.__frameBottom, bg='grey')
        self.__entryMinTemperatuur.pack(side=LEFT)
        Button(self.__frameBottom, text='Zet minimum temperatuur', command=self.__set_min_temperatuur).pack(side=LEFT)
        self.__entryMaxTemperatuur = Entry(self.__frameBottom, bg='grey')
        self.__entryMaxTemperatuur.pack(side=LEFT)
        Button(self.__frameBottom, text='Zet maximum temperatuur', command=self.__set_max_temperatuur).pack(side=LEFT)
        # Lichtopties
        self.__lichtopties_label = Label(self.__frameBottom, text="Zet lichtintensiteit:")
        self.__lichtopties_label.pack(side=LEFT)
        self.__lichtopties = ["Donker", "Schemerig", "Neutraal", "Licht", "Veel licht"]
        self.__selected_licht = StringVar()
        self.__selected_licht.set(self.__lichtopties[0])
        OptionMenu(self.__frameBottom, self.__selected_licht, *self.__lichtopties, command=self.__set_licht).pack(
            side=LEFT)

        # Grafiek tempertatuur
        self.__canvas.create_line(50, 550, 550, 550, width=2)  # x-axis (x,y)(x,y)
        self.__canvas.create_text(50, 25, fill="darkblue", text="Temperatuur celcius", anchor=NW)
        self.__canvas.create_line(50, 50, 50, 550, width=2)  # y-axis
        self.__canvas.create_text(550, 575, fill="darkblue", text="Gemiddelde temperatuur per minuut", anchor=NE)
        # x-axis
        for i in range(11):
            x = 50 + (i * 50)
            self.__canvas.create_line(x, 550, x, 50, width=1, dash=(2, 5))
            self.__canvas.create_text(x, 550, text='%d' % (1 * i), anchor=N)
        ## y-axis
        for i in range(11):
            y = 550 - (i * 50)
            self.__canvas.create_line(50, y, 550, y, width=1, dash=(2, 5))
            self.__canvas.create_text(40, y, text='%d' % (5 * i - 10), anchor=E)

        # Grafiek tempertatuur
        self.__canvas.create_line(675, 550, 1175, 550, width=2)  # x-axis (x,y)(x,y)
        self.__canvas.create_text(675, 25, fill="darkblue", text="Lichtintensiteit", anchor=NW)
        self.__canvas.create_line(675, 550, 675, 50, width=2)  # y-axis
        self.__canvas.create_text(1175, 575, fill="darkblue", text="Gemiddelde lichtintensiteit per minuut", anchor=NE)
        # x-axis
        for i in range(11):
            x = 675 + (i * 50)
            self.__canvas.create_line(x, 550, x, 50, width=1, dash=(2, 5))
            self.__canvas.create_text(x, 550, text='%d' % (1 * i), anchor=N)
        ### y-axis
        for i in range(5):
            y = 550 - (i * 125)
            self.__canvas.create_line(675, y, 1175, y, width=1, dash=(2, 5))
            self.__canvas.create_text(665, y, text=self.__lichtopties[i], anchor=E)

        # Set de mainloop aan
        # self.__root.mainloop()

    def __select_zonnescherm(self, value=None):
        if value == "Geen zonnescherm":
            self.__selected_zonnescherm = None
            return
        for zonnescherm in self.__zonneschermen:
            if zonnescherm.get_name() == value:
                self.__selected_zonnescherm = zonnescherm
                return

    def __set_auto(self):
        if self.__selected_zonnescherm is not None:
            if self.__selected_zonnescherm.get_auto():
                self.__selected_zonnescherm.set_auto(False)
                self.__auto_button["text"] = "Zet automatisch uit"
            else:
                self.__selected_zonnescherm.set_auto(True)
                self.__auto_button["text"] = "Zet automatisch aan"

    def __set_status(self):
        if self.__selected_zonnescherm is not None:
            self.__selected_zonnescherm.set_status(not self.__selected_zonnescherm.get_status())
            if self.__selected_zonnescherm.get_status():
                self.__open_sluit_button["text"] = "Sluit zonnescherm"
                self.__status_zonnescherm_label["text"] = "Status: zonnescherm is open"
            else:
                self.__open_sluit_button["text"] = "Open zonnescherm"
                self.__status_zonnescherm_label["text"] = "Status: zonnescherm is dicht"


    def __set_oprol(self):
        # TODO: Verander deze functie
        if self.__oprolCB != None:
            self.__oprolCB(self.__entryOprolAfstand.get())

    def __set_uitrol(self):
        # TODO: Verander deze functie
        if self.__uitrolCB != None:
            self.__uitrolCB(self.__entryUitrolAfstand.get())

    def __set_min_temperatuur(self):
        # TODO: Verander deze functie
        if self.__min_temperatuurCB != None:
            self.__min_temperatuurCB(self.__entryMinTemperatuur.get())

    def __set_max_temperatuur(self):
        # TODO: Verander deze functie
        if self.__max_temperatuurCB != None:
            self.__max_temperatuurCB(self.__entryMaxTemperatuur.get())

    def __set_licht(self, value):
        # TODO: Verander deze functie
        if self.__lichtCB != None:
            if value == "Donker":
                self.__lichtCB(0)
            elif value == "Schemerig":
                self.__lichtCB(1)
            elif value == "Neutraal":
                self.__lichtCB(2)
            elif value == "Licht":
                self.__lichtCB(3)
            elif value == "Veel licht":
                self.__lichtCB(4)

    def __receive_gem_temperatuur(temperaturen):
        # TODO: Verander deze functie
        pass

    def __receive_gem_lichtintensiteiten(lichtintensiteiten):
        # TODO: Verander deze functie
        pass

    def __receive_status(status):
        # TODO: Verander deze functie
        pass

    def start(self):
        self.__root.mainloop()

    def add_zonnescherm(self, zonnescherm):
        self.__zonneschermen.append(zonnescherm)
        self.__devices.append(zonnescherm.get_name())
        self.__refresh_zonneschermen()

    def remove_zonnescherm(self, name):
        self.__devices.remove(name)
        for zonnescherm in self.__zonneschermen:
            if zonnescherm.get_name() == name:
                self.__zonneschermen.remove(zonnescherm)
                break
        self.__refresh_zonneschermen()

    def __refresh_zonneschermen(self):
        self.__selected_device.set("Geen Zonnescherm")
        self.__zonnescherm_opties["menu"].delete(0, 'end')
        for zonnescherm in self.__devices:
            self.__zonnescherm_opties["menu"].add_command(label=zonnescherm,
                                                          command=_setit(self.__selected_device, zonnescherm,
                                                                         self.__select_zonnescherm))
