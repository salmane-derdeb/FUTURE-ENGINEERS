import time
import numpy as np
import cv2
from picamera2 import Picamera2

# Initialize Picamera2
picam2 = Picamera2(camera_num=0)
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()

def nothing(x):
    pass

# Create a window for trackbars
cv2.namedWindow("Trackbars and Output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Trackbars and Output", 800, 480)

cv2.createTrackbar("L - H", "Trackbars and Output", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars and Output", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars and Output", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars and Output", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars and Output", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars and Output", 255, 255, nothing)

while True:
    # Capture frame
    frame = picam2.capture_array()
    frame = cv2.resize(frame, (640, 480))
    
    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get values from trackbars
    l_h = cv2.getTrackbarPos("L - H", "Trackbars and Output")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars and Output")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars and Output")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars and Output")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars and Output")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars and Output")
    
    # Define lower and upper bounds for the mask
    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])
    
    # Create mask
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Apply mask to the frame
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Combine the mask and result vertically
    combined = np.vstack((mask, result))

    # Display combined output with trackbars
    cv2.imshow("Trackbars and Output", combined)
    
    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
picam2.stop()
cv2.destroyAllWindows()
