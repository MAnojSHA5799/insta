// receive-server.js
const express = require("express");
const app = express();

// Accept very large payloads
app.use(express.json({ limit: "100mb" }));
app.use(express.urlencoded({ extended: true, limit: "100mb" }));

app.post("/receive", (req, res) => {
  const { videoUrl, users } = req.body;

  console.log(`📥 Received ${users.length} users | Video: ${videoUrl}`);

  // Simulate 1-second processing delay
  setTimeout(() => {
    res.json({ status: "ok", received: users.length });
  }, 1000);
});

app.listen(9000, () => console.log("📡 Receiver running on PORT 9000"));
