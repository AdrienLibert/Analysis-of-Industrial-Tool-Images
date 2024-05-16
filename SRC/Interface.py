import sys
import os
from InterfacePrincipale import InterfacePrincipale
from PitchSelection import PitchMatchingDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QStackedLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    # Signal personnalisé pour notifier une distance mesurée
    distanceMeasured = pyqtSignal(float)

    def __init__(self, type=None):
        super().__init__()
        self.type = type
        self.initUI()

    def initUI(self):
        # Configuration initiale de l'interface utilisateur
        self.setWindowTitle('Reconnaissance d’images d’outils industriels')
        self.setWindowIcon(QIcon('Ressources/Icone/icone_1.jpg'))
        self.setGeometry(100, 100, 800, 600)

        # Configuration de l'image par défaut
        self.defaultPixmap = QPixmap(400, 400)
        self.defaultPixmap.fill(Qt.lightGray)
        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(self.defaultPixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setStyleSheet("QLabel { background-color : white; border: 2px dashed #C0C0C0; }")

        # Configuration du conteneur pour l'image
        self.imageContainer = QWidget(self)
        stackedLayout = QStackedLayout(self.imageContainer)
        self.imageContainer.setLayout(stackedLayout)
        stackedLayout.addWidget(self.imageLabel)

        # Configuration des labels et boutons
        self.label = QLabel('Cliquez sur "Charger Image" pour commencer.', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")
        self.btnLoad = QPushButton('Charger Image', self)
        self.btnLoad.clicked.connect(self.loadImage)
        self.btnLoad.setStyleSheet("QPushButton { padding: 10px; font-size: 16px; }")
        self.btnAnalyse = QPushButton('Analyser Image', self)
        self.btnAnalyse.clicked.connect(self.analyser_image)
        self.btnAnalyse.setStyleSheet("QPushButton { padding: 10px; font-size: 16px; }")

        # Assemblage du layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.imageContainer)
        layout.addWidget(self.btnLoad)
        layout.addWidget(self.btnAnalyse)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def getReferenceSize(self):
        # Obtenir la taille de référence de l'utilisateur
        size, ok = QInputDialog.getDouble(self, "Taille de la pièce de référence", "Entrez la taille en mm de votre pièce de référence:", decimals=2)
        if ok:
            self.referenceObjectMM = size
        return ok

    def loadImage(self):
        # Fonction pour charger une image depuis le disque
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        database_path = os.path.join(base_dir, 'Ressources', 'Database')
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', database_path, "Image files (*.jpg *.png)")
        if fname:
            self.imagePath = fname
            self.imageLabel.setPixmap(QPixmap(fname).scaled(400, 400, Qt.KeepAspectRatio))
            self.label.setText('Image chargée. Cliquez sur "Analyser Image" pour procéder.')
            self.loadedPixmap = QPixmap(fname)

    def analyser_image(self):
        # Analyser l'image chargée
        if hasattr(self, 'loadedPixmap'):
            self.getReferenceSize()
            self.fenetre = InterfacePrincipale(self.imagePath, self.referenceObjectMM)
            self.fenetre.size_pixelsReady.connect(self.process_size_pixels)
            self.fenetre.distanceReady.connect(self.process_distance)
            self.fenetre.show()
        else:
            QMessageBox.warning(self, 'Aucune Image', 'Veuillez charger une image avant d\'analyser.')

    def process_size_pixels(self, size_pixels):
        # Traitement de la taille en pixels
        self.size_pixels = size_pixels

    def process_distance(self, distance):
        # Traitement de la distance mesurée
        rounded_distance = round(distance, 1)
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle('Analyse Terminée')
        msgBox.setText(f'L’analyse de l’image a été réalisée avec succès. Distance mesurée: {rounded_distance} mm')
        msgBox.addButton('OK', QMessageBox.AcceptRole)
        msgBox.addButton('Recommencer la mesure', QMessageBox.RejectRole)
        result = msgBox.exec_()
        if result == QMessageBox.AcceptRole:
            self.fenetre.close()
            self.showPitchSelectionWindow(rounded_distance)
        elif result == QMessageBox.RejectRole:
            self.fenetre.viewer.reset()

    def showPitchSelectionWindow(self, diameter):
        # Afficher la fenêtre de sélection du pas
        self.pitchDialog = PitchMatchingDialog(diameter, self.imagePath, self.referenceObjectMM, self.type, self.size_pixels, self)
        self.pitchDialog.exec_()
