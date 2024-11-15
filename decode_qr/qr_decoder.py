from djitellopy import Tello
from pyzbar.pyzbar import decode
import cv2
import socket
import threading
import time

# Tello initialization
tello = Tello()
tello.connect()

# UDP socket setup to send data to Node.js
SERVER_IP = '127.0.0.1'  # Node.js server IP
SERVER_PORT = 4000       # Node.js server QR_PORT
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_to_server(data):
    try:
        sock.sendto(data.encode(), (SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(f"Error sending data: {e}")

# Function to continuously display battery level
def display_battery_level():
    while True:
        try:
            battery_level = tello.get_battery()
            print(f"[Battery Level]: {battery_level}%")
            time.sleep(5)  # Update battery level every 5 seconds
        except Exception as e:
            print(f"Error retrieving battery level: {e}")

# Start the battery level thread
battery_thread = threading.Thread(target=display_battery_level, daemon=True)
battery_thread.start()

# Start video stream from Tello
tello.streamon()
cap = tello.get_frame_read()

try:
    print("QR Code Scanner is running. Press Ctrl+C to stop.")
    while True:
        # Get the current frame
        frame = cap.frame

        # Decode QR codes in the frame
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"[QR Code Detected]: {qr_data}")

            # Send QR data to the server
            send_to_server(qr_data)

            # Example Tello commands based on QR data
            if qr_data == 'takeoff':
                print("[Command]: Takeoff")
                tello.takeoff()
            elif qr_data == 'land':
                print("[Command]: Land")
                tello.land()

        # Display the frame
        cv2.imshow("Tello QR Scanner", frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Cleanup
    tello.streamoff()
    tello.end()
    cv2.destroyAllWindows()