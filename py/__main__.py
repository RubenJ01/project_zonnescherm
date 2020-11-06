from GUI import *
from zonnescherm_loader import *

def main():
    gui = GUI()
    zonnescherm_loader = ZonneschermLoader()

    # Set de callbacks voor de zonnescherm_loader.
    # Wanneer er een zonnescherm wordt aangesloten of verwijdert geeft de zonnescherm_loader dit door aan de gui
    zonnescherm_loader.get_zonnescherm_CB(gui.add_zonnescherm)
    zonnescherm_loader.remove_zonnescherm_CB(gui.remove_zonnescherm)
    gui.draw_grafiek_lichtintensiteiten([0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    gui.draw_grafiek_temp([0, 5, 10, 15, 20, 25, 30, 35, 40, 5])
    gui.draw_grafiek_temp([10, 5, 15, 20, 5, 40, 0, 6, 9, 12])
    gui.draw_grafiek_lichtintensiteiten([4, 3, 2, 1, 0, 4, 3, 2, 1, 0])

    def loop():
        zonnescherm_loader.update()

    gui.set_update_CB(loop, 1000) # Call loop every second
    gui.start()


if __name__ == "__main__":
    main()
