from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\nOuvrir une image pour commencer")
        self.setMinimumSize(1, 1)
        self.pixmapOriginal = None
        self.original_width = 1
        self.original_height = 1

    def setImage(self, cheminImage):
        self.pixmapOriginal = QPixmap(cheminImage)
        if not self.pixmapOriginal.isNull():
            self.original_width = self.pixmapOriginal.width()
            self.original_height = self.pixmapOriginal.height()
            self.updateImageDisplay()
        else:
            self.setText("Failed to load image.")

    def updateImageDisplay(self):
        if self.pixmapOriginal:
            pixmapResized = self.pixmapOriginal.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(pixmapResized)

    def resizeEvent(self, event):
        self.updateImageDisplay()
        super().resizeEvent(event)