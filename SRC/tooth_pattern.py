import cv2
import numpy as np
from matplotlib import pyplot as plt
from diametre_monnaie import conversion_piece

def draw_tooth_pattern(pas_reel_mm, reference_object_mm, image_path, rotation):
    size_pixels = conversion_piece(image_path, reference_object_mm)
    
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

# def match_top_bottom(template, template_r, img_path, vertical_split_ratio=0.5):
#     img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#     h, w = img.shape

#     # Diviser l'image en deux régions horizontalement
#     split_line = int(vertical_split_ratio * h)

#     # Régions supérieure et inférieure
#     top_region = img[:split_line, :]
#     bottom_region = img[split_line:, :]

#     # Appliquer la correspondance de modèle sur la région supérieure avec template_r
#     res_top = cv2.matchTemplate(top_region, template_r, cv2.TM_CCOEFF_NORMED)
#     _, max_val_top, _, max_loc_top = cv2.minMaxLoc(res_top)
#     top_left_top = (max_loc_top[0], max_loc_top[1])
#     bottom_right_top = (max_loc_top[0] + template_r.shape[1], max_loc_top[1] + template_r.shape[0])

#     # Dessiner le rectangle pour la meilleure correspondance dans la région supérieure
#     cv2.rectangle(img, top_left_top, bottom_right_top, 255, 2)

#     # Appliquer la correspondance de modèle sur la région inférieure avec template
#     res_bottom = cv2.matchTemplate(bottom_region, template, cv2.TM_CCOEFF_NORMED)
#     _, max_val_bottom, _, max_loc_bottom = cv2.minMaxLoc(res_bottom)
#     top_left_bottom = (max_loc_bottom[0], max_loc_bottom[1] + split_line)
#     bottom_right_bottom = (max_loc_bottom[0] + template.shape[1], max_loc_bottom[1] + split_line + template.shape[0])

#     # Dessiner le rectangle pour la meilleure correspondance dans la région inférieure
#     cv2.rectangle(img, top_left_bottom, bottom_right_bottom, 255, 2)

#     # Sauvegarder et retourner l'image avec les rectangles de correspondance
#     output_path = 'matched_image.jpg'
#     cv2.imwrite(output_path, img)

#     return img, (top_left_top, bottom_right_bottom)

# Exemple d'utilisation

# # Création des deux templates
# pattern_image = draw_tooth_pattern(pas_reel_mm, reference_object_mm, image_path,False)
# pattern_image_r = draw_tooth_pattern(pas_reel_mm, reference_object_mm, image_path,True)

# # Match
# img_with_matches, (top_left_top, bottom_right_bottom) = match_top_bottom(pattern_image, pattern_image_r, image_path)
