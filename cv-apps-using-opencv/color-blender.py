# Import required modules
import os
import numpy as np
import cv2

# Create a white canvas
def createCanvas(color):
    # Create a 600x800 canvas (height x width x channels)
    # RGB value for white is (255, 255, 255)
    height, width = 600, 800
    canvas = np.full((height, width, 3), color, dtype=np.uint8)
    return canvas

# Mouse callback function
# Mouse callback function
def mouseCallbackFunction(event, x, y, flags, param):
    global color1
    # Check if left mouse button was pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        # Set the color to color at the location
        color1 = findColor(colorPalette,x,y)


# Find the color for an image at the given location
def findColor(img, x, y):
    # Check if coordinates are within image bounds
    if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
        # Get BGR color at the specified coordinates
        bgr_color = img[y, x]  # Note: OpenCV uses [y, x] indexing
        return tuple(int(c) for c in bgr_color)  # Convert to regular Python int
    else:
        print(f"Coordinates ({x}, {y}) are out of bounds")
        return None


def mixColors(color1, color2):
    # Mix two RGB colors by averaging their values
    mixed_r = int((color1[0] + color2[0]) / 2)
    mixed_g = int((color1[1] + color2[1]) / 2)
    mixed_b = int((color1[2] + color2[2]) / 2)
    return (mixed_r, mixed_g, mixed_b)

# Create a callback wrapper function that includes the image data
def createOnMouseClickCallback(image):
    selected_colors = []  # List to store picked colors

    def callback(event, x, y, flags, param):
        return mouseCallbackFunction(event, x, y, flags, [image, selected_colors])

    return callback

# Display an image
def displayImage(image, window_name="Image"):
    cv2.imshow(window_name, image)


# Initialize global variable for mixed color
final_mixed_color = None

# Create initial white canvas
white_color = (255, 255, 255)  # RGB value for white
canvas = createCanvas(white_color)

# Load the color palette from the image file
colorPalette = cv2.imread("color-palette.jpg")
if colorPalette is None:
    print(f"Error: Could not load image from color-palette.jpg")
    os.exit(1)

cv2.namedWindow("Canvas")
cv2.namedWindow("Color Palete")
cv2.setMouseCallback("Color Palete",mouseCallbackFunction)


color1 = None

while 1:
    # First find color from color palette
    displayImage(canvas,"Canvas")
    displayImage(colorPalette,"Color Palete")
    if color1 is not None:
        # Find color in canvas
        color2 = findColor(canvas,10,10)
        # Mix colors
        newColor = mixColors(color1,color2)
        # Fill the new color in canvas
        canvas = createCanvas(newColor)
        # Set color1 back to default value
        color1 = None
    key = cv2.waitKey(20)
    if key == 27:
        break
    elif key == ord('r'):
        canvas = createCanvas(white_color)
        color1 = None
    elif key == ord('s'):
        cv2.imwrite("canvas.png",canvas)

cv2.destroyAllWindows()