import cv2
import numpy as np
from matplotlib import pyplot as plt
import nbimporter
from diametre_monnaie import conversion_piece




# image_path = 'BDD/image7.jpg' 

reference_object_mm = 22.6  # diamètre de la pièce de monnaie en mm ( à Modifier)

# Les dimensions réelles en millimètres de la piece ( à modifier)

diametre_reel_mm = 20  # Diamètre réel du filetage en mm  
pas_reel_mm = 25.4 / 14 # Pas réel du filetage en mm

#Ne pas modifier
longueur_cm = 10  # Longueur des lignes horizontales en mm
depassement_mm = 0.2 # Le dépassement des ligne verticale

def template(image_path,diametre_reel_mm,pas_reel_mm,longueur_cm,depassement_mm,reference_object_mm):
    
    size_pixels = conversion_piece(image_path,reference_object_mm)

    pas_pixels = (pas_reel_mm / size_pixels)
    cm_pixels = (longueur_cm / size_pixels)
    depassement_mm_pixel = (depassement_mm / size_pixels)
    diametre_pixels = (diametre_reel_mm / size_pixels)
    
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
    return pattern_image


def rotate_pattern(pattern, angle):
    # Calculer le centre du motif pour la rotation
    centre = (pattern.shape[1] // 2, pattern.shape[0] // 2)
    
    # Créer la matrice de rotation en utilisant le centre du motif
    matrice_rotation = cv2.getRotationMatrix2D(centre, angle, 1.0)
    
    # Effectuer la rotation
    pattern_rotated = cv2.warpAffine(pattern, matrice_rotation, (pattern.shape[1], pattern.shape[0]))
    
    return pattern_rotated



# pattern_image = template(image_path,diametre_reel_mm,pas_reel_mm,longueur_cm,depassement_mm,reference_object_mm)
# pattern_90_avant = rotate_pattern(pattern_normal, -90)  # Rotation de -90° 
# pattern_90_apres = rotate_pattern(pattern_normal, 90)  # Rotation de 90° 
# cv2.imwrite('pattern_image.jpg', pattern_image)

def match(template,img_path):
    img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    
    return img,res,max_val


# img = match(pattern_image,image_path)
# cv2.imwrite('image.jpg', img[0])


def statistics(img):
    plt.subplot(121),plt.imshow(img[1],cmap = 'gray')
    plt.title('Resultat'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img[0],cmap = 'gray')
    plt.title('Detection'), plt.xticks([]), plt.yticks([])
    plt.show()
    

# statistics(img)