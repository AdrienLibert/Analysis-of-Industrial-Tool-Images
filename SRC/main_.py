import nbimporter
import pandas as pd
from pattern_match import template
from list_pas_diam import pattern_list
from pattern_match import match
import cv2

def main(image_path,reference_object_mm,longueur_cm,depassement_mm):
    l = pattern_list(pd.read_csv('TableauConversion/Tableau_conversion.csv'))
    l_seuil = []
    seuil = 0
    i_final = None
    for i in l:
        # if i[0] == 9.72:
        #     pass
        pas_reel_mm = 25.4 / i[1] # Pas réel du filetage en mm
        template_tmp = template(image_path,i[0],pas_reel_mm,longueur_cm,depassement_mm,reference_object_mm)
        match_tmp = match(template_tmp,image_path)
        l_seuil.append((i,match_tmp[2]))
        if match_tmp[2] > seuil: #on recup le meilleur seuil
            seuil = match_tmp[2]
            i_final = match_tmp[0]
            res = (i[0],i[1])
    # l_seuil_sort = sorted(l_seuil, key=lambda l: l[1])
    # print(l_seuil_sort)
    return i_final, res

image_path = 'DataBase/image10.jpg' 
reference_object_mm = 24.25
depassement_mm = 0.2
longueur_cm = 10


#TEST 

#Image 10 - 16 mm de diametre - 13 mm de pas - 24.25 piece de 50 centime
#Image 9 - 16 mm de diametre - 13 mm de pas - 24.25 piece de 50 centime
#Image 7 -  20 mm de diametre - 14 mm de pas - 22.6 piece de 100 yen
#Image 11 -  10 mm de diametre - 16 mm de pas - 24.25 piece de 50 centime

#Image 7 - res = (4.16, 32.0) FAUX
#Image 10 - res = (4.76, 24.0) FAUX

#Image 7 - res = (9.72, 2.0) FAUX
#Image 9 - res = (9.72, 2.0) FAUX
#Image 10 - res = (9.72, 2.0) FAUX
#Image 11 - res = (9.72, 2.0) FAUX


#Liste des scores images 10 : 
    # ((9.72, 2.0), 0.30649545788764954)
    # ((15.87, 11.0), 0.19323967397212982)  #Très interessant -> proche de la réalité
    # ((15.87, 11.0), 0.19323967397212982)
    # ((9.52, 16.0), 0.18065743148326874)
    # ((9.52, 16.0), 0.18065743148326874)
    # ((11.11, 14.0), 0.1788005232810974)
    # ((11.11, 14.0), 0.1788005232810974)

#A voir : rotation

m,res = main(image_path,reference_object_mm,longueur_cm,depassement_mm)

print(res)
cv2.imwrite('image.jpg', m)