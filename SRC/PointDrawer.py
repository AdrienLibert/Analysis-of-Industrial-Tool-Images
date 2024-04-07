import math
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint, QLineF
from ImageViewer import ImageViewer
from utils.diametre_monnaie import conversion_piece


image_path = "Ressources\Database\image7.jpg"
reference_object_mm = 22.6

class PointDrawer(ImageViewer):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap(image_path)
        self.setPixmap(self.pixmap)
        self.original_width = self.pixmap.width()
        self.original_height = self.pixmap.height()
        self.points = []

    def addPoint(self, x, y):
        if len(self.points) >= 2:
            self.points.pop(0)
        self.points.append(QPoint(x, y))
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.red, 10, Qt.SolidLine)
        painter.setPen(pen)
        for point in self.points:
            painter.drawPoint(point)
        if len(self.points) == 1:
            line_end_point = QPoint(self.width(), self.points[0].y())
            painter.drawLine(QLineF(self.points[0], line_end_point))
        elif len(self.points) == 2:
            painter.drawLine(QLineF(self.points[0], self.points[1]))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.addPoint(event.x(), event.y())
            if len(self.points) > 1:
                distance_pixels = self.calculateDistance()
                displayed_image_width = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation).width() # Largeur de l'image affiché
                resize_factor = displayed_image_width / self.original_width # Calcule le facteur de redimensionnement en divisant la largeur de l'image affichée par la largeur originale de l'image.              
                distance_real = distance_pixels / resize_factor # Convertir la distance en pixels mesurée sur l'image redimensionnée en distance "réelle" en pixels sur l'image originale.
                size_pixels = conversion_piece(image_path, reference_object_mm) #Fonction de conversion
                distance_mm = distance_real * size_pixels # Calcul distance final
                print(f"Distance entre les deux derniers points : {distance_mm} mm")

    def calculateDistance(self):
        if len(self.points) >= 2:
            p1 = self.points[-2]
            p2 = self.points[-1]
            return math.sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)
        return 0
