// server.js
require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// 1) Followers fetch logic (Graph API / provider placeholder)
async function fetchFollowers(igUserId, afterCursor) {
  const accessToken = 'EAAciszmH5BcBQJBgYj3ZB0XLHUzZA1mciTwa7dDZCyo6KaCzTfcAoZC5wONEox1HCoaZCZB3Tm54oZADZBAKWZB6lTtnXTWNxI5MjEHoi6IW2yjFZC2naUWLdufYqZB0HRluCj8Q6JNzZAhVERl7XLsUbSJNj3NZARfAoPfeZBsnOylejndpxISybkhiVuOHJ4Ffa0nMqenljQccfUUMtN0uyK3pbZAvFKQZCRKEm7i3D6ZA7cAExVZAlEwwP2WZBBZBjBIeZCZAXD2gKccZAUTSZBK7SiR5xoCcGl0g6t2y'; // ya API_KEY
  const params = {
    access_token: accessToken,
    limit: 50,
  };
  if (afterCursor) params.after = afterCursor;

  const url = `https://graph.facebook.com/v18.0/${igUserId}/followers`; // example endpoint
  const { data } = await axios.get(url, { params });
  return data;
}

// 2) Single call endpoint (pagination handle on client)
app.get('/followers', async (req, res) => {
  try {
    const { igUserId, after } = req.query;
    if (!igUserId) return res.status(400).json({ error: 'igUserId required' });

    const data = await fetchFollowers(igUserId, after);
    // data.data = followers list, data.paging.next / cursors for next page
    res.json({
      followers: data.data,
      paging: data.paging || null
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// 3) Full list endpoint (server‑side pagination loop)
app.get('/followers/all', async (req, res) => {
  try {
    const { igUserId } = req.query;
    if (!igUserId) return res.status(400).json({ error: 'igUserId required' });

    let allFollowers = [];
    let after = undefined;

    while (true) {
      const data = await fetchFollowers(igUserId, after);
      allFollowers = allFollowers.concat(data.data || []);

      if (!data.paging || !data.paging.cursors || !data.paging.cursors.after) break;
      after = data.paging.cursors.after;
      if (allFollowers.length >= 10000) break; // safety limit
    }

    res.json({ count: allFollowers.length, followers: allFollowers });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.listen(3000, () => console.log('API running on 3000'));
