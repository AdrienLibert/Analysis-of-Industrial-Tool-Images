import sys
from InterfacePrincipale import InterfacePrincipale
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QStackedLayout # type: ignore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import pyqtSignal



class MainWindow(QMainWindow):
    distanceMeasured = pyqtSignal(float)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Reconnaissance d’images d’outils industriels')
        self.setWindowIcon(QIcon('Ressources/Icone/icone_1.jpg'))  # Icône de la fenêtre
        self.setGeometry(100, 100, 800, 600)  # Position et taille de la fenêtre : x, y, largeur, hauteur

        # Définir une image par défaut avec une icône de téléchargement
        self.defaultPixmap = QPixmap(400, 400)
        self.defaultPixmap.fill(Qt.lightGray)  # Remplit l'image par défaut de gris clair
        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(self.defaultPixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setStyleSheet("QLabel { background-color : white; border: 2px dashed #C0C0C0; }")

        # Conteneur pour superposer l'icône au centre
        self.imageContainer = QWidget(self)
        stackedLayout = QStackedLayout(self.imageContainer)
        self.imageContainer.setLayout(stackedLayout)
        
        # Ajout de l'imageLabel et de l'uploadIcon au layout empilé
        stackedLayout.addWidget(self.imageLabel)

        self.label = QLabel('Cliquez sur "Charger Image" pour commencer.', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")

        self.btnLoad = QPushButton('Charger Image', self)
        self.btnLoad.clicked.connect(self.loadImage)
        self.btnLoad.setStyleSheet("QPushButton { padding: 10px; font-size: 16px; }")

        self.btnAnalyse = QPushButton('Analyser Image', self)
        self.btnAnalyse.clicked.connect(self.analyser_image)
        self.btnAnalyse.setStyleSheet("QPushButton { padding: 10px; font-size: 16px; }")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.imageContainer)
        layout.addWidget(self.btnLoad)
        layout.addWidget(self.btnAnalyse)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def getReferenceSize(self):
        size, ok = QInputDialog.getDouble(self, "Taille de la pièce de référence", "Entrez la taille en mm de votre pièce de référence:", decimals=2)
        if ok:
            self.referenceObjectMM = size  # Sauvegarder la taille si l'utilisateur clique sur OK
        return ok

    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', r'Analysis-of-Industrial-Tool-Images\Ressources\Database', "Image files (*.jpg *.png)")
        if fname:
            self.imagePath = fname
            self.imageLabel.setPixmap(QPixmap(fname).scaled(400, 400, Qt.KeepAspectRatio))
            self.label.setText('Image chargée. Cliquez sur "Analyser Image" pour procéder.')
            self.loadedPixmap = QPixmap(fname)  # Stocker le QPixmap original

    def analyser_image(self):
        if hasattr(self, 'loadedPixmap'):  # Vérifier si une image a été chargée
            self.getReferenceSize()
            self.fenetre = InterfacePrincipale(self.imagePath,self.referenceObjectMM)
            self.fenetre.viewer.setImage(self.loadedPixmap)
            self.fenetre.distanceReady.connect(self.process_distance)
            self.fenetre.show()
        else:
            QMessageBox.warning(self, 'Aucune Image', 'Veuillez charger une image avant d\'analyser.')

    def process_distance(self, distance):
        rounded_distance = round(distance, 1)
        QMessageBox.information(self, 'Analyse Terminée', f'L’analyse de l’image a été réalisée avec succès. Distance mesurée: {rounded_distance} mm')
        self.distanceMeasured.emit(rounded_distance)