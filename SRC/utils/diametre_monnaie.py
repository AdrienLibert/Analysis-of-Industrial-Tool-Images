import cv2 
import numpy as np
import os

def conversion_piece(image_path,taille_piece):
    # Afficher le chemin absolu pour le débogage
    print(f"Chemin absolu de l'image: {os.path.abspath(image_path)}")
    
    # Vérifier si le fichier existe
    if not os.path.exists(image_path):
        print("Le fichier spécifié n'existe pas.")
        return None
    
    image = cv2.imread(image_path)#charge image
    if image is None:
        raise ValueError("L'image n'a pas pu être chargée.")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = cv2.bitwise_not(thresh)

    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(5, 5))

    morph_img = thresh.copy()
    cv2.morphologyEx(src=thresh, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img)

    contours,_ = cv2.findContours(morph_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #trouver les contours

    output_image = cv2.cvtColor(morph_img, cv2.COLOR_GRAY2BGR)# préparer l'image de sortie

    height, width = morph_img.shape[:2]# dimensions de l'image

    y_limit1 = height - 800 #limite
    y_limit2 = 800

    max_contour = None #contour et aire
    max_area = 0

    for cnt in contours: #on cherche dans la zone les contours
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        if (center[1] > y_limit1 or center[1] < y_limit2):
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                max_contour = cnt
                
    if max_contour is not None:
        (x, y), radius = cv2.minEnclosingCircle(max_contour)
        diameter = 2 * int(radius)
    else:
        diameter = 0
    
    cv2.imwrite('img.jpg', output_image)
    
    return taille_piece/diameter #diametre

def estimate_image(image_path):
    image = cv2.imread(image_path)#charge image
    if image is None:
        raise ValueError("L'image n'a pas pu être chargée.")
        
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = cv2.bitwise_not(thresh)

    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(5, 5))

    morph_img = thresh.copy()
    cv2.morphologyEx(src=thresh, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img)

    contours,_ = cv2.findContours(morph_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #trouver les contours

    output_image = cv2.cvtColor(morph_img, cv2.COLOR_GRAY2BGR)# préparer l'image de sortie

    height, width = morph_img.shape[:2]# dimensions de l'image

    y_limit1 = height - 800 #limite
    y_limit2 = 800

    max_contour = None #contour et aire
    max_area = 0

    for cnt in contours: #on cherche dans la zone les contours
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        if (center[1] > y_limit1 or center[1] < y_limit2):
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                max_contour = cnt
                
    if max_contour is not None:
        (x, y), radius = cv2.minEnclosingCircle(max_contour)
        diameter = 2 * int(radius)
    else:
        diameter = 0
    
    (x, y), radius = cv2.minEnclosingCircle(max_contour)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(output_image, center, radius, (0, 255, 0), 2)
    cv2.circle(output_image, center, 1, (0, 0, 255), 3)
    start_point = (int(x - radius), int(y))
    end_point = (int(x + radius), int(y))
    cv2.line(output_image, start_point, end_point, (255, 0, 0), 2)

    return output_image #output image