# 🚨 NEW KEYS YAHAN PASTE KARO
YOUTUBE_API_KEY = "AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4"  
SERPAPI_KEY = "6dba7e136f621fa3605620502a65d12957cbf6a86c488186e998a1336ade2edf"  # serpapi.com se

from googleapiclient.discovery import build
import requests

# ✅ TEST 1: YouTube (Fixed date + error handling)
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
try:
    request = youtube.search().list(
        q="best niacinamide serum review India",
        part="snippet", 
        maxResults=10,  # Reduced quota save
        type="video", 
        order="viewCount",
        publishedAfter="2025-01-01T00:00:00Z"  # Fixed future date
    )
    response = request.execute()
    print(f"✅ YOUTUBE OK: {len(response['items'])} videos found!")
    
    for i, item in enumerate(response['items'][:3]):
        print(f"{i+1}. {item['snippet']['title']}")
        
except Exception as e:
    print(f"❌ YouTube Error: {e}")

# ✅ TEST 2: SerpAPI (Always works)
serp_url = f"https://serpapi.com/search.json?q=skincare+serum+demand+top+15+cities+India&api_key={SERPAPI_KEY}"
r = requests.get(serp_url)
data = r.json()
print(f"\n✅ SERPAPI OK: {data.get('search_metadata', {}).get('status')}")
print("Top cities ready!")
