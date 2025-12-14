// server.js (CommonJS)
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(bodyParser.json());

// ----------------------------------------------------------------------
// RANDOM NAME DATA
// ----------------------------------------------------------------------
const firstNames = [
  "Jyoti","Anshu","Himanshu","Riya","Neha","Karan","Deepak",
  "Aman","Pooja","Vipin","Rohit","Sakshi","Tanya","Akash",
  "Mohit","Sneha","Harsh","Ankit","Shivani","Komal"
];

const lastNames = [
  "Shakya","Patel","Yadav","Verma","Singh",
  "Gupta","Kapoor","Chauhan","Kushwaha","Mishra"
];

// Random username
function createUsername() {
  const f = firstNames[Math.floor(Math.random() * firstNames.length)];
  const l = lastNames[Math.floor(Math.random() * lastNames.length)];
  return `${f.toLowerCase()}_${l.toLowerCase()}`;
}

// Random profile fields
function randomFirst() {
  return firstNames[Math.floor(Math.random() * firstNames.length)];
}
function randomLast() {
  return lastNames[Math.floor(Math.random() * lastNames.length)];
}
function randomLocation() {
  return "India";
}

// ----------------------------------------------------------------------
// FOLLOWER GENERATOR (FULL PROFILE + SAFE RECURSION)
// ----------------------------------------------------------------------
function generateFollowers(userId, depth = 1, maxDepth = 3) {
  if (depth > maxDepth) return [];

  const followers = [];
  const perUserCount = 50; // you asked "50 totalFollowers"

  for (let i = 1; i <= perUserCount; i++) {
    const fid = `${userId}_${depth}_${i}`;
    const canHaveFollowers = depth < maxDepth;

    followers.push({
      id: fid,
      username: createUsername(),
      firstName: randomFirst(),
      lastName: randomLast(),
      user_location: randomLocation(),
      totalFollowers: canHaveFollowers ? perUserCount : 0,
      followers: canHaveFollowers ? generateFollowers(fid, depth + 1, maxDepth) : []
    });
  }

  return followers;
}

// ----------------------------------------------------------------------
// MAIN USER
// ----------------------------------------------------------------------
const igUsers = {};

function createMainUser() {
  const mainId = "133094043977116573";

  igUsers[mainId] = {
    id: mainId,
    username: "manoj_shakya",
    firstName: "Manoj",
    lastName: "Shakya",
    user_location: "Kanpur, India",
    totalFollowers: 50,
    followers: generateFollowers(mainId)
  };
}

createMainUser();

// ----------------------------------------------------------------------
// FORMAT RESPONSE (NO EMPTY FIELDS)
// ----------------------------------------------------------------------
function formatUser(user) {
  return {
    id: user.id,
    username: user.username,
    firstName: user.firstName || randomFirst(),
    lastName: user.lastName || randomLast(),
    user_location: user.user_location || randomLocation(),
    totalFollowers: user.totalFollowers,
    followers: user.followers.map(f => formatUser(f))
  };
}

// ----------------------------------------------------------------------
// UTILS: Pagination
// ----------------------------------------------------------------------
function paginateArray(array, page = 1, limit = 20) {
  page = parseInt(page);
  limit = parseInt(limit);

  const start = (page - 1) * limit;
  const end = page * limit;

  return {
    page,
    limit,
    total: array.length,
    data: array.slice(start, end)
  };
}

// UTILS: Cursor Pagination
function cursorPaginate(array, cursor, limit = 20) {
  limit = parseInt(limit);

  let startIndex = 0;

  // If cursor exists, find its index
  if (cursor) {
    startIndex = array.findIndex(item => item.id === cursor);
    if (startIndex === -1) startIndex = 0;
    else startIndex += 1; // Start after cursor
  }

  const endIndex = startIndex + limit;

  const nextCursor = endIndex < array.length ? array[endIndex - 1].id : null;

  return {
    limit,
    nextCursor,
    data: array.slice(startIndex, endIndex)
  };
}

// ----------------------------------------------------------------------
// API 1: GET FULL USER + FOLLOWER TREE
// ----------------------------------------------------------------------
app.get("/ig/:id", (req, res) => {
  const id = req.params.id;
  const user = igUsers[id];

  if (!user) return res.status(404).json({ error: "User not found" });

  res.json(formatUser(user));
});

// ----------------------------------------------------------------------
// API 2: PAGINATION — GET FOLLOWERS
// ----------------------------------------------------------------------
app.get("/ig/:id/followers", (req, res) => {
  const id = req.params.id;
  const user = igUsers[id];

  if (!user) return res.status(404).json({ error: "User not found" });

  const { page, limit, cursor } = req.query;

  // Cursor pagination priority
  if (cursor) {
    return res.json(cursorPaginate(user.followers, cursor, limit));
  }

  // Normal pagination
  return res.json(paginateArray(user.followers, page, limit));
});

// ----------------------------------------------------------------------
app.listen(PORT, () =>
  console.log(`Mock IG server running on port ${PORT}`)
);
