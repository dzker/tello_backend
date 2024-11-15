from djitellopy import Tello
import cv2
from pyzbar.pyzbar import decode
import socket

# Node.js server details
SERVER_IP = '127.0.0.1'  # Replace with your Node.js server IP
SERVER_PORT = 4000

# Set up a UDP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize Tello
tello = Tello()
tello.connect()

print(f"Battery Level: {tello.get_battery()}%")

# Start video stream
tello.streamon()

def decode_qr(frame):
    """Detect and decode QR codes in the video frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    for barcode in barcodes:
        qr_data = barcode.data.decode('utf-8')
        print(f"QR Code Detected: {qr_data}")
        # Send QR data to Node.js server
        client_socket.sendto(qr_data.encode(), (SERVER_IP, SERVER_PORT))

try:
    print("Starting QR code detection...")
    while True:
        # Get the Tello video frame
        frame = tello.get_frame_read().frame
        frame = cv2.resize(frame, (960, 720))  # Resize frame for better display
        
        # Decode QR codes
        decode_qr(frame)
        
        # Display the video feed
        cv2.imshow("Tello Camera", frame)

        # Stop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    # Clean up resources
    tello.streamoff()
    cv2.destroyAllWindows()
    client_socket.close()