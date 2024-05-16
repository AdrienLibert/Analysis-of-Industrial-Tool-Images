import sys
from PyQt5.QtWidgets import QApplication
from Interface import MainWindow
from utils.diametre_pas import demander_type_filetage, pas_metrique, trouver_entiers_adjacents

def main():
    # Demander à l'utilisateur de spécifier le type de filetage (métrique, gaz, etc.)
    type = demander_type_filetage()

    # Créer une application 
    app = QApplication([])

    # Initialiser la fenêtre principale avec le type de filetage spécifié
    fenetre = MainWindow(type)

    # Connecter le signal de mesure de distance à la fonction de traitement
    fenetre.distanceMeasured.connect(lambda distance: process_distance(distance, type))

    # Afficher la fenêtre principale et démarrer la boucle d'événements de l'application
    fenetre.show()
    app.exec_()

def process_distance(distance, type):
    # Trouver les entiers adjacents pour la distance donnée, utile pour calculer le pas
    inf, sup = trouver_entiers_adjacents(distance)
    
    # Afficher les valeurs inférieure et supérieure trouvées
    print(f"[{inf} {sup}]")
    
    # Si le type de filetage est métrique, appliquer la logique de calcul du pas
    if type == 'métrique':
        pas_metrique(inf, sup)
        
if __name__ == "__main__":
    main()
