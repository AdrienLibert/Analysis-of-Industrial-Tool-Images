import cv2
import numpy as np
from matplotlib import pyplot as plt
from diametre_monnaie import conversion_piece


def draw_tooth_pattern(pas_reel_mm, reference_object_mm, image_path, rotation):
    size_pixels = conversion_piece(image_path, reference_object_mm)

    if not size_pixels:
        print("Erreur : la conversion a échoué ou la taille en pixels est zéro.")
        # Retourner une image vide ou une valeur par défaut
        return np.zeros((10, 10), dtype=np.uint8)
    
    pas_pixels = pas_reel_mm / size_pixels
    
    tooth_height = max(int(1 / size_pixels), 1)
    
    pattern_width = int(pas_pixels * 4)
    
    pattern_height = tooth_height
    
    pattern_image = np.zeros((pattern_height, pattern_width), dtype=np.uint8)
    
    # Dessiner et remplir 4 dents
    for i in range(4):
        start_x = int(i * pas_pixels)
        end_x = int((i + 1) * pas_pixels)
        middle_x = int((start_x + end_x) / 2)
        
        # Points définissant le polygone de chaque dent
        points = np.array([[start_x, pattern_height - 1], [middle_x, 0], [end_x, pattern_height - 1]], np.int32)
        points = points.reshape((-1, 1, 2))  # Reshape pour cv2.fillPoly
        
        # Remplir la dent
        cv2.fillPoly(pattern_image, [points], 255)

    if rotation:
        pattern_image = cv2.rotate(pattern_image, cv2.ROTATE_180)
    
    return pattern_image

pas_reel_mm = 4
reference_object_mm = 24.25
image_path = '../DataBase/image7.jpg'
rotation = True

pattern_image = draw_tooth_pattern(pas_reel_mm, reference_object_mm, image_path, rotation)

cv2.imwrite('pattern_image.jpg', pattern_image)


