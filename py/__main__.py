from GUI import *
from Zonnescherm_loader import *

def main():
    gui = GUI()
    zonnescherm_loader = Zonnescherm_loader()

    # Set de callbacks voor de zonnescherm_loader. Wanneer er een zonnescherm wordt aangesloten of verwijdert geeft de zonnescherm_loader dit door aan de gui
    zonnescherm_loader.get_zonnescherm_CB(gui.add_zonnescherm)
    zonnescherm_loader.remove_zonnescherm_CB(gui.remove_zonnescherm)

    gui.start()


if __name__ == "__main__":
    main()
