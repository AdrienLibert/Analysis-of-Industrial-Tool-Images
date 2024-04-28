from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

class PitchMatchingDialog(QDialog):
    pitchConfirmed = pyqtSignal(str)

    def __init__(self,diameter=None,image_path=None,reference_object_mm=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matching du pas")
        self.image_path = image_path
        self.diameter = diameter
        self.reference_object_mm = reference_object_mm
        
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

    def populatePitchPatterns(self):
        pitch_patterns = ["Pattern 1", "Pattern 2", "Pattern 3"] 
        for pattern in pitch_patterns:
            self.pitchComboBox.addItem(pattern)
    
    def displaySelectedPitchPattern(self, index):
        selected_pattern = self.pitchComboBox.currentText()
        pattern_pixmap = self.getPatternPixmap(selected_pattern)
        self.patternItem = QGraphicsPixmapItem(pattern_pixmap)
        self.patternItem.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        self.scene.addItem(self.patternItem)

    # def getPatternPixmap(self, pattern_name):
    #     return QPixmap(f"path/to/{pattern_name}.png")

    def confirmPitch(self):
        selectedPattern = self.pitchComboBox.currentText()
        self.pitchConfirmed.emit(selectedPattern)
        self.accept()
