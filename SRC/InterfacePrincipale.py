from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from PointDrawer import PointDrawer

class InterfacePrincipale(QMainWindow):
    # Signaux pour notifier la distance mesurée et la taille en pixels
    distanceReady = pyqtSignal(float)
    size_pixelsReady = pyqtSignal(float)

    def __init__(self, image_path=None, reference_object_mm=None):
        super().__init__()
        # Configuration de la fenêtre principale
        self.setWindowTitle("Visualiseur de Filetage")

        # Création et configuration du widget central
        widgetCentral = QWidget()
        self.setCentralWidget(widgetCentral)
        layoutPrincipal = QVBoxLayout()
        widgetCentral.setLayout(layoutPrincipal)

        # Ajout du visualiseur d'image, où les mesures seront effectuées
        self.viewer = PointDrawer(image_path, reference_object_mm)
        layoutPrincipal.addWidget(self.viewer)

        # Bouton pour confirmer la mesure de la distance entre deux points
        self.bouton_mesure = QPushButton("Confirmer la mesure", self)
        layoutPrincipal.addWidget(self.bouton_mesure)
        self.bouton_mesure.clicked.connect(self.emitDistance)

    def emitDistance(self):
        # Récupération de la dernière distance mesurée et émission des signaux correspondants
        distance, size_pixels = self.viewer.get_last_measured_distance()
        if distance is not None:
            self.size_pixelsReady.emit(size_pixels)
            self.distanceReady.emit(distance)
