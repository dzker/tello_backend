const express = require('express');
const dgram = require('dgram');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path'); // Import path module for resolving file paths

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const PORT = 3000;
const QR_PORT = 4000;

// Serve static files from the 'public' folder
app.use(express.static(path.join(__dirname, 'test_front_end')));

// Handle root route to serve index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'test_front_end', 'index.html'));
});

// Socket.IO for real-time communication
io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('disconnect', () => {
        console.log('A user disconnected');
    });
});

// UDP socket for receiving QR data from Python
const qrSocket = dgram.createSocket('udp4');
qrSocket.on('message', (msg) => {
    const qrData = msg.toString();
    console.log('QR Code Received:', qrData);

    // Broadcast QR data to the frontend
    io.emit('qr-code-detected', qrData);
});

qrSocket.bind(QR_PORT, () => {
    console.log(`Listening for QR code data on port ${QR_PORT}`);
});

// Start the server
server.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});