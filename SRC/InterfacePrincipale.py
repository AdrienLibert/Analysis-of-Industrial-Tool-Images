from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PointDrawer import PointDrawer

class InterfacePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualiseur de Filetage")

        #self.resize(1000, 700)
        
        widgetCentral = QWidget()
        self.setCentralWidget(widgetCentral)
        layoutPrincipal = QVBoxLayout()
        widgetCentral.setLayout(layoutPrincipal)
        
        self.viewer = PointDrawer()
        layoutPrincipal.addWidget(self.viewer)
