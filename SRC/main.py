import cv2
import numpy as np

def main():
    image_path = 'BDD/image7.jpg'
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("The image could not be loaded.")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # Threshold the image
    ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    piece_contour = sorted_contours[0]
    coin_contour = sorted_contours[1]

    # Draw contours
    cv2.drawContours(image, [piece_contour], -1, (255, 0, 0), 2)
    cv2.drawContours(image, [coin_contour], -1, (0, 255, 0), 2)

    # Save and show the image
    cv2.imwrite('detected_image.png', image)
if __name__ == '__main__':
    main()
