import cv2
import numpy as np
from matplotlib import pyplot as plt

def draw_tooth_pattern(size_pixels, pas_reel_mm, rotation): #Fonction pour dessiner le motif des dents du filetage
    if size_pixels is None or size_pixels <= 0:
        raise ValueError("La taille en pixels doit être positive et non nulle")
    
    pas_pixels = pas_reel_mm / size_pixels
    tooth_height = max(int(1 / size_pixels), 1)
    pattern_width = int(pas_pixels * 4)
    pattern_height = tooth_height
    
    # Créer une image avec un fond transparent (canal alpha initialisé à 0, les autres à 255)
    pattern_image = np.zeros((pattern_height, pattern_width, 4), dtype=np.uint8)
    
    # Dessiner et remplir 4 dents avec du blanc sur le canal alpha
    for i in range(4):
        start_x = int(i * pas_pixels)
        end_x = int((i + 1) * pas_pixels)
        middle_x = int((start_x + end_x) / 2)
        
        # Points définissant le polygone de chaque dent
        points = np.array([[start_x, pattern_height - 1], [middle_x, 0], [end_x, pattern_height - 1]], np.int32)
        points = points.reshape((-1, 1, 2))  
        
        # Dessiner les lignes sur le canal alpha pour rendre visible les dents
        cv2.line(pattern_image, (start_x, tooth_height - 1), (middle_x, 0), (255, 255, 255, 255), 1)
        cv2.line(pattern_image, (middle_x, 0), (end_x, tooth_height - 1), (255, 255, 255, 255), 1)

    if rotation:
        # Rotation de l'image si nécessaire
        pattern_image = cv2.rotate(pattern_image, cv2.ROTATE_180)
    
    return pattern_image





