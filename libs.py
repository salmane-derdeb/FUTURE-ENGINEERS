import numpy as np
import cv2
import matplotlib.pyplot as plt
from rplidar import RPLidar

# Initialize LIDAR
PORT_NAME = '/dev/ttyUSB0'  # Update this to your correct LIDAR port
lidar = RPLidar(PORT_NAME)

# Set up Matplotlib for plotting
plt.ion()
fig, ax = plt.subplots()

# Function to update plot in real-time
def update_plot(scan_data):
    ax.clear()
    scan_data = np.array(scan_data)
    if len(scan_data) > 0:
        angles = scan_data[:, 1]  # Angle values (degrees)
        distances = scan_data[:, 2]  # Distance values (mm)
        
        # Convert polar coordinates (angles, distances) to Cartesian coordinates (x, y)
        x_vals = distances * np.cos(np.radians(angles))
        y_vals = distances * np.sin(np.radians(angles))
        
        ax.plot(x_vals, y_vals, 'bo', markersize=2)
        ax.set_xlim(-6000, 6000)
        ax.set_ylim(-6000, 6000)
        ax.set_aspect('equal')
        plt.draw()

# Main loop to read from LIDAR and update the visualization
try:
    for scan in lidar.iter_scans():
        scan_data = []
        for _, angle, distance in scan:
            scan_data.append([_, angle, distance])

        # Update plot using Matplotlib
        update_plot(scan_data)
        plt.pause(0.01)

        # Convert the Matplotlib plot to OpenCV image
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        # Display using OpenCV
        cv2.imshow('LIDAR Visualization', img)

        # Stop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop the LIDAR when done
    lidar.stop()
    lidar.disconnect()
    cv2.destroyAllWindows()
