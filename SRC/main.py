import sys
from PyQt5.QtWidgets import QApplication
from InterfacePrincipale import InterfacePrincipale
from utils.diametre_pas import demander_type_filetage
from utils.diametre_pas import pas_metrique
from utils.diametre_pas import trouver_entiers_adjacents

def main():
    type = demander_type_filetage()
    app = QApplication([])
    fenetre = InterfacePrincipale()
    
    fenetre.distanceReady.connect(lambda distance: process_distance(distance, type))

    fenetre.show()
    app.exec_()

def process_distance(distance,type):
    inf, sup = trouver_entiers_adjacents(distance)
    print(f"[{inf} {sup}]")
    if type == 'métrique': #implémenter logique du pattern
        pas_metrique(inf, sup)

if __name__ == "__main__":
    main()