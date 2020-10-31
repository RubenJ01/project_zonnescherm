from GUI import *
from zonnescherm_loader import *
from zonnescherm import *


def main():
    gui = GUI()
    zonnescherm_loader = ZonneschermLoader()

    # Set de callbacks voor de zonnescherm_loader.
    # Wanneer er een zonnescherm wordt aangesloten of verwijdert geeft de zonnescherm_loader dit door aan de gui
    zonnescherm_loader.get_zonnescherm_CB(gui.add_zonnescherm)
    zonnescherm_loader.remove_zonnescherm_CB(gui.remove_zonnescherm)

    gui.add_zonnescherm(Zonnescherm("Scherm 1"))
    gui.add_zonnescherm(Zonnescherm("Scherm 2"))

    gui.start()


if __name__ == "__main__":
    main()
