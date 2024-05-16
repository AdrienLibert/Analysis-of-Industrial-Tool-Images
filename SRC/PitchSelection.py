from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QPixmap, QImage
from utils.diametre_pas import demander_type_filetage, pas_metrique, trouver_entiers_adjacents, load_csvgaz_to_df, select_possible_pitches
from utils.draw_tooth_pattern import draw_tooth_pattern
from utils.diametre_monnaie import conversion_piece
from CustomGraphicsView import CustomGraphicsView

class PitchMatchingDialog(QDialog):
    pitchConfirmed = pyqtSignal(str)  # Signal émis lorsque le pas est confirmé

    def __init__(self, diameter=None, image_path=None, reference_object_mm=None, type=None, size_pixels=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matching du pas")
        self.image_path = image_path
        self.diameter = diameter
        self.reference_object_mm = reference_object_mm
        self.type = type
        self.size_pixels = size_pixels

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
        # Récupère les pas possibles en fonction du type de filetage
        pitches = []
        if self.type == 'métrique':
            pitches_dict = pas_metrique(self.diameter) 
            for size, pas_list in pitches_dict.items():
                for pas in pas_list:
                    pitches.append((size, pas))
            print(pitches)
        elif self.type == 'gaz':
            df = load_csvgaz_to_df()
            pitches = select_possible_pitches(df, self.diameter)
        return pitches
    
    def populatePitchPatterns(self):
        # Remplit le comboBox avec les motifs de pas disponibles
        if self.type == 'gaz':
            pitches = self.getPossiblePitches()
            self.pattern_images = {}
            for pitch in pitches:
                pixmap = self.createPitchPixmap(25.4/pitch)
                self.pattern_images[pitch] = pixmap
                self.pitchComboBox.addItem(str(pitch), pixmap)
        elif self.type == 'métrique':
            pitches = self.getPossiblePitches()
            self.pattern_images = {}
            for size, pas in pitches:
                pixmap = self.createPitchPixmap(pas/100)
                self.pattern_images[(size, pas)] = pixmap
                self.pitchComboBox.addItem(f"{size}, {pas}", pixmap)

    def createPitchPixmap(self, pitch):
        # Crée un pixmap pour chaque pas spécifié
        rotation = False
        pattern_image = draw_tooth_pattern(self.size_pixels, pitch, rotation)
        height, width, channels = pattern_image.shape
        bytes_per_line = 4 * width
        qimg = QImage(pattern_image.data, width, height, bytes_per_line, QImage.Format_ARGB32)
        return QPixmap.fromImage(qimg)
        
    def displaySelectedPitchPattern(self, index):
        # Affiche le motif de pas sélectionné dans la vue graphique
        if self.patternItem is not None:
            self.graphicsView.scene().removeItem(self.patternItem)
            self.patternItem = None
        pitch = self.pitchComboBox.itemText(index)
        pattern_pixmap = self.pitchComboBox.itemData(index)
        self.patternItem = QGraphicsPixmapItem(pattern_pixmap)
        self.patternItem.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        self.graphicsView.scene().addItem(self.patternItem)

        # Positionne le motif de la dent au milieu de la vue graphique
        view_width = self.graphicsView.scene().width()
        view_height = self.graphicsView.scene().height()
        pixmap_width = pattern_pixmap.width()
        pixmap_height = pattern_pixmap.height()
        self.patternItem.setPos((view_width - pixmap_width) / 2, (view_height - pixmap_height) / 2)

    def confirmPitch(self):
        # Confirme le choix du pas et émet le signal correspondant
        selectedPattern = self.pitchComboBox.currentText()
        self.pitchConfirmed.emit(selectedPattern)
        self.accept()
        if self.type == 'métrique':
            QMessageBox.information(self, "Confirmation du pas", f"Le diamètre est de {self.diameter} mm avec un pas de {selectedPattern}.")
        elif self.type == 'gaz':
            QMessageBox.information(self, "Confirmation du pas", f"Le diamètre est de {self.diameter} mm avec {selectedPattern} filet sur un pouce (25,4 mm).")
