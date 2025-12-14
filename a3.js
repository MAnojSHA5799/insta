// server.js
const express = require("express");
const app = express();
const PORT = 8000;

app.use(express.json());

/**
 * Chunked Crore Loop Function
 * Safe Non-Blocking Loop
 */
function runCroreChunked(total, batchSize, onProgress, onDone) {
  let i = 0;
  let sum = 0;

  const tick = () => {
    const end = Math.min(i + batchSize, total);

    for (; i < end; i++) {
      sum += i; // your work here
    }

    onProgress(i, total);

    if (i < total) {
      // give back control to event-loop (non-blocking)
      if (typeof setImmediate === "function") {
        setImmediate(tick);
      } else {
        setTimeout(tick, 0);
      }
    } else {
      onDone(sum);
    }
  };

  tick();
}

/**
 * API: Start 1 Crore Loop
 */
app.get("/run-crore", (req, res) => {
  const TOTAL = 10_000_000;  // 1 Crore = 1,00,00,000 (India style)
  const BATCH = 50_000;      // safe batch size

  console.log("Loop Started...");

  const startTime = Date.now();

  runCroreChunked(
    TOTAL,
    BATCH,
    (done, total) => {
      // progress (optional)
      const percent = ((done / total) * 100).toFixed(2);
      process.stdout.write(`Progress: ${percent}%\r`);
    },
    (result) => {
      const totalTime = (Date.now() - startTime) / 1000;
      console.log("\nLoop Finished!");
      console.log("Result =", result);
      console.log("Time =", totalTime, "seconds");
    }
  );

  res.json({
    status: "started",
    message: `1 crore loop started (total: ${TOTAL})`,
  });
});

/**
 * Start Server
 */
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
