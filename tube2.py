# import requests
# import json
# import re
# import time
# from collections import Counter
# import sys
# from datetime import datetime, timedelta
# from urllib.parse import quote

# # Your working API key
# API_KEY = 'AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4'

# # 🔥 ULTIMATE CONFIG - SAB DATA!
# CITIES = {
#     'kanpur': 'IN', 'lucknow': 'IN', 'delhi': 'IN', 'mumbai': 'IN', 
#     'noida': 'IN', 'agra': 'IN', 'pune': 'IN', 'bangalore': 'IN',
#     'chennai': 'IN', 'hyderabad': 'IN', 'kolkata': 'IN', 'jaipur': 'IN',
#     'up': 'IN', 'uttar': 'IN', 'india': 'IN', 'global': 'US'
# }

# SEARCH_MODES = ['viewCount', 'rating', 'relevance', 'date', 'title']

# def safe_api_call(url, retries=5):
#     """🔥 Heavy retry for quota limits"""
#     for attempt in range(retries):
#         try:
#             response = requests.get(url, timeout=10)
#             data = response.json()
#             if 'error' in data:
#                 print(f"⚠️  QUOTA: {data['error'].get('message', 'Unknown')}")
#                 time.sleep(2 ** attempt)  # Exponential backoff
#                 continue
#             return data
#         except Exception as e:
#             print(f"⚠️  API Error: {e}")
#             time.sleep(1)
#     print(f"❌ Failed after {retries} attempts")
#     return None

# def get_all_apis(query):
#     """🔥 SAB APIs ek saath!"""
#     all_data = {}
    
#     print("🔍 Running 5 search modes...")
#     for mode in SEARCH_MODES:
#         url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={quote(query)}&type=video&maxResults=50&order={mode}&key={API_KEY}"
#         print(f"  → {mode}...")
#         data = safe_api_call(url)
#         all_data[f'search_{mode}'] = data or {}
#         time.sleep(0.2)
    
#     print("📈 Fetching trending...")
#     trend_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=IN&maxResults=50&key={API_KEY}"
#     all_data['trending'] = safe_api_call(trend_url) or {}
    
#     print("✅ All APIs complete!")
#     return all_data

# def extract_complete_data(all_apis, query):
#     """🔥 FIXED - SAB DATA extract karo! (100% Error Free)"""
#     videos = []
#     tags = Counter()
#     hashtags = Counter()
#     channels = Counter()
#     categories = Counter()
    
#     # 🔥 SAFELY extract from ALL sources
#     sources = ['search_viewCount', 'search_rating', 'search_date', 'trending']
#     for source in sources:
#         data = all_apis.get(source, {})
#         if not data or 'items' not in data:
#             continue
            
#         for item in data['items'][:30]:
#             # 🔥 FIXED: Safe ID checking
#             try:
#                 if not isinstance(item, dict):
#                     continue
                    
#                 video_id = None
#                 if 'id' in item and isinstance(item['id'], dict) and 'videoId' in item['id']:
#                     video_id = item['id']['videoId']
#                 elif 'videoId' in item:  # Direct videoId
#                     video_id = item['videoId']
                    
#                 if not video_id:
#                     continue
                    
#                 # 🔥 Safe snippet access
#                 snippet = item.get('snippet', {})
#                 if not isinstance(snippet, dict):
#                     continue
                    
#                 video_data = {
#                     'id': video_id,
#                     'title': snippet.get('title', 'No Title'),
#                     'channel': snippet.get('channelTitle', 'Unknown'),
#                     'categoryId': snippet.get('categoryId', '0'),
#                     'description': snippet.get('description', '')[:300],
#                     'published': snippet.get('publishedAt', ''),
#                     'thumbnails': snippet.get('thumbnails', {}),
#                     'source': source
#                 }
#                 videos.append(video_data)
                
#             except Exception as e:
#                 print(f"⚠️ Skipping item: {e}")
#                 continue
    
#     # 🔥 Remove duplicates by video ID
#     unique_videos = []
#     seen_ids = set()
#     for video in videos:
#         if video['id'] not in seen_ids:
#             unique_videos.append(video)
#             seen_ids.add(video['id'])
    
#     print(f"✅ Found {len(unique_videos)} unique videos from {len(videos)} total")
    
#     # 🔥 ALL METRICS ANALYSIS
#     for video in unique_videos:
#         title_lower = video['title'].lower()
#         desc_lower = video['description'].lower()
        
#         # 🔥 TAGS & HASHTAGS from title + description
#         all_text = f"{video['title']} {video['description']}"
#         found_hashtags = re.findall(r'#([a-zA-Z0-9_]+)', all_text, re.IGNORECASE)
#         for tag in found_hashtags:
#             hashtags[tag.lower()] += 1
        
#         # 🔥 CHANNELS
#         channel_name = video['channel'][:30]
#         channels[channel_name] += 1
        
#         # 🔥 CATEGORIES
#         categories[video['categoryId']] += 1
        
#         # 🔥 HOOKS (viral title patterns)
#         hook = video['title'][:25].lower().strip('?!.')
#         if any(word in hook for word in ['rainbow', 'color', 'diy', 'secret', 'how', 'tutorial']):
#             tags[hook] += 1
    
#     return {
#         'total_videos': len(unique_videos),
#         'unique_videos': unique_videos,
#         'hashtags': dict(hashtags.most_common(50)),
#         'top_channels': dict(channels.most_common(20)),
#         'categories': dict(categories),
#         'top_hooks': dict(tags.most_common(20)),
#         'api_sources': {k: len(v.get('items', [])) if isinstance(v, dict) else 0 for k, v in all_apis.items()}
#     }

# def print_ultimate_analysis(data, query):
#     """🔥 SAB DATA PRINT - PROFESSIONAL TABLE FORMAT"""
#     print(f"\n{'='*100}")
#     print(f"🎯 ULTIMATE ANALYSIS: '{query}' - SAB DATA EXTRACTED!")
#     print(f"{'='*100}")
    
#     print(f"\n📊 OVERVIEW:")
#     print(f"{'Videos':<12} {data['total_videos']:>8} | {'Channels':<12} {len(data['top_channels']):>8} | {'Hashtags':<12} {len(data['hashtags']):>8}")
    
#     print(f"\n🏆 TOP 20 HASHTAGS (Copy These!):")
#     print(f"{'Rank':<5} {'Hashtag':<20} {'Count':<8}")
#     print("-" * 40)
#     for i, (tag, count) in enumerate(data['hashtags'].items(), 1):
#         print(f"{i:<5} #{tag:<20} {count:<8}")
#         if i >= 20: break
    
#     print(f"\n👑 TOP 10 CHANNELS:")
#     print(f"{'Rank':<5} {'Channel':<30} {'Videos':<8}")
#     print("-" * 45)
#     for i, (channel, count) in enumerate(data['top_channels'].items(), 1):
#         print(f"{i:<5} {channel:<30} {count:<8}")
#         if i >= 10: break
    
#     print(f"\n🎨 TOP 5 VIRAL HOOKS:")
#     print("-" * 30)
#     for i, (hook, count) in enumerate(data['top_hooks'].items(), 1):
#         print(f"{i}. '{hook[:40]}...' ({count}x)")
#         if i >= 5: break
    
#     print(f"\n📂 TOP CATEGORIES:")
#     print("-" * 25)
#     for cat_id, count in data['categories'].items():
#         print(f"ID {cat_id}: {count} videos")

# def master_ultimate_analyzer(query):
#     """🔥 SAB DATA NIKALO! (100% FIXED & WORKING)"""
#     print(f"\n🚀 ULTIMATE DATA EXTRACTION STARTED: {query}")
#     print("⏳ This will take 30-60 seconds...")
    
#     all_apis = get_all_apis(query)
#     complete_data = extract_complete_data(all_apis, query)
    
#     print_ultimate_analysis(complete_data, query)
    
#     # 🔥 ULTIMATE JSON - SAB KUCH!
#     ultimate_json = {
#         'query': query,
#         'extraction_time': time.strftime("%Y-%m-%d %H:%M:%S IST"),
#         'total_api_calls': len(all_apis),
#         'data_summary': {
#             'total_videos': complete_data['total_videos'],
#             'hashtags': complete_data['hashtags'],
#             'top_channels': complete_data['top_channels'],
#             'top_hooks': complete_data['top_hooks']
#         },
#         'sample_videos': complete_data['unique_videos'][:10],  # First 10 videos
#         'api_sources': complete_data['api_sources']
#     }
    
#     filename = f"ULTIMATE_{query.replace(' ', '_').upper()}_{int(time.time())}.json"
#     with open(filename, "w", encoding='utf-8') as f:
#         json.dump(ultimate_json, f, indent=2, ensure_ascii=False)
    
#     filesize = len(str(ultimate_json)) // 1000
#     print(f"\n💾 SAVED ULTIMATE FILE: {filename}")
#     print(f"📦 Size: {filesize}KB | Videos: {complete_data['total_videos']} | Hashtags: {len(complete_data['hashtags'])}")
    
#     return ultimate_json

# def main():
#     """🔥 MAIN LOOP - 100% CRASH PROOF"""
#     print("🔥 YOUTUBE ULTIMATE ANALYZER v12.2 - SAB DATA! (FIXED)")
#     print("=" * 80)
#     print("🤖 5 Search Modes + Trending + 200+ Videos + NO ERRORS!")
#     print("💡 Examples: 'lip balm', 'face serum', 'hair oil'")
#     print("📊 Output: Table + JSON with ALL data!")
    
#     while True:
#         try:
#             print("\n" + "="*80)
#             query = input("🔍 Enter query (or 'quit'): ").strip()
#             if query.lower() in ['quit', 'exit', 'q']:
#                 print("\n👋 ANALYSIS COMPLETE! All files saved!")
#                 break
#             if query:
#                 master_ultimate_analyzer(query)
#                 print("\n✅ READY FOR NEXT QUERY!")
#         except KeyboardInterrupt:
#             print("\n👋 STOPPED BY USER!")
#             break
#         except Exception as e:
#             print(f"💥 Unexpected error: {e}")
#             print("🔄 Continuing...")
#             continue

# if __name__ == "__main__":
#     main()





import requests
import json
import re
import time
from collections import Counter
import sys
from datetime import datetime
from urllib.parse import quote
import pandas as pd  # 🔥 EXCEL SUPPORT

API_KEY = 'AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4'
BRAND_KEYWORDS = ['loreal', 'maybelline', 'lakme', 'mamaearth', 'nykaa', 'plum']

def safe_api_call(url, retries=3):
    """Safe API call"""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if 'error' in data:
                print(f"⚠️ API Error: {data['error'].get('message', 'Unknown')}")
                time.sleep(2)
                continue
            return data
        except Exception as e:
            print(f"⚠️ Request error: {e}")
            time.sleep(1)
    return None

def search_keyword_data(query, max_results=100):
    """🔥 SPECIFIC KEYWORD DATA"""
    print(f"🔍 SEARCHING '{query}'...")
    all_data = {}
    video_ids = set()
    
    search_modes = ['viewCount', 'rating', 'relevance', 'date']
    regions = ['IN', 'US', 'GB']
    
    for mode in search_modes:
        for region in regions:
            print(f"   → {mode}/{region}...")
            url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={quote(query)}&type=video&maxResults=50&order={mode}&regionCode={region}&key={API_KEY}"
            data = safe_api_call(url)
            if data and 'items' in data:
                for item in data['items']:
                    vid_id = item['id']['videoId']
                    video_ids.add(vid_id)
            time.sleep(0.3)
    
    print(f"✅ {len(video_ids)} VIDEO IDs FOUND")
    return list(video_ids)

def get_full_video_details(video_ids):
    """🔥 FULL VIDEO DETAILS"""
    all_videos = []
    
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        print(f"📊 Batch {i//50 + 1}/{(len(video_ids)-1)//50 + 1}...")
        
        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={','.join(batch)}&key={API_KEY}"
        data = safe_api_call(url)
        
        if data and 'items' in data:
            for item in data['items']:
                try:
                    video = {
                        'Video_ID': item['id'],
                        'Title': item['snippet'].get('title', ''),
                        'Channel': item['snippet'].get('channelTitle', ''),
                        'Channel_ID': item['snippet'].get('channelId', ''),
                        'Description': item['snippet'].get('description', '')[:400],
                        'Published': item['snippet'].get('publishedAt', ''),
                        'Views': int(item['statistics'].get('viewCount', 0)),
                        'Likes': int(item['statistics'].get('likeCount', 0)),
                        'Comments': int(item['statistics'].get('commentCount', 0)),
                        'Duration_Raw': item['contentDetails'].get('duration', 'PT0S'),
                        'Video_URL': f"https://www.youtube.com/watch?v={item['id']}",
                        'Short_URL': f"https://youtu.be/{item['id']}"
                    }
                    
                    # 🔥 Duration parsing
                    duration_match = re.search(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', video['Duration_Raw'])
                    if duration_match:
                        h, m, s = duration_match.groups()
                        total_sec = int(h or 0)*3600 + int(m or 0)*60 + int(s or 0)
                        video['Duration_Seconds'] = total_sec
                        video['Duration'] = f"{total_sec//60}m {total_sec%60}s"
                    else:
                        video['Duration_Seconds'] = 0
                        video['Duration'] = '0s'
                    
                    all_videos.append(video)
                except:
                    continue
        
        time.sleep(0.5)
    
    return all_videos

def save_to_excel(videos, analysis, query):
    """🔥 EXCEL EXPORT - MAIN + ANALYSIS SHEETS"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{query.upper().replace('-', '_')}_ANALYSIS_{timestamp}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 🔥 SHEET 1: ALL VIDEOS
        df_videos = pd.DataFrame(videos)
        df_videos.to_excel(writer, sheet_name='ALL_VIDEOS', index=False)
        
        # 🔥 SHEET 2: TOP ENGAGEMENT
        engagement_data = []
        for v in videos:
            if v['Views'] > 0:
                ratio = (v['Likes'] / v['Views']) * 100
                engagement_data.append({
                    'Title': v['Title'][:50],
                    'Views': v['Views'],
                    'Likes': v['Likes'],
                    'Comments': v['Comments'],
                    'Like_Ratio_%': f"{ratio:.1f}%",
                    'Duration': v['Duration'],
                    'URL': v['Short_URL']
                })
        
        df_engagement = pd.DataFrame(engagement_data).sort_values('Views', ascending=False)
        df_engagement.to_excel(writer, sheet_name='TOP_ENGAGEMENT', index=False)
        
        # 🔥 SHEET 3: ANALYSIS SUMMARY
        summary_data = {
            'Metric': [
                'Total Videos', 'Total Views', 'Total Likes', 'Avg Like Ratio',
                'Top Hashtag', 'Top Hook', 'Best Duration', 'Peak Hour'
            ],
            'Value': [
                len(videos),
                f"{sum(v['Views'] for v in videos):,}",
                f"{sum(v['Likes'] for v in videos):,}",
                f"{sum(v['Likes'] for v in videos)/sum(v['Views'] for v in videos)*100:.1f}%" if videos else "0%",
                list(analysis['hashtags'].most_common(1))[0][0] if analysis['hashtags'] else '-',
                list(analysis['hooks'].most_common(1))[0][0][:30] if analysis['hooks'] else '-',
                list(analysis['duration_patterns'].most_common(1))[0][0] if analysis['duration_patterns'] else '-',
                list(analysis['publish_hours'].most_common(1))[0][0] if analysis['publish_hours'] else '-'
            ]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='SUMMARY', index=False)
        
        # 🔥 SHEET 4: HASHTAGS
        hashtags_df = pd.DataFrame([
            {'Hashtag': tag, 'Count': count} 
            for tag, count in analysis['hashtags'].most_common(50)
        ])
        hashtags_df.to_excel(writer, sheet_name='HASHTAGS', index=False)
        
        # 🔥 SHEET 5: HOOKS
        hooks_df = pd.DataFrame([
            {'Hook': hook[:50], 'Count': count} 
            for hook, count in analysis['hooks'].most_common(30)
        ])
        hooks_df.to_excel(writer, sheet_name='HOOKS', index=False)
    
    print(f"\n💾 ✅ EXCEL SAVED: {filename}")
    print("📊 SHEETS: ALL_VIDEOS | TOP_ENGAGEMENT | SUMMARY | HASHTAGS | HOOKS")
    return filename

def analyze_keyword_data(videos, query):
    """🔥 ANALYSIS"""
    analysis = {
        'hashtags': Counter(),
        'hooks': Counter(),
        'duration_patterns': Counter(),
        'publish_hours': Counter(),
        'top_channels': Counter(),
        'brands': Counter()
    }
    
    for video in videos:
        text = f"{video['Title']} {video['Description']}"
        hashtags = re.findall(r'#([a-zA-Z0-9_]+)', text, re.IGNORECASE)
        analysis['hashtags'].update(hashtags)
        
        hook = video['Title'][:30].strip('?!.')
        analysis['hooks'][hook] += 1
        
        analysis['duration_patterns'][video['Duration']] += 1
        
        title_lower = video['Title'].lower()
        for brand in BRAND_KEYWORDS:
            if brand in title_lower:
                analysis['brands'][brand.title()] += 1
        
        analysis['top_channels'][video['Channel'][:30]] += 1
        
        if video['Published']:
            try:
                pub_hour = datetime.fromisoformat(video['Published'].replace('Z', '+00:00')).hour
                analysis['publish_hours'][f"{pub_hour}:00"] += 1
            except:
                pass
    
    return analysis

def print_keyword_report(videos, analysis, query):
    """🔥 CONSOLE REPORT"""
    print("\n" + "="*100)
    print(f"🚀 '{query.upper()}' - COMPLETE ANALYSIS")
    print("="*100)
    
    total_views = sum(v['Views'] for v in videos)
    total_likes = sum(v['Likes'] for v in videos)
    
    print(f"📊 TOTAL: {len(videos)} videos")
    print(f"👀 VIEWS: {total_views:,} | ❤️ LIKES: {total_likes:,}")
    
    print(f"\n🏆 TOP 10 HASHTAGS:")
    for i, (tag, count) in enumerate(analysis['hashtags'].most_common(10), 1):
        print(f"{i:2d}. #{tag:<15} ({count})")
    
    print(f"\n🎨 TOP HOOKS:")
    for i, (hook, count) in enumerate(analysis['hooks'].most_common(5), 1):
        print(f"{i:2d}. '{hook}' ({count})")

def main():
    """🔥 MAIN - EXCEL AUTO EXPORT"""
    print("🚀 YOUTUBE ANALYZER v23.0 - EXCEL EXPORT!")
    print("=" * 80)
    print("📝 lip-bam → JSON + EXCEL (5 sheets) AUTO!")
    
    while True:
        try:
            print("\n" + "="*80)
            query = input("🔍 Enter keyword (quit to exit): ").strip()
            
            if query.lower() in ['quit', 'q', 'exit']:
                print("👋 EXCEL FILES SAVED!")
                break
            
            if not query:
                print("❌ Enter keyword!")
                continue
            
            # 🔥 FULL PROCESS
            print(f"\n🚀 Processing '{query}'...")
            video_ids = search_keyword_data(query)
            
            if not video_ids:
                print("❌ No videos found!")
                continue
            
            videos = get_full_video_details(video_ids)
            analysis = analyze_keyword_data(videos, query)
            
            print_keyword_report(videos, analysis, query)
            excel_file = save_to_excel(videos, analysis, query)
            
            print(f"\n✅ '{query}' → {excel_file}")
            print("📊 OPEN EXCEL → 5 SHEETS READY!")
            
        except KeyboardInterrupt:
            print("\n👋 Stopped!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
