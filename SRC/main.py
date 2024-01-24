import cv2
import nbimporter
import numpy as np

from diametre_monnaie import estimate_diameter
def main():
    image_path = 'BDD/image7.jpg' 

    
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("The image could not be loaded.")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area 
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    piece_contour = sorted_contours[1]  # the nut's contour

    # Draw contours
    cv2.drawContours(image, [piece_contour], -1, (255, 0, 0), 2)

    # Calculate the bounding rectangle and extract the width (horizontal diameter)
    x, y, w, h = cv2.boundingRect(piece_contour)

    diameter_pixels = max(w,h)
    
    print(diameter_pixels)


    
    reference_object_real_world_mm = 22.6  # Example: the coin diameter in mm
    reference_object_size_pixels = estimate_diameter(image_path)
    print(reference_object_size_pixels)
    print(diameter_pixels)

    # Calculate the nut's diameter in real-world units
    nut_diameter_mm = (diameter_pixels / reference_object_size_pixels) * reference_object_real_world_mm

    print(f"Diameter of the nut: {nut_diameter_mm} mm")

    # Save 
    cv2.imwrite('Test/detected_nut_diameter.jpg', image)

if __name__ == '__main__':
    main()
