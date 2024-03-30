import cv2
import numpy as np
from matplotlib import pyplot as plt
import nbimporter
from diametre_monnaie import conversion_piece

image_path = 'DataBase/image7.jpg'

reference_object_mm = 22.6  # diamètre de la pièce de monnaie en mm 
size_pixels = conversion_piece(image_path, reference_object_mm)
# Les dimensions réelles en millimètres de la piece 
diametre_mm = 20 # Diamètre réel du filetage en mm  
pas_mm = 25.4 / 14 # Pas réel du filetage en mm

def draw_tooth_pattern(size_pixels,pas_reel_mm,rotation):

    if size_pixels <= 0:
        raise ValueError("La taille en pixels doit être positive et non nulle")
    
    pas_pixels = pas_reel_mm / size_pixels
    
    tooth_height = max(int(1 / size_pixels), 1)
    
    pattern_width = int(pas_pixels * 4)
    
    pattern_height = tooth_height
    
    pattern_image = np.full((pattern_height, pattern_width), 0, dtype=np.uint8)
    
    # Dessiner et remplir 4 dents
    for i in range(4):
        start_x = int(i * pas_pixels)
        end_x = int((i + 1) * pas_pixels)
        middle_x = int((start_x + end_x) / 2)
        
        # Points définissant le polygone de chaque dent
        points = np.array([[start_x, pattern_height - 1], [middle_x, 0], [end_x, pattern_height - 1]], np.int32)
        points = points.reshape((-1, 1, 2))  
        
        cv2.line(pattern_image, (start_x, tooth_height - 1), (middle_x, 0), (255), 1)
        cv2.line(pattern_image, (middle_x, 0), (end_x, tooth_height - 1), (255), 1)

    if rotation:
        pattern_image = cv2.rotate(pattern_image, cv2.ROTATE_180)
    
    return pattern_image


def create_combined_pattern(size_pixels,pas_reel_mm, distance_entre_patterns):
    # Générer le motif supérieur sans rotation
    pattern_top = draw_tooth_pattern(size_pixels,pas_reel_mm, rotation=False)
    
    # Générer le motif inférieur avec rotation
    pattern_bottom = draw_tooth_pattern(size_pixels,pas_reel_mm, rotation=True)
    
    # Créer l'espace vide 
    empty_space_height = int(distance_entre_patterns / size_pixels)

    # Combinaison des motifs et de l'espace vide
    combined_pattern = np.vstack((pattern_top, np.full((empty_space_height, pattern_top.shape[1]), 0, dtype=np.uint8), pattern_bottom))

    # Hauteur du motif de denture (sans les dents)
    top_offset = pattern_top.shape[0]
    bottom_offset = top_offset + empty_space_height

    # Dessiner les lignes verticales sur la partie centrale uniquement
    cv2.line(combined_pattern, (0, top_offset), (0, bottom_offset - 1), (255), 1)
    cv2.line(combined_pattern, (combined_pattern.shape[1] - 1, top_offset), (combined_pattern.shape[1] - 1, bottom_offset - 1), (255), 1)
    
    return combined_pattern

def extract_contour_from_pattern(pattern_image):
    # Trouver les contours dans le motif
    contours, _ = cv2.findContours(pattern_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Retourner le plus grand contour trouvé dans le motif
    return max(contours, key=cv2.contourArea)

# Créer le motif combiné
combined_pattern = create_combined_pattern(size_pixels,pas_mm, diametre_mm)

cv2.imwrite('pattern_image.jpg', combined_pattern)

# # Extraire le contour du motif
# thread_contour = extract_contour_from_pattern(combined_pattern)

# # Charger l'image d'entrée
# image = cv2.imread(image_path, 0)

# # Détection de bords de Canny
# edges = cv2.Canny(image, threshold1=100, threshold2=200)

# # Trouver les contours dans l'image des bords
# contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# # Comparer les contours trouvés avec le contour de référence
# for contour in contours:
#     similarity = cv2.matchShapes(contour, thread_contour, cv2.CONTOURS_MATCH_I1, 0.0)
#     if similarity < 0.1:  # Valeur seuil pour la similarité
#         cv2.drawContours(image, [contour], -1, (255, 0, 0), 3)
# cv2.imwrite('image.jpg', image)
