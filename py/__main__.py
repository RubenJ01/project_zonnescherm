from GUI import *

def ontvangZonnescherm(value):
    print(value)

def ontvangAuto(value):
    print(value)

def ontvangOpenSluit(value):
    print(value)

def ontvangOprol(value):
    print(value)

def ontvangUitrol(value):
    print(value)

def ontvangMinTemperatuur(value):
    print(value)

def ontvangMaxTemperatuur(value):
    print(value)

def ontvangLicht(value):
    print(value)


def main():
    gui = GUI()
    gui.setZonneschermCB(ontvangZonnescherm)
    gui.setAutoCB(ontvangAuto)
    gui.setOpenSluitCB(ontvangOpenSluit)
    gui.setOprolCB(ontvangOprol)
    gui.setUitrolCB(ontvangUitrol)
    gui.setMinTemperatuurCB(ontvangMinTemperatuur)
    gui.setMaxTemperatuurCB(ontvangMaxTemperatuur)
    gui.setLichtCB(ontvangLicht)
    gui.start()


if __name__ == "__main__":
    main()