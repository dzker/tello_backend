const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const dgram = require('dgram');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const PORT = 3000;
const PYTHON_PORT = 5000; // Port for communication with Python backend
const PYTHON_HOST = '127.0.0.1'; // Python backend address

const udpClient = dgram.createSocket('udp4');

// Serve static files
app.use(express.static('test_front_end'));

io.on('connection', (socket) => {
    console.log('A user connected');

    // Listen for commands from the frontend
    socket.on('drone-command', (command) => {
        console.log(`Command received: ${command}`);
        
        // Forward command to the Python backend
        udpClient.send(command, PYTHON_PORT, PYTHON_HOST, (err) => {
            if (err) {
                console.error(`Error sending command: ${err}`);
            }
        });
    });

    socket.on('disconnect', () => {
        console.log('A user disconnected');
    });
});

server.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});