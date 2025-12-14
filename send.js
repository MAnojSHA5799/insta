// // bulk-sender.js
// const express = require("express");
// const axios = require("axios");

// const app = express();
// app.use(express.json());

// // -------------------------------
// // Create 3,20,000 Dummy Users
// // -------------------------------
// const users = Array.from({ length: 320000 }, (_, i) => ({
//   id: i + 1,
//   name: `User_${i + 1}`,
// }));

// // --------------------------------------------------------
// // Function to Send Users in Batches (1000 users each batch)
// // --------------------------------------------------------
// async function sendVideoInBatches(videoUrl, batchSize =3000, delayMs = 3000) {
//   console.log("🚀 Sending Started for 3,20,000 Users...");

//   for (let i = 0; i < users.length; i += batchSize) {
//     const batch = users.slice(i, i + batchSize);

//     console.log(`📤 Sending Batch ${i / batchSize + 1} (${batch.length} users)`);

//     try {
//       // Send to another server
//       await axios.post("http://localhost:9000/receive", {
//         videoUrl,
//         users: batch,
//       });

//       console.log(`✅ Batch Delivered (${batch.length} users)`);

//     } catch (error) {
//       console.log("❌ Error sending batch:", error.message);
//     }

//     // Wait 5 seconds before sending next batch
//     await new Promise(resolve => setTimeout(resolve, delayMs));
//   }

//   console.log("🎉 All Batches Sent Successfully!");
// }

// // --------------------------------------------------------
// // API: Trigger Sending
// // --------------------------------------------------------
// app.post("/send-video", (req, res) => {
//   const { videoUrl } = req.body;

//   if (!videoUrl) {
//     return res.status(400).json({ error: "videoUrl is required" });
//   }

//   // Start process in background
//   sendVideoInBatches(videoUrl);

//   res.json({
//     status: "Sending started...",
//     totalUsers: users.length,
//     batchSize: 3000,
//     delay: "5 seconds",
//   });
// });

// app.listen(8000, () => {
//   console.log("📡 Bulk Sender Server running on PORT 8000");
// });


// bulk-sender.js
// bulk-sender.js
// bulk-sender.js
const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json({ limit: "50mb" }));

// --------------------------------
// Create 3,20,000 Dummy Users
// --------------------------------
const users = Array.from({ length: 1240000 }, (_, i) => ({
  id: i + 1,
  name: `User_${i + 1}`,
}));

// --------------------------------
// Format time ms → mm:ss
// --------------------------------
function formatTime(ms) {
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);
  return `${minutes}m ${seconds}s`;
}

// --------------------------------
// Safe Batch Sender with Retry
// --------------------------------
async function sendBatch(videoUrl, batch) {
  const maxRetries = 3;
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      await axios.post(
        "http://localhost:9000/receive",
        { videoUrl, users: batch },
        {
          maxBodyLength: Infinity,
          maxContentLength: Infinity,
          timeout: 20000,
        }
      );
      return true;
    } catch (err) {
      attempt++;
      console.log(`⚠️ Attempt ${attempt} failed: ${err.message}`);

      if (attempt === maxRetries) {
        console.log("❌ Max retries reached. Skipping batch...");
        return false;
      }

      console.log("🔁 Retrying in 2 seconds...");
      await new Promise((r) => setTimeout(r, 2000));
    }
  }
}

// --------------------------------
// Main Bulk Sending Function
// --------------------------------
async function sendVideoInBatches(videoUrl, batchSize = 10000, delayMs = 5000) {
  console.log("\n🚀 Sending Started for 3,20,000 Users...\n");

  const totalBatches = Math.ceil(users.length / batchSize);
  const startTime = Date.now();

  for (let i = 0; i < users.length; i += batchSize) {
    const batchNumber = i / batchSize + 1;
    const batch = users.slice(i, i + batchSize);

    console.log(`\n📤 Sending Batch ${batchNumber}/${totalBatches} (${batch.length} users)`);

    const batchStart = Date.now();
    const success = await sendBatch(videoUrl, batch);

    const batchEnd = Date.now();
    const batchTime = batchEnd - batchStart;

    if (success) {
      console.log(`✅ Batch Delivered in ${formatTime(batchTime)}`);
    } else {
      console.log("⚠️ Batch Failed After Retry");
    }

    const remaining = totalBatches - batchNumber;
    console.log(`⏳ Batches Left: ${remaining}`);

    console.log(`⏸ Waiting ${delayMs / 1000} seconds...`);
    await new Promise((r) => setTimeout(r, delayMs));
  }

  const totalTime = Date.now() - startTime;
  console.log("\n🎉 All Batches Processed!");
  console.log(`⏱ Total Time Taken: ${formatTime(totalTime)}\n`);
}

// --------------------------------
// API Trigger
// --------------------------------
app.post("/send-video", (req, res) => {
  const { videoUrl } = req.body;

  if (!videoUrl) {
    return res.status(400).json({ error: "videoUrl is required" });
  }

  sendVideoInBatches(videoUrl);

  res.json({
    status: "Sending started...",
    totalUsers: users.length,
    batchSize: 10000,
    delay: "5 seconds",
  });
});

app.listen(8000, () => console.log("📡 Bulk Sender running on PORT 8000"));
