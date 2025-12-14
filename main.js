const express = require('express');
const axios = require('axios');
const app = express();

// ===== APNI VALUES YAHAN DAALO =====
const APP_ID = '2008477996672023';  // developers.facebook.com se
const APP_SECRET = '246058a77a3c47a61891d2cfba6b2def';   // same jagah se
const REDIRECT_URI = 'http://localhost:9000/callback';  // tumhara callback URL
// =================================

app.get('/instagram/connect', (req, res) => {
    const loginUrl = `https://www.facebook.com/v20.0/dialog/oauth?client_id=${APP_ID}&redirect_uri=${REDIRECT_URI}&scope=instagram_basic,pages_show_list,instagram_manage_insights&response_type=code`;
    res.redirect(loginUrl);
});

app.get('/callback', async (req, res) => {
    const { code } = req.query;
    
    if (!code) {
        return res.send('❌ Login failed - No code received');
    }

    try {
        // 1. Code se short-lived token
        const tokenResponse = await axios({
            method: 'GET',
            url: 'https://graph.facebook.com/v20.0/oauth/access_token',
            params: {
                client_id: APP_ID,
                client_secret: APP_SECRET,
                redirect_uri: REDIRECT_URI,
                code: code
            }
        });

        const shortToken = tokenResponse.data.access_token;

        // 2. Short → Long-lived token
        const longTokenResponse = await axios({
            method: 'GET',
            url: 'https://graph.facebook.com/v20.0/oauth/access_token',
            params: {
                grant_type: 'fb_exchange_token',
                client_id: APP_ID,
                client_secret: APP_SECRET,
                fb_exchange_token: shortToken
            }
        });

        const accessToken = longTokenResponse.data.access_token;

        // 3. User ke FB Pages + linked IG accounts
        const accountsResponse = await axios({
            method: 'GET',
            url: 'https://graph.facebook.com/v20.0/me/accounts',
            params: { access_token: accessToken }
        });

        const igBusinessId = accountsResponse.data.data[0]?.instagram_business_account?.id;
        
        if (!igBusinessId) {
            return res.send('❌ No Instagram Business Account found. Convert to Professional first.');
        }

        // 4. YEHI WALA USER_ID TUMHE CHAHIYE!
        const igUserResponse = await axios({
            method: 'GET',
            url: `https://graph.facebook.com/v20.0/${igBusinessId}`,
            params: {
                fields: 'id,username,followers_count,media_count',
                access_token: accessToken
            }
        });

        const userData = igUserResponse.data;
        
        // SUCCESS SCREEN
        res.send(`
            <h1>✅ Instagram Connected!</h1>
            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">
                <h2>Details Saved:</h2>
                <p><strong>Instagram User ID:</strong> ${userData.id}</p>
                <p><strong>Username:</strong> @${userData.username}</p>
                <p><strong>Followers:</strong> ${userData.followers_count}</p>
                <p><strong>Total Posts:</strong> ${userData.media_count}</p>
                <hr>
                <p><em>Ab ye user_id tumhare DB me save kar lo</em></p>
            </div>
        `);

        console.log('🎉 USER_ID MIL GAYA:', userData.id);

    } catch (error) {
        console.error(error.response?.data);
        res.send(`❌ Error: ${error.response?.data?.error?.message || error.message}`);
    }
});

app.listen(9000, () => {
    console.log('🚀 Server ready on http://localhost:9000');
    console.log('Button URL: http://localhost:9000');
});
