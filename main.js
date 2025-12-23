const express = require('express');
const axios = require('axios');
const app = express();

// ===== APNI VALUES YAHAN DAALO (BAAD ME .env ME LE JANA) =====
const APP_ID = '2489693924757448';         // developers.facebook.com se
const APP_SECRET = '56dbdecdec3b5b19397da2c1570cbfd6';  // same jagah se
// LOCAL TEST KE LIYE:
const REDIRECT_URI = 'http://localhost:9000/callback';
// =================================

app.get('/instagram/connect', (req, res) => {
  // ❌ instagram_basic, instagram_manage_insights hata diye (invalid scopes ka error aa raha tha)
  const loginUrl =
    `https://www.facebook.com/v20.0/dialog/oauth` +
    `?client_id=${APP_ID}` +
    `&redirect_uri=${encodeURIComponent(REDIRECT_URI)}` +
    `&scope=pages_show_list,pages_read_engagement` +
    `&response_type=code`;
  
  console.log('🔗 Redirecting to:', loginUrl);
  res.redirect(loginUrl);
});

app.get('/callback', async (req, res) => {
  const { code } = req.query;

  console.log('🔍 CALLBACK HIT, code =', code);

  if (!code) {
    return res.send('❌ Login failed - No code received');
  }

  try {
    // 1. Code se short-lived token
    console.log('📥 STEP 1: Getting short-lived token...');
    const tokenResponse = await axios({
      method: 'GET',
      url: 'https://graph.facebook.com/v20.0/oauth/access_token',
      params: {
        client_id: APP_ID,
        client_secret: APP_SECRET,
        redirect_uri: REDIRECT_URI,
        code
      }
    });

    const shortToken = tokenResponse.data.access_token;
    console.log('✅ Short token OK');

    // 2. Short → Long-lived token
    console.log('📈 STEP 2: Exchanging for long-lived token...');
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
    console.log('✅ Long token OK');

    // 3. User ke FB Pages + linked IG accounts
    console.log('📋 STEP 3: Fetching pages...');
    const accountsResponse = await axios({
      method: 'GET',
      url: 'https://graph.facebook.com/v20.0/me/accounts',
      params: { access_token: accessToken }
    });

    console.log('Pages response:', JSON.stringify(accountsResponse.data, null, 2));

    const firstPage = accountsResponse.data.data?.[0];
    const igBusinessId = firstPage?.instagram_business_account?.id;

    if (!igBusinessId) {
      return res.send(`
        ❌ No Instagram Business Account found. 
        <br/>Ensure:
        <ul>
          <li>Instagram account is Professional (Business/Creator)</li>
          <li>Instagram is connected to this Facebook Page</li>
        </ul>
      `);
    }

    // 4. YEHI WALA USER_ID TUMHE CHAHIYE!
    console.log('👤 STEP 4: Fetching IG user details for', igBusinessId);
    const igUserResponse = await axios({
      method: 'GET',
      url: `https://graph.facebook.com/v20.0/${igBusinessId}`,
      params: {
        fields: 'id,username,followers_count,media_count',
        access_token: accessToken
      }
    });

    const userData = igUserResponse.data;

    console.log('🎉 USER_ID MIL GAYA:', userData.id);

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
  } catch (error) {
    console.error('💥 ERROR:', error.response?.data || error.message);
    res.send(`❌ Error: ${error.response?.data?.error?.message || error.message}`);
  }
});

app.listen(9000, () => {
  console.log('🚀 Server ready on http://localhost:9000');
  console.log('Button URL: http://localhost:9000/instagram/connect');
  console.log('Callback URL (Facebook settings me add karo):', REDIRECT_URI);
});





// const express = require('express');
// const axios = require('axios');
// const app = express();

// // ===== APNI VALUES YAHAN DAALO (LOCAL TEST KE LIYE) =====
// // ===== APNI VALUES YAHAN DAALO =====
// const APP_ID = '2008477996672023';  // developers.facebook.com se
// const APP_SECRET = '246058a77a3c47a61891d2cfba6b2def';   // same jagah se
// const REDIRECT_URI = 'https://insta-amber-six.vercel.app/callback';  // tumhara callback URL
// // =================================

// app.get('/instagram/connect', (req, res) => {
//     console.log('🔗 Going to Facebook Login...');
//     const loginUrl = `https://www.facebook.com/v20.0/dialog/oauth?client_id=${APP_ID}&redirect_uri=${REDIRECT_URI}&scope=pages_show_list,pages_read_engagement,instagram_business_account,instagram_manage_insights&response_type=code`;
//     console.log('Login URL:', loginUrl);
//     res.redirect(loginUrl);
// });

// app.get('/callback', async (req, res) => {
//     const { code } = req.query;
//     console.log('🔍 CALLBACK HIT! Code:', code ? 'YES' : 'NO');
    
//     if (!code) {
//         return res.send('❌ Login failed - No code received. <a href="/instagram/connect">Try Again</a>');
//     }

//     try {
//         console.log('📥 STEP 1: Short token...');
//         // 1. Code se short-lived token
//         const tokenResponse = await axios({
//             method: 'GET',
//             url: 'https://graph.facebook.com/v20.0/oauth/access_token',
//             params: {
//                 client_id: APP_ID,
//                 client_secret: APP_SECRET,
//                 redirect_uri: REDIRECT_URI,
//                 code: code
//             }
//         });
//         const shortToken = tokenResponse.data.access_token;
//         console.log('✅ STEP 1 OK');

//         console.log('📈 STEP 2: Long token...');
//         // 2. Short → Long-lived token
//         const longTokenResponse = await axios({
//             method: 'GET',
//             url: 'https://graph.facebook.com/v20.0/oauth/access_token',
//             params: {
//                 grant_type: 'fb_exchange_token',
//                 client_id: APP_ID,
//                 client_secret: APP_SECRET,
//                 fb_exchange_token: shortToken
//             }
//         });
//         const accessToken = longTokenResponse.data.access_token;
//         console.log('✅ STEP 2 OK');

//         console.log('📋 STEP 3: Pages...');
//         // 3. User ke FB Pages + linked IG accounts
//         const accountsResponse = await axios({
//             method: 'GET',
//             url: 'https://graph.facebook.com/v20.0/me/accounts',
//             params: { access_token: accessToken }
//         });
        
//         console.log('Pages count:', accountsResponse.data.data.length);
//         console.log('First page:', accountsResponse.data.data[0]);

//         const igBusinessId = accountsResponse.data.data[0]?.instagram_business_account?.id;
        
//         if (!igBusinessId) {
//             console.log('❌ NO IG BUSINESS ID!');
//             return res.send(`
//                 ❌ No Instagram Business Account found. 
//                 <br><br>
//                 <strong>Debug:</strong> ${accountsResponse.data.data.length} pages found
//                 <br>
//                 <a href="/instagram/connect">Try Again</a>
//             `);
//         }
//         console.log('✅ IG ID:', igBusinessId);

//         console.log('👤 STEP 4: User details...');
//         // 4. YEHI WALA USER_ID TUMHE CHAHIYE!
//         const igUserResponse = await axios({
//             method: 'GET',
//             url: `https://graph.facebook.com/v20.0/${igBusinessId}`,
//             params: {
//                 fields: 'id,username,followers_count,media_count',
//                 access_token: accessToken
//             }
//         });

//         const userData = igUserResponse.data;
//         console.log('🎉 USER_ID:', userData.id);

//         // SUCCESS SCREEN
//         res.send(`
//             <h1>✅ Instagram Connected!</h1>
//             <div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">
//                 <h2>Details:</h2>
//                 <p><strong>Instagram User ID:</strong> ${userData.id}</p>
//                 <p><strong>Username:</strong> @${userData.username}</p>
//                 <p><strong>Followers:</strong> ${userData.followers_count}</p>
//                 <p><strong>Total Posts:</strong> ${userData.media_count}</p>
//                 <hr>
//                 <p><em>SAVE YE USER_ID!</em></p>
//             </div>
//         `);

//     } catch (error) {
//         console.error('💥 ERROR:', error.response?.data);
//         res.send(`❌ Error: ${error.response?.data?.error?.message || error.message}`);
//     }
// });

// app.listen(9000, () => {
//     console.log('🚀 Server: http://localhost:9000');
//     console.log('📱 Connect: http://localhost:9000/instagram/connect');
// });

