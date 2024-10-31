import pygame
import serial
import time

# Initialize serial communication with Arduino
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Adjust to your Arduinos port
time.sleep(2)  # Allow time for the serial connection

# Initialize pygame for PS4 controller
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

def map_range(value, in_min, in_max, out_min, out_max):
    # Scale joystick values from one range to another
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def send_control_data(speed, steering):
    # Send speed and steering data as comma-separated values
    command = f"{speed},{steering}\n"
    ser.write(command.encode('utf-8'))

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                # Left joystick Y-axis for speed
                left_stick_y = -joystick.get_axis(1)  # Y-axis is usually inverted

                # Right joystick X-axis for steering
                right_stick_x = joystick.get_axis(3)

                # Map joystick values to -100 to 100 range
                speed = map_range(left_stick_y, -1, 1, -100, 100)
                steering = map_range(right_stick_x, -1, 1, -100, 100)

                # Send the control data
                send_control_data(speed, steering)

        #time.sleep(0.001)  # Control loop delay

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()
    pygame.quit()
