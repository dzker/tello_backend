const express = require('express');
const dgram = require('dgram');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const PORT = 3000;
const QR_PORT = 4000;

// Serve the frontend (if any)
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/test_front_end/index.html');
});

// Socket.io for real-time communication
io.on('connection', (socket) => {
    console.log('A user connected');
});

// UDP socket for receiving QR data from Python
const qrSocket = dgram.createSocket('udp4');
qrSocket.on('message', (msg, rinfo) => {
    const qrData = msg.toString();
    console.log('QR Code Received:', qrData);

    // Broadcast QR data to the frontend
    io.emit('qr-code-detected', qrData);

    // Example: Control Tello based on QR code
    if (qrData === 'takeoff') {
        console.log('Command: Takeoff');
        // Send Tello takeoff command here
    } else if (qrData === 'land') {
        console.log('Command: Land');
        // Send Tello land command here
    }
});

qrSocket.bind(QR_PORT, () => {
    console.log(`Listening for QR code data on port ${QR_PORT}`);
});

// Start the server
server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});