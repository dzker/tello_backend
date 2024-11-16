import socket
from djitellopy import Tello
import threading

# Tello initialization
tello = Tello()
tello.connect()

# UDP server setup
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

# Command handler
def handle_command(command):
    print(f"Received command: {command}")
    if command == "takeoff":
        tello.takeoff()
    elif command == "land":
        tello.land()
    elif command == "forward":
        tello.move_forward(30)
    elif command == "backward":
        tello.move_back(30)
    elif command == "left":
        tello.move_left(30)
    elif command == "right":
        tello.move_right(30)
    elif command == "up":
        tello.move_up(30)
    elif command == "down":
        tello.move_down(30)
    elif command == "rotate_ccw":
        tello.rotate_counter_clockwise(30)
    elif command == "rotate_cw":
        tello.rotate_clockwise(30)

# Listen for commands
def listen_for_commands():
    print("Listening for commands...")
    while True:
        data, addr = sock.recvfrom(1024)
        command = data.decode("utf-8")
        handle_command(command)

# Start the command listener in a thread
listener_thread = threading.Thread(target=listen_for_commands, daemon=True)
listener_thread.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
finally:
    tello.end()
    sock.close()