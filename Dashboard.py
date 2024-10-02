import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, patches

# LiDAR Simulation Data (Angles in degrees and distances in meters)
angles = np.linspace(0, 360, 100)  # 100 readings in 360 degrees
distances = np.random.uniform(0.5, 5.0, 100)  # Random distances (replace with actual data)

# DTOF Sensor Readings (in meters)
dtof_readings = np.array([1.2, 1.5, 2.0, 0.8])  # Replace with actual DTOF data
dtof_labels = ['Front', 'Right', 'Back', 'Left']

# Simulated Gyroscope Data (in degrees)
yaw = 30  # Rotation around the vertical axis
pitch = 5  # Tilt forward/backward
roll = 10  # Tilt left/right

# Simulated Path Data (X, Y position of the robot over time)
time = np.linspace(0, 100, 200)
path_x = np.cumsum(np.random.randn(200))  # Replace with real data
path_y = np.cumsum(np.random.randn(200))  # Replace with real data
dtof_path_data = np.random.uniform(0.5, 2.0, 200)  # Replace with real DTOF data

# Simulated Temperature Data (in degrees Celsius)
temperature = np.random.uniform(20, 30, 1)[0]  # Random temperature data (replace with actual)

# Convert LiDAR polar coordinates to cartesian for plotting
x_lidar = distances * np.cos(np.deg2rad(angles))
y_lidar = distances * np.sin(np.deg2rad(angles))

# Create the figure and GridSpec layout
fig = plt.figure(figsize=(15, 10))
gs = gridspec.GridSpec(2, 3, width_ratios=[1, 1, 1], height_ratios=[1, 1])

# --- LiDAR Environment Map ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(x_lidar, y_lidar, color='blue', s=10, label="Obstacles")
ax1.plot(0, 0, 'ro', markersize=12, label="Robot")
ax1.set_xlim([-6, 6])
ax1.set_ylim([-6, 6])
ax1.set_title('LiDAR Environment Map')
ax1.set_xlabel('X (meters)')
ax1.set_ylabel('Y (meters)')
ax1.legend()
ax1.grid(True)
ax1.set_aspect('equal', adjustable='box')

# --- DTOF Sensor Readings (Bar Plot) ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.bar(dtof_labels, dtof_readings, color='cyan')
ax2.set_ylim([0, 3])
ax2.axhline(y=0.5, color='red', linestyle='--', label="Obstacle Warning Threshold")
ax2.set_title('DTOF Sensor Readings')
ax2.set_ylabel('Distance (meters)')
ax2.legend()

# --- Gyroscope Visualization (Yaw, Pitch, Roll) ---
# Yaw (Compass-style)
ax3 = fig.add_subplot(gs[1, 0], polar=True)
ax3.set_theta_zero_location("N")  # North is 0 degrees
ax3.set_theta_direction(-1)  # Clockwise direction
ax3.set_ylim(0, 1)
ax3.plot(np.deg2rad([0, yaw]), [0, 1], lw=2, label=f'Yaw: {yaw}°', color='orange')
ax3.fill_between(np.deg2rad([0, yaw]), 0, 1, color='orange', alpha=0.3)
ax3.set_title('Gyroscope - Yaw')
ax3.legend()

# Pitch and Roll (Bar Plot)
ax4 = fig.add_subplot(gs[1, 1])
ax4.bar(['Pitch', 'Roll'], [pitch, roll], color=['green', 'blue'])
ax4.set_ylim([-90, 90])
ax4.axhline(0, color='black', lw=1)
ax4.set_title('Gyroscope - Pitch & Roll')

# --- Robot Path with Sensor Data ---
ax5 = fig.add_subplot(gs[1, 2])
sc = ax5.scatter(path_x, path_y, c=dtof_path_data, cmap='plasma', s=10, label="Path")
plt.colorbar(sc, ax=ax5, label="DTOF Distance (m)")
ax5.plot(path_x, path_y, color='gray', linestyle='--', lw=0.5, alpha=0.7)
ax5.plot(0, 0, 'ro', markersize=10, label="Start")
ax5.set_title('Robot Path with Sensor Data')
ax5.set_xlabel('X Position (m)')
ax5.set_ylabel('Y Position (m)')
ax5.legend()
ax5.grid(True)
ax5.set_aspect('equal', adjustable='box')

# --- Speedometer (Circular Gauge) ---
ax6 = fig.add_subplot(gs[0, 2])
max_speed = 180
current_speed = 120  # Replace with dynamic speed data

# Draw speedometer arc
arc = patches.Arc((0, 0), 4, 4, theta1=0, theta2=180, color='black', lw=2)
ax6.add_patch(arc)

# Draw ticks and labels for speedometer
for speed in range(0, max_speed + 1, 20):
    angle = np.deg2rad(180 * speed / max_speed)
    x1, y1 = np.cos(angle) * 1.8, np.sin(angle) * 1.8
    x2, y2 = np.cos(angle) * 2, np.sin(angle) * 2
    ax6.plot([x1, x2], [y1, y2], color='black')
    ax6.text(x2 * 1.1, y2 * 1.1, str(speed), ha='center', va='center', fontsize=10)

# Needle for the speedometer
angle = np.deg2rad(180 * current_speed / max_speed)
needle_length = 2
needle_x = np.cos(angle) * needle_length
needle_y = np.sin(angle) * needle_length
needle = ax6.plot([0, needle_x], [0, needle_y], lw=2, color='red')[0]

# Aesthetics for the speedometer
ax6.set_xlim([-2.5, 2.5])
ax6.set_ylim([-2.5, 2.5])
#ax6.set_title(f'Speed: {current_speed} km/h')
ax6.axis('off')
ax6.set_aspect('equal')

# --- Temperature Sensor Readings ---
ax_temp = fig.add_subplot(gs[0, 2])
ax_temp.bar(['Temperature'], [temperature], color='orange')
ax_temp.set_ylim([0, 40])  # Adjust range based on expected temperature values
ax_temp.axhline(y=30, color='red', linestyle='--', label="Warning Threshold")
ax_temp.set_title('Temperature Sensor Reading')
ax_temp.set_ylabel('Temperature (°C)')
ax_temp.legend()

# Adjust layout and show the complete figure
plt.tight_layout()
plt.show()
