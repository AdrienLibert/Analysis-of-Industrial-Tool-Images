from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem,QMessageBox, QAction,QMenu
from PyQt5.QtCore import Qt , QRectF, QSizeF, QFileInfo
from PyQt5.QtGui import  *
import cv2


class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__()

        self.scene_ = QGraphicsScene() #Scene de la classe
        self.setScene(self.scene_) # Associe la scène à la vue

        self.setFocusPolicy(Qt.WheelFocus) # Définit le focus sur la molette
        self.setDragMode(QGraphicsView.ScrollHandDrag) # Active le défilement de la vue en mode "main"

        # Initialiser des variables des méthodes
        self.image = None # Image affichée dans la vue
        self.min_zoom_factor = None  # Facteur de zoom minimal


    def wheelEvent(self, event): #Evenement de la molette de la souris sur la scène
        if event.modifiers() == Qt.ControlModifier:
            delta = event.angleDelta().y() / 120
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super().wheelEvent(event)

    def zoom_in(self):
        if self.image != None:
            self.zoom_factor = 1.1
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
            self.scale(self.zoom_factor, self.zoom_factor)

    def zoom_out(self):
        if self.image != None:
            self.zoom_factor = 0.9
            self.current_zoom = self.transform().m11()
            if self.current_zoom >= self.min_zoom_factor:
                self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
                self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
                self.scale(self.zoom_factor, self.zoom_factor)

    def openPicture(self, file_path):

        self.image = QPixmap(file_path) # Charge l'image à partir du path

        if self.image.isNull():
            QMessageBox.warning(self, "Error", "Failed to load image.")
        else:
            item = QGraphicsPixmapItem(self.image)
            self.scene_.clear()
            self.scene_.addItem(item)

            self.zoom_factor = 1.0

            self.setSceneRect(QRectF(self.image.rect()))
            self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

            self.min_zoom_factor = self.transform().m11() #Valeur du zoom initial a l'ouverture de l'image