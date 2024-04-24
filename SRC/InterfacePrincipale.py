from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from PointDrawer import PointDrawer

class InterfacePrincipale(QMainWindow):
    distanceReady = pyqtSignal(float)

    def __init__(self,image_path=None,reference_object_mm=None):
        super().__init__()
        self.setWindowTitle("Visualiseur de Filetage")

        widgetCentral = QWidget()
        self.setCentralWidget(widgetCentral)
        layoutPrincipal = QVBoxLayout()
        widgetCentral.setLayout(layoutPrincipal)
        
        self.viewer = PointDrawer(image_path,reference_object_mm)
        layoutPrincipal.addWidget(self.viewer)

        self.bouton_mesure = QPushButton("Confirmer la mesure", self)
        layoutPrincipal.addWidget(self.bouton_mesure)
        self.bouton_mesure.clicked.connect(self.emitDistance)

    def emitDistance(self):
        distance = self.viewer.get_last_measured_distance()
        if distance is not None:
            self.distanceReady.emit(distance)
