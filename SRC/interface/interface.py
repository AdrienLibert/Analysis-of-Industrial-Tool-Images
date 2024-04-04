from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from viewer import ImageViewer

class InterfacePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualiseur de Filetage")

        self.resize(1000, 700)
        
        # Créer le widget central et le layout principal
        widgetCentral = QWidget()
        self.setCentralWidget(widgetCentral)
        layoutPrincipal = QVBoxLayout()
        widgetCentral.setLayout(layoutPrincipal)
        
        # Ajouter le visualiseur d'image
        self.viewer = ImageViewer()
        layoutPrincipal.addWidget(self.viewer)
