import cv2
import numpy as np
from matplotlib import pyplot as plt
import nbimporter
from diametre_monnaie import conversion_piece

image_path = 'DataBase/image7.jpg' 

reference_object_mm = 22.6  # diamètre de la pièce de monnaie en mm 

# Les dimensions réelles en millimètres de la piece 

diametre_reel_mm = 20  # Diamètre réel du filetage en mm  
pas_reel_mm = 25.4 / 14 # Pas réel du filetage en mm


def draw_tooth_pattern(image_path,diametre_reel_mm, pas_reel_mm, reference_object_mm,rotation):
    size_pixels = conversion_piece(image_path, reference_object_mm)
    
    pas_pixels = pas_reel_mm / size_pixels
    tooth_height = int(1 / size_pixels)  # La hauteur de la dent est définie ici
    
    pattern_width = int(pas_pixels) * 4  # Largeur pour 4 dents
    
    pattern_image = np.zeros((tooth_height, pattern_width), dtype=np.uint8)
    
    # Dessiner 4 dents
    for i in range(4):
        # Calculer les points de départ, milieu et fin pour chaque dent
        start_x = int(i * pas_pixels + pas_pixels * 0.25)
        end_x = int((i + 1) * pas_pixels - pas_pixels * 0.25)
        middle_x = int((start_x + end_x) / 2)
        
        # Dessiner les côtés supérieurs des dents
        cv2.line(pattern_image, (start_x, tooth_height - 1), (middle_x, 0), (255), 1)
        cv2.line(pattern_image, (middle_x, 0), (end_x, tooth_height - 1), (255), 1)

    if rotation:
        pattern_image = cv2.rotate(pattern_image, cv2.ROTATE_180)

    return pattern_image


pattern_image = draw_tooth_pattern(image_path,diametre_reel_mm,pas_reel_mm,reference_object_mm,False)
cv2.imwrite('pattern_image.jpg', pattern_image)

def match(template,img_path):
    img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    
    return img,res,max_val


img, res, max_val = match(pattern_image, image_path)
cv2.imwrite('matched_image.jpg', img)