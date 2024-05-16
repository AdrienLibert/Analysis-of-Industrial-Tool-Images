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
    
    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("L'image n'a pas pu être chargée.")
    
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Appliquer un seuil pour obtenir une image binaire
    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = cv2.bitwise_not(thresh)

    # Créer un élément structurant pour l'opération de fermeture morphologique
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(5, 5))

    # Effectuer une opération de fermeture morphologique
    morph_img = thresh.copy()
    cv2.morphologyEx(src=thresh, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img)

    # Trouver les contours dans l'image
    contours,_ = cv2.findContours(morph_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Préparer l'image de sortie
    output_image = cv2.cvtColor(morph_img, cv2.COLOR_GRAY2BGR)

    # Obtenir les dimensions de l'image
    height, width = morph_img.shape[:2]

    # Définir les limites pour la recherche des contours
    y_limit1 = height - 800
    y_limit2 = 800

    # Initialiser le contour et l'aire maximaux
    max_contour = None
    max_area = 0

    # Chercher le plus grand contour dans la zone définie
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        if (center[1] > y_limit1 or center[1] < y_limit2):
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                max_contour = cnt
                
    # Calculer le diamètre du cercle qui englobe le plus grand contour
    if max_contour is not None:
        (x, y), radius = cv2.minEnclosingCircle(max_contour)
        diameter = 2 * int(radius)
    else:
        diameter = 0
    
    # Retourner le rapport de la taille de la pièce sur le diamètre
    return taille_piece/diameter

def estimate_image(image_path):
    # Lecture de l'image depuis le chemin spécifié
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("L'image n'a pas pu être chargée.")
    
    # Conversion de l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Application du seuillage pour binariser l'image
    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = cv2.bitwise_not(thresh)

    # Création d'un élément structurant pour l'opération morphologique
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(5, 5))

    # Application de la fermeture pour combler les petits trous dans les contours
    morph_img = thresh.copy()
    cv2.morphologyEx(src=thresh, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img)

    # Détection des contours dans l'image morphologique
    contours,_ = cv2.findContours(morph_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Préparation de l'image de sortie en convertissant l'image morphologique en couleur
    output_image = cv2.cvtColor(morph_img, cv2.COLOR_GRAY2BGR)

    height, width = morph_img.shape[:2]# dimensions de l'image

    y_limit1 = height - 800 #limite
    y_limit2 = 800

    # Initialisation des variables pour la recherche du plus grand contour
    max_contour = None
    max_area = 0

    # Détermination du plus grand contour en dehors des zones délimitées
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        if (center[1] > y_limit1 or center[1] < y_limit2):
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                max_contour = cnt

    #Si un contour maximal est trouvé, dessiner le cercle correspondant
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

    return output_image # Retourner l'image annotée