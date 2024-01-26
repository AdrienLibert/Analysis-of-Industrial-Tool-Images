import cv2
import numpy as np
from piece import piece
from matplotlib import pyplot as plt

image_path = 'BDD/image7.jpg' 

reference_object_size_pixels = piece(image_path)

# Les dimensions réelles en millimètres
reference_object_real_world_mm = 22.6  # diamètre de la pièce de monnaie en mm
diametre_reel_mm = 18  # Diamètre réel du filetage en mm
pas_reel_mm = 1   # Pas réel du filetage en mm
longueur_cm = 10  # Longueur des lignes horizontales en mm
depassement_mm = 0.2 # Pas réel du filetage en mm

pas_reel_mm = 25.4 / 14

# Convertir les mesures réelles en pixels
diametre_pixels = (diametre_reel_mm * reference_object_size_pixels) / reference_object_real_world_mm
pas_pixels = (pas_reel_mm * reference_object_size_pixels) / reference_object_real_world_mm
cm_pixels = (longueur_cm * reference_object_size_pixels) / reference_object_real_world_mm
depassement_mm_pixel = (depassement_mm * reference_object_size_pixels) / reference_object_real_world_mm

print(pas_pixels)
# Créer une image noire qui servira de base pour le pattern
pattern_height = int(diametre_pixels)  # Hauteur du pattern basée sur le diamètre en pixels
pattern_width = int(cm_pixels)   # Largeur du pattern basée sur le pas en pixels
depassement = int(depassement_mm_pixel) # Nombre de pixels que les verticales dépassent des horizontales

pattern_image = np.zeros((pattern_height, pattern_width), dtype=np.uint8)

# Dessiner les deux lignes horizontales
cv2.line(pattern_image, (0, depassement), (pattern_width, depassement), (255), 1)
cv2.line(pattern_image, (0, pattern_height - 1 - depassement), (pattern_width, pattern_height - 1 - depassement), (255), 1)

# Dessiner les segments verticaux entre les lignes horizontales
for x in range(0, pattern_width, int(pas_pixels)):
    cv2.line(pattern_image, (x, 0), (x, pattern_height - 1), (255), 1)

# Sauvegarder l'image du pattern
cv2.imwrite('Test/pattern_image.jpg', pattern_image)


#Phase de template
img = cv2.imread('BDD/image7.jpg', cv2.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
template = cv2.imread('Test/pattern_image.jpg', cv2.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]

# Effectuer le template matching
res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(img,top_left, bottom_right, 255, 2)
plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])

plt.show()
