const express = require("express");
const http = require("http");
const WebSocket = require('ws');
const CharacterAI = require("node_characterai");
const characterAI = new CharacterAI();
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors()); // Enable CORS for all routes

characterAI.authenticateAsGuest();

app.post("/", async (req, res) => {
  try {
    // Authenticating as a guest (use `.authenticateWithToken()` to use an account)

    // Place your character's id here
    const characterId = "DxbivEWgDGIk54IHP2YUBveZWmq4rT_g6VNZeEX-yHU"; // Use your character id here

    const chat = await characterAI.createOrContinueChat(characterId);

    // Extract user input from the request
    const userInput = req.body.input;

    // Send a message
    const response = await chat.sendAndAwaitResponse(userInput, true);

    res.json({ aiResponse: response.text });
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.post('/check_url', async (req, res) => {
    try {
      const response = await fetch('http://5e14-34-150-222-5.ngrok-free.app/check_url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(req.body),
      });
      const data = await response.json();
      res.json(data);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'An error occurred' });
    }
  });

const server = http.createServer(app);

// Create a WebSocket server
const wss = new WebSocket.Server({ noServer: true });

wss.on('connection', (ws) => {
  // Handle WebSocket connections here
  ws.on('message', (message) => {
    // Handle WebSocket messages
    console.log(`Received WebSocket message: ${message}`);
    
    // You can send a response back through WebSocket if needed
    // ws.send('You sent: ' + message);
  });
});

server.on('upgrade', (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, (ws) => {
    wss.emit('connection', ws, request);
  });
});

const PORT = 5776;

server.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
