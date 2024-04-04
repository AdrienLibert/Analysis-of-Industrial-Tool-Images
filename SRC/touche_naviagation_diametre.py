import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
from diametre_monnaie import conversion_piece



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

points = []

image_path = '../DataBase/image7.jpg' 
reference_object_mm = 22.6  # diamètre de la pièce de monnaie en mm 

def on_click(event):
    global points, canvas, reference_object_mm, image_path
    radius = 3
    points.append((event.x, event.y))
    canvas.create_oval(event.x - radius, event.y - radius, event.x + radius, event.y + radius, fill='red')


    if len(points) == 2:
        distance = math.sqrt((points[1][0] - points[0][0]) ** 2 + (points[1][1] - points[0][1]) ** 2)
        print(f"Distance: {distance} pixels")
        size_pixels = conversion_piece(image_path, reference_object_mm)
        print(f"Distance en mm: {distance * size_pixels} mm")
        points = []


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

canvas.bind("<Button-1>", on_click)
root.bind("<Up>", move_up)
root.bind("<Down>", move_down)
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

root.bind("z", zoom)
root.bind("x", dezoom)

root.mainloop()