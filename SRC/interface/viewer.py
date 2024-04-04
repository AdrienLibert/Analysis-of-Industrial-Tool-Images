from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\nOuvrir une image pour commencer")
        self.setMinimumSize(1, 1)  # Évite que le QLabel ne devienne trop grand
        self.setPixmap(QPixmap("image7.jpg"))

    def setImage(self, cheminImage):
        pixmap = QPixmap(cheminImage)
        self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, event):
        if self.pixmap:  # Accès à la propriété pixmap, pas appel de fonction
            self.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

