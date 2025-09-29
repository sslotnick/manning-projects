import os
import cv2
import numpy as np

def captureImage():
    cap = cv2.VideoCapture(0)

    frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video", frame)
        if cv2.waitKey(20) == ord('c'):
            break
    cap.release()
    cv2.destroyWindow("Video")
    return frame

def loadMask():
    mask = cv2.imread("mask.png", cv2.IMREAD_UNCHANGED)
    if mask is None:
        print("Error: Could not load mask.png")
        os.exit(1)
    mask = cv2.resize(mask, None, fx=0.2, fy=0.2)
    # Extract alpha channel (4th channel in BGRA)
    alpha_channel = mask[:, :, 3]
    alpha_channel = cv2.cvtColor(alpha_channel, cv2.COLOR_GRAY2BGR)
    mask = mask[:,:,:3]

    return alpha_channel, mask

def applyMask(selfie, mask, alpha_channel, x, y):
    """
    Apply face mask to selfie at specified (x,y) coordinates using bitwise operations.
    Uses alpha channel for transparency handling.
    """
    # Create a copy of the selfie to avoid modifying the original
    result = selfie.copy()

    # Get mask dimensions
    mask_height, mask_width = mask.shape[:2]

    # Calculate the region of interest (ROI) in the selfie
    # Center the mask around the clicked point
    start_y = max(0, y - mask_height // 2)
    end_y = min(selfie.shape[0], start_y + mask_height)
    start_x = max(0, x - mask_width // 2)
    end_x = min(selfie.shape[1], start_x + mask_width)

    # Adjust mask coordinates if clipping occurs
    mask_start_y = max(0, mask_height // 2 - y) if y < mask_height // 2 else 0
    mask_end_y = mask_start_y + (end_y - start_y)
    mask_start_x = max(0, mask_width // 2 - x) if x < mask_width // 2 else 0
    mask_end_x = mask_start_x + (end_x - start_x)

    # Extract the region of interest from the selfie
    roi = result[start_y:end_y, start_x:end_x]

    # Extract the corresponding mask and alpha regions
    mask_roi = mask[mask_start_y:mask_end_y, mask_start_x:mask_end_x]
    alpha_roi = alpha_channel[mask_start_y:mask_end_y, mask_start_x:mask_end_x]

    # Ensure dimensions match
    if roi.shape[:2] != mask_roi.shape[:2]:
        return result

    # Normalize alpha channel to 0-1 range
    alpha_normalized = alpha_roi.astype(np.float32) / 255.0

    # Apply bitwise operations using alpha blending
    # Method 1: Using multiplication and addition (equivalent to bitwise operations)
    # Background (selfie) contribution where mask is transparent
    background_contribution = roi.astype(np.float32) * (1.0 - alpha_normalized)
    # Foreground (mask) contribution where mask is opaque
    foreground_contribution = mask_roi.astype(np.float32) * alpha_normalized

    # Combine foreground and background
    blended = background_contribution + foreground_contribution
    # Update the result image
    result[start_y:end_y, start_x:end_x] = blended.astype(np.uint8)

    return result

# Global variables for mouse callback
current_selfie = None
current_mask = None
current_alpha = None
masked_selfie = None

def mouseCallback(event, x, y, flags, param):
    """
    Mouse callback function to handle user clicks and apply mask at clicked location.
    """
    global current_selfie, current_mask, current_alpha, masked_selfie, selfie

    # Apply mask at the clicked position
    masked_selfie = applyMask(current_selfie, current_mask, current_alpha, x, y)

    # Display the updated selfie
    cv2.imshow("Selfie with Mask", masked_selfie)
    if (event == cv2.EVENT_LBUTTONDOWN):
        current_selfie = masked_selfie.copy()

# Capture selfie and load mask
selfie = captureImage()
alpha_channel, mask = loadMask()

# Initialize global variables
current_selfie = selfie.copy()
current_mask = mask
current_alpha = alpha_channel
masked_selfie = selfie.copy()

# Display initial images
cv2.imshow("Selfie with Mask", masked_selfie)



# Set up mouse callback for the selfie window
cv2.setMouseCallback("Selfie with Mask", mouseCallback)

print("Instructions:")
print("- Click on the selfie to apply the mask at that location")
print("- Press 's' to save the current image")
print("- Press 'r' to reset to original selfie")
print("- Press 'ESC' to exit")

# Main loop for handling keyboard input
while True:
    key = cv2.waitKey(20)

    if key == 27:  # ESC key
        print("Exiting...")
        break
    elif key == ord('s'):  # Save image
        if masked_selfie is not None:
            filename = "masked_selfie.png"
            cv2.imwrite(filename, masked_selfie)
            print(f"Image saved as {filename}")
        else:
            print("No image to save")
    elif key == ord('r'):  # Reset to original
        print("Resetting to original selfie...")
        current_selfie = selfie.copy()
        masked_selfie = selfie.copy()
        cv2.imshow("Selfie with Mask", masked_selfie)

cv2.destroyAllWindows()
