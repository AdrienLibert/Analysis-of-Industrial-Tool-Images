from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap,QPainter, QPen, QPixmap, QImage
from utils.diametre_pas import demander_type_filetage, pas_metrique,trouver_entiers_adjacents,load_csvgaz_to_df,select_possible_pitches
from utils.draw_tooth_pattern import draw_tooth_pattern
from utils.diametre_monnaie import conversion_piece
from CustomGraphicsView import CustomGraphicsView
class PitchMatchingDialog(QDialog):
    pitchConfirmed = pyqtSignal(str)

    def __init__(self,diameter=None,image_path=None,reference_object_mm=None,type=None,size_pixels=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matching du pas")
        self.image_path = image_path
        self.diameter = diameter
        self.reference_object_mm = reference_object_mm
        self.type=type
        self.size_pixels=size_pixels

        self.patternItem = None
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.imageLabel = QLabel("Alignez le motif de pas avec le filetage:")
        self.imageLabel.setFixedHeight(20)
        layout.addWidget(self.imageLabel)
        

        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)

        self.graphicsView = CustomGraphicsView()
        self.graphicsView.openPicture(image_path)
        header_layout.addWidget(self.graphicsView)

        self.pitchComboBox = QComboBox()
        self.populatePitchPatterns()
        self.pitchComboBox.currentIndexChanged.connect(self.displaySelectedPitchPattern)
        header_layout.addWidget(self.pitchComboBox)

        self.confirmButton = QPushButton("Confirmer le pas")
        self.confirmButton.clicked.connect(self.confirmPitch)
        layout.addWidget(self.confirmButton)

    def getPossiblePitches(self):
        pitches = []
        if self.type == 'métrique':
            inf, sup = trouver_entiers_adjacents(self.diameter)
            print(inf,sup)
            pitches = pas_metrique(inf, sup) 
            print(pitches)
        elif self.type == 'gaz':
            df = load_csvgaz_to_df()
            pitches = select_possible_pitches(df, self.diameter)
        return pitches
    
    def populatePitchPatterns(self):
        pitches = self.getPossiblePitches()
        self.pattern_images = {}
        for pitch in pitches:
            pixmap = self.createPitchPixmap(pitch)
            self.pattern_images[pitch] = pixmap
            self.pitchComboBox.addItem(str(pitch), pixmap)

    def createPitchPixmap(self, pitch):
        rotation = False
        pattern_image = draw_tooth_pattern(self.size_pixels, 25.4 / pitch, rotation)

        height, width, channels = pattern_image.shape
        bytes_per_line = 4 * width  # 4 canaux (RGBA), donc 4 bytes par pixel

        # Créer un QImage qui utilise le format correct pour une image RGBA
        qimg = QImage(pattern_image.data, width, height, bytes_per_line, QImage.Format_ARGB32)

        # Convertir le QImage en QPixmap pour l'affichage
        return QPixmap.fromImage(qimg)
        
    def displaySelectedPitchPattern(self, index):
        # Supprimez l'ancien motif si présent
        if self.patternItem is not None:
            self.graphicsView.scene().removeItem(self.patternItem)
            self.patternItem = None  # Réinitialiser la référence

        # Récupérez le pixmap du motif sélectionné
        pitch = self.pitchComboBox.itemText(index)
        pattern_pixmap = self.pitchComboBox.itemData(index)

        # Créez un nouvel élément de motif et ajoutez-le à la scène
        self.patternItem = QGraphicsPixmapItem(pattern_pixmap)
        self.patternItem.setFlag(QGraphicsPixmapItem.ItemIsMovable)  # Permettre de déplacer l'élément
        self.graphicsView.scene().addItem(self.patternItem)

        # Positionnez le motif sur l'image
        # Ajustez la position initiale si nécessaire
        self.patternItem.setPos(50, 50)  # Exemple de positionnement initial

    def confirmPitch(self):
        selectedPattern = self.pitchComboBox.currentText()
        self.pitchConfirmed.emit(selectedPattern)
        self.accept()