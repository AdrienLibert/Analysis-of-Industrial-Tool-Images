import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
from matplotlib import pyplot as plt
from diametre_monnaie import conversion_piece
import math
from tooth_pattern import draw_tooth_pattern


def zoom(event):
    global image, photo
    new_width = int(image.width * 1.1)
    new_height = int(image.height * 1.1)
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_on_canvas, image=photo)

def dezoom(event):
    global image, photo
    new_width = int(image.width * 0.9)
    new_height = int(image.height * 0.9)
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_on_canvas, image=photo)

def rotate(shape, angle):
    coords = canvas.coords(shape)
    center_x = (coords[0] + coords[2]) / 2
    center_y = (coords[1] + coords[3]) / 2

    new_coords = []
    for i in range(0, len(coords), 2):
        x = coords[i] - center_x
        y = coords[i + 1] - center_y
        new_x = center_x + x * math.cos(math.radians(angle)) - y * math.sin(math.radians(angle))
        new_y = center_y + x * math.sin(math.radians(angle)) + y * math.cos(math.radians(angle))
        new_coords.extend([new_x, new_y])

    canvas.coords(shape, *new_coords)

def rotate_left(event):
    rotate(pattern, 10)

def rotate_right(event):
    rotate(pattern, -10)
def move_up(event):
    canvas.move(pattern, 0, -10)

def move_down(event):
    canvas.move(pattern, 0, 10)

def move_left(event):
    canvas.move(pattern, -10, 0)

def move_right(event):
    canvas.move(pattern, 10, 0)


image_path = '../DataBase/image7.jpg' 

reference_object_mm = 24.25  # diamètre de la pièce de monnaie en mm 

# Les dimensions réelles en millimètres de la piece 
diametre_reel_mm = 10 # Diamètre réel du filetage en mm  
# pas_reel_mm = 25.4 / 14 # Pas réel du filetage en mm
pas_reel_mm = 4 # Pas réel du filetage en mm
#Image 11 -  10 mm de diametre - 16 mm de pas - 24.25 piece de 50 centime

root = tk.Tk()
image = Image.open(image_path)

photo = ImageTk.PhotoImage(image)
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.pack()

image_on_canvas = canvas.create_image(0, 0, image=photo, anchor=tk.NW)

pattern_image_path = 'pattern_image.jpg'
pattern_image = Image.open(pattern_image_path)
pattern_photo = ImageTk.PhotoImage(pattern_image)
pattern = canvas.create_image(100, 100, image=pattern_photo)

root.bind("<Up>", move_up)
root.bind("<Down>", move_down)
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

root.bind("z", zoom)
root.bind("x", dezoom)

root.bind("<a>", rotate_left)
root.bind("<e>", rotate_right)

root.mainloop()

