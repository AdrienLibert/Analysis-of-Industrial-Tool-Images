import math
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint, QLineF
from ImageViewer import ImageViewer
from utils.diametre_monnaie import conversion_piece


class PointDrawer(ImageViewer):
    def __init__(self,image_path,reference_object_mm):
        super().__init__()
        self.last_measured_distance_mm = None
        self.points = []
        self.image_path = image_path 
        self.reference_object_mm = reference_object_mm

    def addPoint(self, x, y):
        if len(self.points) >= 2:
            self.points.pop(0)
        self.points.append(QPoint(x, y))
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.pixmapOriginal:
            return
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
        if event.button() == Qt.LeftButton and not self.pixmapOriginal.isNull():
            self.addPoint(event.x(), event.y())
            if len(self.points) > 1:
                distance_pixels = self.calculateDistance()
                displayed_image_width = self.pixmap().size().width()
                resize_factor = displayed_image_width / self.original_width
                distance_real = distance_pixels / resize_factor
                self.size_pixels = conversion_piece(self.image_path, self.reference_object_mm)
                distance_mm = distance_real * self.size_pixels
                print(f"Distance entre les deux derniers points : {distance_mm} mm")
                self.last_measured_distance_mm = distance_mm

    def calculateDistance(self):
        if len(self.points) >= 2:
            p1 = self.points[-2]
            p2 = self.points[-1]
            return math.sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)

    def get_last_measured_distance(self):
        return self.last_measured_distance_mm, self.size_pixels
    
    def reset(self):
        self.points = []  # Assuming you store points here
        self.lines = []  # And lines here, if applicable
        self.last_measured_distance_mm = None
        self.points.clear()  # This clears the points list
        self.update()


