from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap,QPainter, QPen, QPixmap, QImage
from utils.diametre_pas import demander_type_filetage, pas_metrique,trouver_entiers_adjacents,load_csvgaz_to_df,select_possible_pitches
from utils.draw_tooth_pattern import draw_tooth_pattern

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
        
        self.layout = QVBoxLayout(self)

        self.imageLabel = QLabel("Alignez le motif de pas avec le filetage:")
        self.layout.addWidget(self.imageLabel)
        
        self.graphicsView = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        
        self.pixmapItem = QGraphicsPixmapItem(QPixmap(image_path))
        self.scene.addItem(self.pixmapItem)
        self.layout.addWidget(self.graphicsView)

        self.pitchComboBox = QComboBox()
        self.populatePitchPatterns()
        self.pitchComboBox.currentIndexChanged.connect(self.displaySelectedPitchPattern)
        self.layout.addWidget(self.pitchComboBox)

        self.confirmButton = QPushButton("Confirmer le pas")
        self.confirmButton.clicked.connect(self.confirmPitch)
        self.layout.addWidget(self.confirmButton)

    def getPossiblePitches(self):
        pitches = []
        if self.type == 'métrique':
            inf, sup = trouver_entiers_adjacents(self.diameter)
            pitches = pas_metrique(inf, sup)  # Assuming this returns a list of pitches
        elif self.type == 'gaz':
            df = load_csvgaz_to_df()
            pitches = select_possible_pitches(df, self.diameter)
        return pitches
    
    def populatePitchPatterns(self):
        pitches = self.getPossiblePitches()
        print(pitches)
        self.pattern_images = {}
        for pitch in pitches:
            pixmap = self.createPitchPixmap(pitch)
            self.pattern_images[pitch] = pixmap
            self.pitchComboBox.addItem(str(pitch), pixmap)

    def createPitchPixmap(self, pitch):
        # Générer le motif à l'aide de la fonction draw_tooth_pattern
        rotation = False   # Vous pouvez choisir de faire pivoter le motif ou non
        pattern_image = draw_tooth_pattern(self.size_pixels, pitch, rotation)

        # Convertir le numpy array (pattern_image) en QPixmap
        height, width = pattern_image.shape
        bytes_per_line = width
        qimg = QImage(pattern_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        return QPixmap.fromImage(qimg)
        
    def displaySelectedPitchPattern(self, index):
        pitch = self.pitchComboBox.itemText(index)
        pattern_pixmap = self.pitchComboBox.itemData(index)

        # Clear any existing pattern items first
        for item in self.scene.items():
            if isinstance(item, QGraphicsPixmapItem) and item is not self.pixmapItem:
                self.scene.removeItem(item)

        # Create and display the new pattern item
        self.patternItem = QGraphicsPixmapItem(pattern_pixmap)
        self.patternItem.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        self.scene.addItem(self.patternItem)
        self.patternItem.setPos(50, 50)  # Initial position, adjust as necessary

    def confirmPitch(self):
        selectedPattern = self.pitchComboBox.currentText()
        self.pitchConfirmed.emit(selectedPattern)
        self.accept()
