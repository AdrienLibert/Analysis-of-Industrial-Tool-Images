import cv2
import numpy as np
from piece import piece

image_path = 'BDD/image5.jpg' 

reference_object_size_pixels = piece(image_path)

# Les dimensions réelles en millimètres
reference_object_real_world_mm = 22.6  # diamètre de la pièce de monnaie en mm
diametre_reel_mm = 12  # Diamètre réel du filetage en mm
pas_reel_mm = 1   # Pas réel du filetage en mm
longueur_cm = 10  # Longueur des lignes horizontales en mm

# Convertir les mesures réelles en pixels
diametre_pixels = (diametre_reel_mm * reference_object_size_pixels) / reference_object_real_world_mm
pas_pixels = (pas_reel_mm * reference_object_size_pixels) / reference_object_real_world_mm
cm_pixels = (longueur_cm * reference_object_size_pixels) / reference_object_real_world_mm

# Créer une image noire qui servira de base pour le pattern
pattern_height = int(diametre_pixels)  # Hauteur du pattern basée sur le diamètre en pixels
pattern_width = int(cm_pixels)   # Largeur du pattern basée sur le pas en pixels


pattern_image = np.zeros((pattern_height, pattern_width), dtype=np.uint8)

depassement = 5  # Nombre de pixels que les verticales dépassent des horizontales


# Dessiner les deux lignes horizontales
cv2.line(pattern_image, (0, depassement), (pattern_width, depassement), (255), 1)
cv2.line(pattern_image, (0, pattern_height - 1 - depassement), (pattern_width, pattern_height - 1 - depassement), (255), 1)

# Dessiner les segments verticaux entre les lignes horizontales
for x in range(0, pattern_width, int(pas_pixels)):
    cv2.line(pattern_image, (x, 0), (x, pattern_height - 1), (255), 1)

# Sauvegarder l'image du pattern
cv2.imwrite('Test/pattern_image.jpg', pattern_image)

# # Charger l'image cible
# target_image = cv2.imread(image_path)
# gray_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

# # Effectuer le template matching
# result = cv2.matchTemplate(gray_image, pattern_image, cv2.TM_CCOEFF_NORMED)

# # Seuil pour la reconnaissance
# threshold = 0.8
# locations = np.where(result >= threshold)

# # Superposer le pattern sur l'image cible
# for loc in zip(*locations[::-1]):
#     # Dessiner un rectangle autour de la zone correspondante
#     cv2.rectangle(target_image, loc, (loc[0] + pattern_width, loc[1] + pattern_height), (0,255,0), 2)

# # Afficher l'image résultante
# cv2.imwrite('Test/target_image.jpg', target_image)
