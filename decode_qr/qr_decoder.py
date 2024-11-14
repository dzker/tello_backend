from djitellopy import Tello
import socketio
import time

# Configure Socket.IO
SERVER_URL = "http://localhost:3000"  # Update with your server URL
sio = socketio.Client()

# Connect to the Node.js server
@sio.event
def connect():
    print("Connected to the Node.js server!")

@sio.event
def disconnect():
    print("Disconnected from the Node.js server!")

sio.connect(SERVER_URL)

# Initialize Tello
tello = Tello()
tello.connect()

print(f"Connected to Tello Drone: Battery Level {tello.get_battery()}%")

try:
    while True:
        # Get battery level from Tello
        battery_level = tello.get_battery()
        print(f"Battery Level: {battery_level}%")

        # Send battery level to Node.js server
        sio.emit('battery-level', battery_level)

        # Wait for a while before sending the next update
        time.sleep(10)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    tello.end()
    sio.disconnect()