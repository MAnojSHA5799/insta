// server.js
const express = require("express");
const app = express();

// --------------------------------------------------------
// Instagram-style console error
// --------------------------------------------------------
console.error(`
================= INSTAGRAM ERROR =================

User: https://www.instagram.com/manojshakya3409/

Action Blocked
Try again later.

We limit how often you can do certain things on Instagram 
to protect our community.

This action was blocked. Please wait a few minutes 
before you try again.

===================================================
`);


// --------------------------------------------------------
// REAL INSTAGRAM-LIKE ERROR RESPONSE
// --------------------------------------------------------
app.get("/instagram/manojshakya3409", (req, res) => {
  return res.status(429).json({
    status: false,
    user: "https://www.instagram.com/manojshakya3409/",
    title: "Action Blocked",
    message_1: "Try again later.",
    message_2:
      "We limit how often you can do certain things on Instagram to protect our community.",
    message_3:
      "This action was blocked. Please wait a few minutes before you try again.",
    error_type: "action_blocked",
    timestamp: new Date().toISOString(),
  });
});


// --------------------------------------------------------
app.listen(8000, () => {
  console.log("Server started on port 8000");
});
