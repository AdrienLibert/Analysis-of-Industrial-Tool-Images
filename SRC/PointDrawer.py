from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGraphicsEllipseItem, QGraphicsLineItem
from CustomGraphicsView import CustomGraphicsView
from utils.diametre_monnaie import conversion_piece
import math
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen,QColor
class PointDrawer(QDialog):
    def __init__(self, image_path, reference_object_mm):
        super().__init__()
        # Initialisation avec un chemin d'image et une référence de taille
        self.last_measured_distance_mm = None
        self.points = []
        self.image_path = image_path
        self.reference_object_mm = reference_object_mm

        # Configuration de la vue graphique
        self.graphicsView = CustomGraphicsView()
        self.graphicsView.openPicture(image_path)
        self.graphicsView.mousePressEvent = self.mousePressEvent
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.graphicsView)

    def addPoint(self, x, y):
        # Convertir les coordonnées de la souris en coordonnées de la scène
        scenePos = self.graphicsView.mapToScene(x, y)

        # Maintenir seulement deux points sur la scène
        if len(self.points) >= 2:
            # Supprime le premier point si deux points sont déjà présents
            item_to_remove = self.points.pop(0)
            self.graphicsView.scene().removeItem(item_to_remove)

        # Créer un nouveau point plus grand et le remplir
        ellipse = QGraphicsEllipseItem(scenePos.x() - 15, scenePos.y() - 15, 30, 30)  # Taille ajustée à 30x30
        ellipse.setPen(QPen(Qt.red, 4))  # Contour plus épais
        ellipse.setBrush(QColor(Qt.red))  # Remplissage rouge
        self.graphicsView.scene().addItem(ellipse)
        self.points.append(ellipse)

        # Si deux points sont présents, dessiner une ligne et calculer la distance
        if len(self.points) == 2:
            self.drawLine()

    def drawLine(self):
        # Supprime la ligne existante si elle existe
        if hasattr(self, 'lineItem'):
            self.graphicsView.scene().removeItem(self.lineItem)
        
        p1 = self.points[0].rect().center() + self.points[0].pos()
        p2 = self.points[1].rect().center() + self.points[1].pos()
        self.lineItem = QGraphicsLineItem(p1.x(), p1.y(), p2.x(), p2.y())
        self.lineItem.setPen(QPen(Qt.blue, 6))
        self.graphicsView.scene().addItem(self.lineItem)

        # Calcul et affichage de la distance
        self.calculateAndDisplayDistance(p1, p2)

    def calculateAndDisplayDistance(self, p1, p2):
        # Calcule la distance en millimètres entre deux points
        distance_pixels = math.sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)
        displayed_image_width = self.graphicsView.image.width()
        resize_factor = displayed_image_width / self.graphicsView.original_width
        distance_real = distance_pixels / resize_factor
        self.size_pixels = conversion_piece(self.image_path, self.reference_object_mm)
        distance_mm = distance_real * self.size_pixels
        self.last_measured_distance_mm = distance_mm
        print(f"Distance entre les deux points : {distance_mm} mm")

    def mousePressEvent(self, event):
        # Gestion des événements de clic pour ajouter des points
        if event.button() == Qt.LeftButton:
            self.addPoint(event.x(), event.y())

    def reset(self):
        # Réinitialise les points et les mesures
        for item in self.points:
            self.graphicsView.scene().removeItem(item)
        self.points.clear()
        if hasattr(self, 'lineItem'):
            self.graphicsView.scene().removeItem(self.lineItem)
        self.last_measured_distance_mm = None

    def get_last_measured_distance(self):
        # Retourne la dernière distance mesurée et la taille en pixels
        return self.last_measured_distance_mm, self.size_pixels

