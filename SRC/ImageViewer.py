from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# image_path = "Ressources/Database/image7.jpg"
# class ImageViewer(QLabel):
#     def __init__(self):
#         super().__init__()
#         self.setAlignment(Qt.AlignCenter)
#         self.setText("\n\nOuvrir une image pour commencer")
#         self.setMinimumSize(1, 1)  # Évite que le QLabel ne devienne trop grand
#         self.setPixmap(QPixmap("Ressources\Database\image7.jpg"))

#     def setImage(self, cheminImage):
#         self.pixmapOriginal = QPixmap(cheminImage)
#         self.zoomFactor = 1.0  # Réinitialiser le zoom pour une nouvelle image
#         self.updateImageDisplay()

#     def updateImageDisplay(self):
#         if self.pixmapOriginal:
#             size = self.pixmapOriginal.size()
#             size *= self.zoomFactor  # Appliquer le facteur de zoom
#             pixmapZoomed = self.pixmapOriginal.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#             self.setPixmap(pixmapZoomed)

    # def setImage(self, cheminImage):
    #     pixmap = QPixmap(cheminImage)
    #     self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # def resizeEvent(self, event):
    #     if self.pixmap:  # Accès à la propriété pixmap, pas appel de fonction
    #         self.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

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