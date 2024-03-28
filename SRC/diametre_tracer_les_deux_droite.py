import cv2
import numpy as np
from matplotlib import pyplot as plt
import nbimporter
from diametre_monnaie import conversion_piece
from tooth_pattern import draw_tooth_pattern
from tooth_pattern import match_top_bottom

image_path = '../DataBase/image15.jpg' 

reference_object_mm = 26.5  # diamètre de la pièce de monnaie en mm 

# Les dimensions réelles en millimètres de la piece 

diametre_reel_mm = 21.5  # Diamètre réel du filetage en mm  
pas_reel_mm = 25.4 / 26 # Pas réel du filetage en mm


def segments(img, top_left_top, bottom_right_bottom):
    line_length = 300
    
    line_top_start = (max(top_left_top[0] - line_length, 0), top_left_top[1])
    line_top_end = (min(top_left_top[0] + line_length, img.shape[1]), top_left_top[1])
    
    line_bottom_start = (max(bottom_right_bottom[0] - line_length, 0), bottom_right_bottom[1])
    line_bottom_end = (min(bottom_right_bottom[0] + line_length, img.shape[1]), bottom_right_bottom[1])
    
    cv2.line(img, line_top_start, line_top_end, 255, 2)
    cv2.line(img, line_bottom_start, line_bottom_end, 255, 2)
    
    diametre = abs(line_top_start[1] - line_bottom_start[1])
    y_values = []
    y_values2 = []

    x_start = max(top_left_top[0] - line_length, 0)
    x_end = min(top_left_top[0] + line_length, img.shape[1])
    for x in range(x_start, x_end):
        y_values.append(top_left_top[1])
        
    x_start2 = max(bottom_right_bottom[0] - line_length, 0)
    x_end2 = min(bottom_right_bottom[0] + line_length, img.shape[1])
    for x in range(x_start, x_end):
        y_values2.append(bottom_right_bottom[1])
    
    cv2.line(img, (line_top_start[0]+200, line_top_start[1]), (line_top_start[0]+200, line_bottom_start[1]), 255, 2)
    cv2.line(img, ((x_end + x_start)//2, line_top_start[1]), ((x_end + x_start)//2, line_bottom_start[1]), 255, 2)
    cv2.line(img, ((x_end2 + x_start2)//2, line_top_start[1]), ((x_end2 + x_start2)//2, line_bottom_start[1]), 255, 2)

    return img,diametre