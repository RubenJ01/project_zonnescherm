from zonnescherm import *

from tkinter import *
from tkinter import _setit


class GUI:

    def __init__(self):
        # Variables
        self.__zonneschermen = []
        self.__selected_zonnescherm = None
        self.__update_CB = None
        self.__update_milliseconds = 1000
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
        self.__open_sluit_button = Button(self.__frameTop, text='Open zonnescherm', command=self.__set_status)
        self.__open_sluit_button.pack(side=LEFT)
        self.__status_zonnescherm_label = Label(self.__frameTop, text="Status: zonnescherm is dicht")
        self.__status_zonnescherm_label.pack(side=LEFT)
        # Op en uitrol afstand
        self.__entry_oprol_text = StringVar()
        self.__entry_oprol_text.set("0")
        Entry(self.__frameBottom, textvariable=self.__entry_oprol_text, bg='grey').pack(side=LEFT)
        Button(self.__frameBottom, text='Zet oprol afstand', command=self.__set_oprol).pack(side=LEFT)
        self.__entry_uitrol_text = StringVar()
        self.__entry_uitrol_text.set("0")
        Entry(self.__frameBottom, textvariable=self.__entry_uitrol_text, bg='grey').pack(side=LEFT)
        Button(self.__frameBottom, text='Zet uitrol afstand', command=self.__set_uitrol).pack(side=LEFT)
        # Minimum en maxim temperatuur
        self.__entry_min_temperatuur_text = StringVar()
        self.__entry_min_temperatuur_text.set("0")
        Entry(self.__frameBottom, textvariable=self.__entry_min_temperatuur_text, bg='grey').pack(side=LEFT)
        Button(self.__frameBottom, text='Zet minimum temperatuur', command=self.__set_min_temperatuur).pack(side=LEFT)
        self.__entry_max_temperatuur_text = StringVar()
        self.__entry_max_temperatuur_text.set("0")
        Entry(self.__frameBottom, textvariable=self.__entry_max_temperatuur_text, bg='grey').pack(side=LEFT)
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
        self.__canvas.create_line(50, 550, 500, 550, width=2)  # x-axis (x,y)(x,y)
        self.__canvas.create_text(50, 25, fill="darkblue", text="Temperatuur celcius", anchor=NW)
        self.__canvas.create_line(50, 50, 50, 550, width=2)  # y-axis
        self.__canvas.create_text(550, 575, fill="darkblue", text="Gemiddelde temperatuur per minuut", anchor=NE)
        # x-axis
        for i in range(10):
            x = 50 + (i * 50)
            self.__canvas.create_line(x, 550, x, 50, width=1, dash=(2, 5))
            self.__canvas.create_text(x, 550, text='%d' % ((1 * i) + 1), anchor=N)
        ## y-axis
        for i in range(11):
            y = 550 - (i * 50)
            self.__canvas.create_line(50, y, 500, y, width=1, dash=(2, 5))
            self.__canvas.create_text(40, y, text='%d' % (5 * i - 10), anchor=E)

        # Grafiek lichtintensiteit
        self.__canvas.create_line(675, 550, 1125, 550, width=2)  # x-axis (x,y)(x,y)
        self.__canvas.create_text(675, 25, fill="darkblue", text="Lichtintensiteit", anchor=NW)
        self.__canvas.create_line(675, 550, 675, 50, width=2)  # y-axis
        self.__canvas.create_text(1175, 575, fill="darkblue", text="Gemiddelde lichtintensiteit per minuut", anchor=NE)
        # x-axis
        for i in range(10):
            x = 675 + (i * 50)
            self.__canvas.create_line(x, 550, x, 50, width=1, dash=(2, 5))
            self.__canvas.create_text(x, 550, text='%d' % ((1 * i) + 1), anchor=N)
        ### y-axis
        for i in range(5):
            y = 550 - (i * 125)
            self.__canvas.create_line(675, y, 1125, y, width=1, dash=(2, 5))
            self.__canvas.create_text(665, y, text=self.__lichtopties[i], anchor=E)

        # Set de mainloop aan
        # self.__root.mainloop()

    def __select_zonnescherm(self, value=None):
        """
        Selecteerd een zonnescherm.
        :param value: het zonnescherm dat je selecteerd.
        :return: void.
        """
        if value == "Geen zonnescherm":
            if self.__selected_zonnescherm is not None:
                # Remove de callbacks van het zonnescherm
                self.__selected_zonnescherm.set_gem_temperatuur_CB(None)
                self.__selected_zonnescherm.set_gem_lichtintensiteit_CB(None)
                self.__selected_zonnescherm.set_status_CB(None)
                self.__selected_zonnescherm = None
            return
        for zonnescherm in self.__zonneschermen:
            if zonnescherm.get_name() == value:
                self.__selected_zonnescherm = zonnescherm
                # Set data van zonnescherm in GUI
                self.__auto_button[
                    "text"] = "Zet automatisch uit" if self.__selected_zonnescherm.get_auto() else "Zet automatisch aan"
                self.__open_sluit_button[
                    "text"] = "Sluit zonnescherm" if self.__selected_zonnescherm.get_status() else "Open zonnescherm"
                self.__status_zonnescherm_label[
                    "text"] = "Status: zonnescherm is open" if self.__selected_zonnescherm.get_status() else "Status: zonnescherm is dicht"
                self.__entry_oprol_text.set(self.__selected_zonnescherm.get_oprol_afstand())
                self.__entry_uitrol_text.set(self.__selected_zonnescherm.get_uitrol_afstand())
                self.__entry_min_temperatuur_text.set(self.__selected_zonnescherm.get_min_temperatuur())
                self.__entry_max_temperatuur_text.set(self.__selected_zonnescherm.get_max_temperatuur())
                self.__selected_licht.set(self.__lichtopties[self.__selected_zonnescherm.get_lichtintensiteit()])
                # Set de callbacks voor het zonnescherm
                self.__selected_zonnescherm.set_gem_temperatuur_CB(self.__receive_gem_temperatuur)
                self.__selected_zonnescherm.set_gem_lichtintensiteit_CB(self.__receive_gem_lichtintensiteiten)
                self.__selected_zonnescherm.set_status_CB(self.__receive_status)
                return

    def __set_auto(self):
        """
        Stelt de automatische modus in.
        """
        if self.__selected_zonnescherm is not None:
            self.__selected_zonnescherm.set_auto(not self.__selected_zonnescherm.get_auto())
            if self.__selected_zonnescherm.get_auto():
                self.__auto_button["text"] = "Zet automatisch uit"
            else:
                self.__auto_button["text"] = "Zet automatisch aan"

    def __set_status(self):
        """
        Stelt de status van het zonnescherm in en past het aan op de gui.
        """
        if self.__selected_zonnescherm is not None:
            self.__selected_zonnescherm.set_status(not self.__selected_zonnescherm.get_status())
            if self.__selected_zonnescherm.get_status():
                self.__open_sluit_button["text"] = "Sluit zonnescherm"
                self.__status_zonnescherm_label["text"] = "Status: zonnescherm is open"
            else:
                self.__open_sluit_button["text"] = "Open zonnescherm"
                self.__status_zonnescherm_label["text"] = "Status: zonnescherm is dicht"

    def __set_oprol(self):
        """
        Stelt de oprol afstand in.
        """
        if self.__selected_zonnescherm is not None:
            self.__selected_zonnescherm.set_oprol(self.__entry_oprol_text.get())

    def __set_uitrol(self):
        """
        Stelt de uitrol afstand in.
        """
        if self.__selected_zonnescherm is not None:
            self.__selected_zonnescherm.set_uitrol(self.__entry_uitrol_text.get())

    def __set_min_temperatuur(self):
        """
        Stelt de minimum temperatuur in.
        """
        if self.__selected_zonnescherm is not None:
            self.__selected_zonnescherm.set_min_temperatuur(self.__entry_min_temperatuur_text.get())

    def __set_max_temperatuur(self):
        """
        Stelt de maximum temperatuur in.
        """
        if self.__selected_zonnescherm is not None:
            self.__selected_zonnescherm.set_max_temperatuur(self.__entry_max_temperatuur_text.get())

    def __set_licht(self, value):
        """
        Stelt de lichtintensiteit in.
        :param value: de lichtintensiteit.
        """
        if self.__selected_zonnescherm is not None:
            if value == "Donker":
                self.__selected_zonnescherm.set_licht(0)
            elif value == "Schemerig":
                self.__selected_zonnescherm.set_licht(1)
            elif value == "Neutraal":
                self.__selected_zonnescherm.set_licht(2)
            elif value == "Licht":
                self.__selected_zonnescherm.set_licht(3)
            elif value == "Veel licht":
                self.__selected_zonnescherm.set_licht(4)

    def __receive_gem_temperatuur(temperaturen):
        # TODO: Verander deze functie
        pass

    def __receive_gem_lichtintensiteiten(lichtintensiteiten):
        # TODO: Verander deze functie
        pass

    def __receive_status(self, status):
        """
        Ontvangt de status van het zonnescherm en geeft het als tekst weer.
        :param status: de status van het zonnescherm.
        """
        self.__open_sluit_button["text"] = "Sluit zonnescherm" if status else "Open zonnescherm"
        self.__status_zonnescherm_label[
            "text"] = "Status: zonnescherm is open" if status else "Status: zonnescherm is dicht"

    def set_update_CB(self, callback, milliseconds):
        """
        Maakt een callback voor __update.
        :param callback:
        :param milliseconds: tijd in miliseconden.
        """
        self.__update_CB = callback
        self.__update_milliseconds = milliseconds

    def __update(self):
        """
        Update de gui als er bijvoorbeeld een zonnescherm word toegevoegd.
        """
        if self.__update_CB is not None:
            self.__update_CB()
        self.__canvas.after(self.__update_milliseconds, self.__update)

    def start(self):
        """
        Start de gui.
        """
        self.__canvas.after(self.__update_milliseconds, self.__update)
        self.__root.mainloop()

    def add_zonnescherm(self, zonnescherm):
        """
        Voegt een zonnescherm toe.
        :param zonnescherm: de naam van het zonnescherm dat moet worden toegevoegd.
        """
        self.__zonneschermen.append(zonnescherm)
        self.__devices.append(zonnescherm.get_name())
        self.__refresh_zonneschermen()

    def remove_zonnescherm(self, name):
        """
        Verwijdert een zonnescherm.
        :param name: de naam van het zonnescherm dat moet worden verwijdert.
        """
        self.__devices.remove(name)
        for zonnescherm in self.__zonneschermen:
            if zonnescherm.get_name() == name:
                self.__zonneschermen.remove(zonnescherm)
                break
        self.__refresh_zonneschermen()

    def __refresh_zonneschermen(self):
        """
        Refreshed de lijst met zonneschermen.
        """
        self.__selected_device.set("Geen Zonnescherm")
        self.__zonnescherm_opties["menu"].delete(0, 'end')
        for zonnescherm in self.__devices:
            self.__zonnescherm_opties["menu"].add_command(label=zonnescherm,
                                                          command=_setit(self.__selected_device, zonnescherm,
                                                                         self.__select_zonnescherm))

    def __draw_grafiek_temp(self, temperaturen):
        """
        Tekent de grafiek met temperaturen.
        :param temperaturen: lijst van temperaturen ex: [10, 20, 40, -5] etc...
        """
        punten = []
        for index, temp in enumerate(temperaturen):
            temp = (temp + 10) / 50
            punt_op_y = 550 - (500 * temp)
            punt_op_x = ((index + 1) * 50)
            punten.append([punt_op_x, punt_op_y])
        for index in range(len(punten)):
            if index is not 0:
                self.__canvas.create_line(punten[index][0], punten[index][1], punten[index - 1][0], punten[index - 1][1],
                        fill="blue", tags="temp")

    def __draw_grafiek_lichtintensiteiten(self, licht_intensiteiten):
        """
        Tekent de grafiek met lichtintensiteiten.
        :param licht_intensiteiten: lijst van licht intensiteiten ex: ["licht", "schemerig", "neutraal"] etc...
        """
        y_waarde_bij_licht = {
            "veel licht" : 50,
            "licht" : 175,
            "neutraal" : 300,
            "schemerig" : 425,
            "donker" : 550
        }
        punten = []
        for index, licht in enumerate(licht_intensiteiten):
            punt_op_y = y_waarde_bij_licht[licht]
            punt_op_x = 625 + ((index + 1) * 50)
            punten.append([punt_op_x, punt_op_y])
        for index in range(len(punten)):
            if index is not 0:
                self.__canvas.create_line(punten[index][0], punten[index][1], punten[index - 1][0], punten[index - 1][1],
                        fill="blue", tags="temp")
