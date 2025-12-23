# import requests
# import json
# import re
# import time
# from collections import Counter

# # Your working API key
# API_KEY = 'AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4'

# def safe_api_call(url, retries=3):
#     """🔥 Safe API call with retry"""
#     for attempt in range(retries):
#         try:
#             response = requests.get(url)
#             data = response.json()
#             if 'error' in data:
#                 print(f"❌ API ERROR: {data['error'].get('message', 'Unknown')}")
#                 if attempt < retries - 1:
#                     time.sleep(1)
#                     continue
#                 return None
#             return data
#         except Exception as e:
#             print(f"💥 Error: {e}")
#             if attempt < retries - 1:
#                 time.sleep(1)
#                 continue
#     return None

# def get_video_keywords(video_id):
#     """🔥 Extract tags + title keywords from video"""
#     url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
#     data = safe_api_call(url)
    
#     if data and data['items']:
#         video = data['items'][0]
#         tags = video['snippet'].get('tags', [])
#         title = video['snippet']['title']
        
#         # Extract keywords from title
#         title_words = re.findall(r'\b[a-zA-Z]{3,15}\b', title.lower())
#         title_keywords = [w for w in title_words if w not in ['for', 'the', 'with', 'learn', 'free', 'full']]
        
#         print(f"📺 Video: {title[:60]}...")
#         print(f"🏷️  TAGS ({len(tags)}): {', '.join(tags[:8])}")
#         print(f"📝 TITLE KW ({len(title_keywords)}): {', '.join(title_keywords[:8])}")
        
#         return list(set(tags + title_keywords))
#     return []

# def get_search_keywords(query, max_results=15):
#     """🔥 Extract keywords from search results"""
#     url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&key={API_KEY}"
#     data = safe_api_call(url)
    
#     keywords = []
#     for item in data.get('items', []):
#         title = item['snippet']['title']
#         # Extract meaningful words
#         words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
#         keywords.extend([w for w in words if len(w) > 3 and w not in ['with', 'from', 'your', 'this']])
    
#     return list(set(keywords))

# def get_channel_keywords(channel_id):
#     """🔥 Extract channel keywords"""
#     url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
#     data = safe_api_call(url)
    
#     if data and data['items']:
#         channel = data['items'][0]
#         keywords = channel['snippet'].get('keywords', [])
#         print(f"👤 CHANNEL: {channel['snippet']['title']}")
#         print(f"🏷️  CHANNEL KW: {', '.join(keywords[:6])}")
#         return keywords
#     return []

# def master_keywords_extractor(query="Python tutorial", video_id=None, channel_id=None):
#     """🔥 MASTER FUNCTION - ALL KEYWORDS COMBINED"""
#     print(f"\n🎯 KEYWORDS EXTRACTION FOR: '{query}'")
#     print("=" * 80)
    
#     all_keywords = set()
    
#     # 1. VIDEO KEYWORDS (if provided)
#     if video_id:
#         video_kws = get_video_keywords(video_id)
#         all_keywords.update(video_kws)
    
#     # 2. SEARCH RESULT KEYWORDS
#     search_kws = get_search_keywords(query)
#     all_keywords.update(search_kws)
    
#     # 3. CHANNEL KEYWORDS (if provided)
#     if channel_id:
#         channel_kws = get_channel_keywords(channel_id)
#         all_keywords.update(channel_kws)
    
#     # 4. Query-based keywords
#     query_words = re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())
#     all_keywords.update(query_words)
    
#     # ANALYSIS
#     print(f"\n📊 KEYWORD ANALYSIS:")
#     print(f"🔥 Total unique keywords: {len(all_keywords)}")
    
#     # Categorize keywords
#     high_volume = [kw for kw in all_keywords if len(kw) > 6]
#     long_tail = [kw for kw in all_keywords if ' ' in kw]
#     brands = [kw for kw in all_keywords if kw[0].isupper() and len(kw) > 3]
    
#     print(f"📈 High Volume (>6 chars): {len(high_volume)}")
#     print(f"📏 Long Tail: {len(long_tail)}")
#     print(f"🏪 Brands: {len(brands)}")
    
#     # TOP 25 KEYWORDS (sorted by length + alphabetically)
#     top_keywords = sorted(list(all_keywords), key=lambda x: (-len(x), x))[:25]
    
#     print(f"\n🏆 TOP 25 KEYWORDS:")
#     print("-" * 40)
#     for i, keyword in enumerate(top_keywords, 1):
#         length_score = len(keyword)
#         print(f"{i:2d}. {keyword:<20} | Length: {length_score}")
    
#     # RECOMMENDATIONS
#     print(f"\n💡 RECOMMENDATIONS:")
#     print(f"• Primary: '{top_keywords[0]} {query}'")
#     print(f"• Long Tail: '{top_keywords[1]} {top_keywords[2]}'")
#     print(f"• Brand Combo: {' + '.join(brands[:3])}")
    
#     return {
#         'all_keywords': list(all_keywords),
#         'top_keywords': top_keywords,
#         'high_volume': high_volume,
#         'brands': brands,
#         'search_volume_keywords': search_kws
#     }

# def keyword_frequency_analysis(keywords):
#     """🔥 Analyze keyword frequency across multiple videos/searches"""
#     word_count = Counter()
#     for kw in keywords:
#         word_count[kw] += 1
    
#     print("\n📊 FREQUENCY ANALYSIS:")
#     most_common = word_count.most_common(15)
#     for word, count in most_common:
#         print(f"{word:<15} → {count} occurrences")

# # 🔥 MAIN EXECUTION
# if __name__ == "__main__":
#     print("🔥 YOUTUBE KEYWORDS EXTRACTOR v2.0")
#     print("=" * 60)
    
#     # Test cases for different scenarios
#     test_cases = [
#         ("Face serum", None, None),
#         # ("Python tutorial", None, "UC_x5XG1OV2P6uZZ5FSM9Ttw"),
#         # ("body lotion", "dQw4w9WgXcQ", None),  # Rick Roll video for demo
#     ]
    
#     for query, video_id, channel_id in test_cases:
#         print(f"\n{'='*80}")
#         results = master_keywords_extractor(query, video_id, channel_id)
        
#         # Save to JSON
#         with open(f"keywords_{query.replace(' ', '_')}.json", "w") as f:
#             json.dump(results, f, indent=2)
#         print(f"\n💾 Saved to: keywords_{query.replace(' ', '_')}.json")
    
#     print("\n" + "="*80)
#     print("✅ KEYWORDS EXTRACTION COMPLETE!")
#     print("✅ 3 JSON files generated")
#     print("✅ Ready for SEO/Marketing use!")




# import requests
# import json
# import re
# import time
# from collections import Counter
# import sys

# # Your working API key
# API_KEY = 'AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4'

# def safe_api_call(url, retries=3):
#     """🔥 Safe API call with retry"""
#     for attempt in range(retries):
#         try:
#             response = requests.get(url)
#             data = response.json()
#             if 'error' in data:
#                 print(f"❌ API ERROR: {data['error'].get('message', 'Unknown')}")
#                 if attempt < retries - 1:
#                     time.sleep(1)
#                     continue
#                 return None
#             return data
#         except Exception as e:
#             print(f"💥 Error: {e}")
#             if attempt < retries - 1:
#                 time.sleep(1)
#                 continue
#     return None

# def get_video_keywords(video_id):
#     """🔥 Extract tags + title keywords from video"""
#     url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
#     data = safe_api_call(url)
    
#     if data and data['items']:
#         video = data['items'][0]
#         tags = video['snippet'].get('tags', [])
#         title = video['snippet']['title']
        
#         title_words = re.findall(r'\b[a-zA-Z]{3,15}\b', title.lower())
#         title_keywords = [w for w in title_words if w not in ['for', 'the', 'with', 'learn', 'free', 'full']]
        
#         print(f"📺 Video: {title[:60]}...")
#         print(f"🏷️  TAGS ({len(tags)}): {', '.join(tags[:8])}")
#         print(f"📝 TITLE KW ({len(title_keywords)}): {', '.join(title_keywords[:8])}")
        
#         return list(set(tags + title_keywords))
#     return []

# def get_search_keywords(query, max_results=15):
#     """🔥 Extract keywords from search results"""
#     url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&key={API_KEY}"
#     data = safe_api_call(url)
    
#     keywords = []
#     for item in data.get('items', []):
#         title = item['snippet']['title']
#         words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
#         keywords.extend([w for w in words if len(w) > 3 and w not in ['with', 'from', 'your', 'this']])
    
#     return list(set(keywords))

# def get_channel_keywords(channel_id):
#     """🔥 Extract channel keywords"""
#     url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
#     data = safe_api_call(url)
    
#     if data and data['items']:
#         channel = data['items'][0]
#         keywords = channel['snippet'].get('keywords', [])
#         print(f"👤 CHANNEL: {channel['snippet']['title']}")
#         print(f"🏷️  CHANNEL KW: {', '.join(keywords[:6])}")
#         return keywords
#     return []

# def master_keywords_extractor(query, video_id=None, channel_id=None):
#     """🔥 MASTER FUNCTION - ALL KEYWORDS COMBINED"""
#     print(f"\n🎯 KEYWORDS EXTRACTION FOR: '{query}'")
#     print("=" * 80)
    
#     all_keywords = set()
    
#     if video_id:
#         video_kws = get_video_keywords(video_id)
#         all_keywords.update(video_kws)
    
#     search_kws = get_search_keywords(query)
#     all_keywords.update(search_kws)
    
#     if channel_id:
#         channel_kws = get_channel_keywords(channel_id)
#         all_keywords.update(channel_kws)
    
#     query_words = re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())
#     all_keywords.update(query_words)
    
#     # ANALYSIS
#     print(f"\n📊 KEYWORD ANALYSIS:")
#     print(f"🔥 Total unique keywords: {len(all_keywords)}")
    
#     high_volume = [kw for kw in all_keywords if len(kw) > 6]
#     long_tail = [kw for kw in all_keywords if ' ' in kw]
#     brands = [kw for kw in all_keywords if kw[0].isupper() and len(kw) > 3]
    
#     print(f"📈 High Volume (>6 chars): {len(high_volume)}")
#     print(f"📏 Long Tail: {len(long_tail)}")
#     print(f"🏪 Brands: {len(brands)}")
    
#     top_keywords = sorted(list(all_keywords), key=lambda x: (-len(x), x))[:25]
    
#     print(f"\n🏆 TOP 25 KEYWORDS:")
#     print("-" * 40)
#     for i, keyword in enumerate(top_keywords, 1):
#         length_score = len(keyword)
#         print(f"{i:2d}. {keyword:<20} | Length: {length_score}")
    
#     print(f"\n💡 RECOMMENDATIONS:")
#     print(f"• Primary: '{top_keywords[0]} {query}'")
#     print(f"• Long Tail: '{top_keywords[1]} {top_keywords[2]}'")
#     print(f"• Brand Combo: {' + '.join(brands[:3])}")
    
#     # Save JSON
#     results = {
#         'query': query,
#         'all_keywords': list(all_keywords),
#         'top_keywords': top_keywords,
#         'high_volume': high_volume,
#         'brands': brands
#     }
#     filename = f"keywords_{query.replace(' ', '_')}_{int(time.time())}.json"
#     with open(filename, "w") as f:
#         json.dump(results, f, indent=2)
#     print(f"\n💾 Saved: {filename}")
    
#     return results

# # 🔥 TERMINAL INTERACTIVE MODE
# def main():
#     print("🔥 YOUTUBE KEYWORDS EXTRACTOR v3.0 - TERMINAL MODE")
#     print("=" * 60)
#     print("📝 Type your search query (or 'quit' to exit)")
#     print("💡 Example: 'hair serum', 'face cream', 'Python tutorial'")
#     print("-" * 60)
    
#     while True:
#         try:
#             # Get input from terminal
#             query = input("\n🔍 Enter search keyword: ").strip()
            
#             if query.lower() in ['quit', 'exit', 'q']:
#                 print("\n👋 Goodbye!")
#                 break
            
#             if not query:
#                 print("❌ Please enter a valid query!")
#                 continue
            
#             # Extract video/channel ID if provided
#             video_id = None
#             channel_id = None
            
#             # Check if query contains YouTube URL
#             if 'youtube.com/watch?v=' in query or 'youtu.be/' in query:
#                 video_match = re.search(r'(?:v=|youtu\.be/)([^&\n?#]+)', query)
#                 if video_match:
#                     video_id = video_match.group(1)
#                     query = query.split(' ')[0].replace('youtube.com/watch?v=', '').replace('youtu.be/', '')
            
#             if 'channel/' in query:
#                 channel_match = re.search(r'channel/([a-zA-9_-]+)', query)
#                 if channel_match:
#                     channel_id = channel_match.group(1)
            
#             # Run extraction
#             print()
#             results = master_keywords_extractor(query, video_id, channel_id)
            
#             print("\n" + "="*80)
#             print("✅ Search complete! Type next keyword or 'quit'")
            
#         except KeyboardInterrupt:
#             print("\n\n👋 Interrupted by user. Goodbye!")
#             break
#         except Exception as e:
#             print(f"💥 Error: {e}")
#             continue

# if __name__ == "__main__":
#     main()





# import requests
# import json
# import re
# import time
# from collections import Counter
# import sys

# # Your working API key
# API_KEY = 'AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4'

# # 🔥 LOCATION CONFIG (Kanpur/UP + Top Indian Cities)
# CITIES = ['kanpur', 'lucknow', 'delhi', 'mumbai', 'noida', 'agra', 'pune', 'bangalore', 
#           'chennai', 'hyderabad', 'kolkata', 'jaipur', 'up', 'uttar', 'india']

# COMMON_STOPWORDS = ['for', 'the', 'with', 'learn', 'free', 'full', 'best', 'top', 'review']

# def safe_api_call(url, retries=3):
#     """🔥 Safe API call with retry"""
#     for attempt in range(retries):
#         try:
#             response = requests.get(url)
#             data = response.json()
#             if 'error' in data:
#                 print(f"❌ API ERROR: {data['error'].get('message', 'Unknown')}")
#                 if attempt < retries - 1:
#                     time.sleep(1)
#                     continue
#                 return None
#             return data
#         except Exception as e:
#             print(f"💥 Error: {e}")
#             if attempt < retries - 1:
#                 time.sleep(1)
#                 continue
#     return None

# def get_video_keywords(video_id):
#     """🔥 Extract tags + title keywords from video"""
#     url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
#     data = safe_api_call(url)
    
#     if data and data['items']:
#         video = data['items'][0]
#         tags = video['snippet'].get('tags', [])
#         title = video['snippet']['title']
        
#         title_words = re.findall(r'\b[a-zA-Z]{3,15}\b', title.lower())
#         title_keywords = [w for w in title_words if w not in COMMON_STOPWORDS]
        
#         print(f"📺 Video: {title[:60]}...")
#         print(f"🏷️  TAGS ({len(tags)}): {', '.join(tags[:8])}")
#         print(f"📝 TITLE KW ({len(title_keywords)}): {', '.join(title_keywords[:8])}")
        
#         return list(set(tags + title_keywords))
#     return []

# def get_search_keywords_with_location(query, max_results=20):
#     """🔥 Extract keywords + LOCATION data from top search results"""
#     # Get TOP videos by viewCount for demand analysis
#     url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&order=viewCount&key={API_KEY}"
#     data = safe_api_call(url)
    
#     keywords = []
#     locations = Counter()
#     search_time = time.strftime("%Y-%m-%d %H:%M:%S IST")
    
#     for item in data.get('items', [])[:15]:
#         title = item['snippet']['title'].lower()
#         channel_title = item['snippet']['channelTitle'].lower()
        
#         # Extract keywords from title
#         words = re.findall(r'\b[a-zA-Z]{4,}\b', title)
#         for w in words:
#             if w not in COMMON_STOPWORDS and len(w) > 3:
#                 keywords.append(w)
        
#         # 🔥 LOCATION EXTRACTION (cities from title + channel)
#         content = title + ' ' + channel_title
#         for city in CITIES:
#             if city in content:
#                 locations[city] += 1
    
#     print(f"🕒 Search Time: {search_time}")
#     print(f"📍 Top Locations: {dict(locations.most_common(5))}")
    
#     return list(set(keywords)), locations, search_time

# def extract_city_demand(all_keywords, locations):
#     """🔥 Rank cities by demand (frequency in top videos)"""
#     city_demand = []
#     for city, count in locations.items():
#         if count > 0:
#             city_demand.append({'city': city.title(), 'demand_score': count, 'mentions': count})
#     return sorted(city_demand, key=lambda x: x['demand_score'], reverse=True)[:10]

# def get_channel_keywords(channel_id):
#     """🔥 Extract channel keywords"""
#     url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
#     data = safe_api_call(url)
    
#     if data and data['items']:
#         channel = data['items'][0]
#         keywords = channel['snippet'].get('keywords', [])
#         print(f"👤 CHANNEL: {channel['snippet']['title']}")
#         print(f"🏷️  CHANNEL KW: {', '.join(keywords[:6])}")
#         return keywords
#     return []

# def master_keywords_extractor(query, video_id=None, channel_id=None):
#     """🔥 MASTER FUNCTION - KEYWORDS + CITY DEMAND + LOCATION DATA"""
#     print(f"\n🎯 KEYWORDS EXTRACTION FOR: '{query}'")
#     print("=" * 80)
    
#     all_keywords = set()
#     locations = Counter()
#     search_time = ""
    
#     # 1. VIDEO KEYWORDS (if provided)
#     if video_id:
#         video_kws = get_video_keywords(video_id)
#         all_keywords.update(video_kws)
    
#     # 2. SEARCH + LOCATION ANALYSIS
#     search_kws, locations, search_time = get_search_keywords_with_location(query)
#     all_keywords.update(search_kws)
    
#     # 3. CHANNEL KEYWORDS (if provided)
#     if channel_id:
#         channel_kws = get_channel_keywords(channel_id)
#         all_keywords.update(channel_kws)
    
#     # 4. Query-based keywords
#     query_words = re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())
#     all_keywords.update(query_words)
    
#     # 🔥 CITY DEMAND RANKING
#     top_cities = extract_city_demand(list(all_keywords), locations)
    
#     # ANALYSIS
#     print(f"\n📊 KEYWORD ANALYSIS:")
#     print(f"🔥 Total unique keywords: {len(all_keywords)}")
    
#     high_volume = [kw for kw in all_keywords if len(kw) > 6]
#     brands = [kw for kw in all_keywords if kw[0].isupper() and len(kw) > 3]
    
#     print(f"📈 High Volume (>6 chars): {len(high_volume)}")
#     print(f"🏪 Brands: {len(brands)}")
    
#     # 🔥 TOP 10 CITY DEMAND
#     print(f"\n🏙️  TOP 10 CITIES IN DEMAND:")
#     print("-" * 40)
#     for i, city_data in enumerate(top_cities, 1):
#         print(f"{i:2d}. {city_data['city']:<12} | Score: {city_data['demand_score']}")
    
#     # TOP 25 KEYWORDS
#     top_keywords = sorted(list(all_keywords), key=lambda x: (-len(x), x))[:25]
    
#     print(f"\n🏆 TOP 25 KEYWORDS:")
#     print("-" * 40)
#     for i, keyword in enumerate(top_keywords, 1):
#         print(f"{i:2d}. {keyword:<20} | Length: {len(keyword)}")
    
#     # RECOMMENDATIONS
#     print(f"\n💡 LOCATION-BASED RECOMMENDATIONS:")
#     if top_cities:
#         print(f"• Target City: '{top_cities[0]['city']} {query}'")
#         print(f"• Top 3 Cities: {', '.join([c['city'] for c in top_cities[:3]])}")
#     print(f"• Brand + City: '{brands[0] if brands else 'Brand'} {top_cities[0]['city'] if top_cities else 'City'}'")
    
#     # Enhanced JSON with LOCATION DATA
#     results = {
#         'query': query,
#         'search_time': search_time,
#         'total_keywords': len(all_keywords),
#         'top_cities_demand': top_cities,
#         'location_mentions': dict(locations),
#         'all_keywords': list(all_keywords),
#         'top_keywords': top_keywords,
#         'brands': brands,
#         'high_volume': high_volume
#     }
    
#     filename = f"keywords_{query.replace(' ', '_')}_{int(time.time())}.json"
#     with open(filename, "w") as f:
#         json.dump(results, f, indent=2)
#     print(f"\n💾 Saved: {filename}")
    
#     return results

# # 🔥 TERMINAL INTERACTIVE MODE
# def main():
#     print("🔥 YOUTUBE KEYWORDS EXTRACTOR v4.0 - CITY DEMAND ANALYZER")
#     print("=" * 70)
#     print("📍 Auto-detects TOP 10 cities + search time + location demand")
#     print("💡 Example: 'top ten city moisturiser', 'kanpur face cream'")
#     print("-" * 70)
    
#     while True:
#         try:
#             query = input("\n🔍 Enter search keyword: ").strip()
            
#             if query.lower() in ['quit', 'exit', 'q']:
#                 print("\n👋 Goodbye!")
#                 break
            
#             if not query:
#                 print("❌ Please enter a valid query!")
#                 continue
            
#             # Auto-detect video/channel IDs
#             video_id = None
#             channel_id = None
            
#             if 'youtube.com/watch?v=' in query or 'youtu.be/' in query:
#                 video_match = re.search(r'(?:v=|youtu\.be/)([^&\n?#]+)', query)
#                 if video_match:
#                     video_id = video_match.group(1)
            
#             if 'channel/' in query:
#                 channel_match = re.search(r'channel/([a-zA-9_-]+)', query)
#                 if channel_match:
#                     channel_id = channel_match.group(1)
            
#             print()
#             results = master_keywords_extractor(query, video_id, channel_id)
            
#             print("\n" + "="*80)
#             print("✅ Analysis complete! Next query or 'quit'")
            
#         except KeyboardInterrupt:
#             print("\n\n👋 Interrupted. Goodbye!")
#             break
#         except Exception as e:
#             print(f"💥 Error: {e}")
#             continue

# if __name__ == "__main__":
#     main()


import requests
import json
import re
import time
from collections import Counter
import sys


# Your working API key
API_KEY = 'AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4'


# 🔥 CONFIG - LOCATION WISE SEARCH ✅
CITIES = {
    'kanpur': 'IN', 'lucknow': 'IN', 'delhi': 'IN', 'mumbai': 'IN', 
    'noida': 'IN', 'agra': 'IN', 'pune': 'IN', 'bangalore': 'IN',
    'chennai': 'IN', 'hyderabad': 'IN', 'kolkata': 'IN', 'jaipur': 'IN',
    'up': 'IN', 'uttar': 'IN', 'india': 'IN'
}

COMMON_STOPWORDS = ['for', 'the', 'with', 'learn', 'free', 'full', 'best', 'top', 'review']
CATEGORIES = ['beauty', 'skincare', 'moisturizer', 'serum', 'tutorial', 'review', 'music', 'dance']


def safe_api_call(url, retries=3):
    """🔥 Safe API call with retry"""
    for attempt in range(retries):
        try:
            response = requests.get(url)
            data = response.json()
            if 'error' in data:
                print(f"❌ API ERROR: {data['error'].get('message', 'Unknown')}")
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                return None
            return data
        except Exception as e:
            print(f"💥 Error: {e}")
            if attempt < retries - 1:
                time.sleep(1)
                continue
    return None


def get_video_details(video_id):
    """🔥 Get full video details (tags, duration, category, stats)"""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_id}&key={API_KEY}"
    data = safe_api_call(url)
    
    if data and data['items']:
        video = data['items'][0]
        snippet = video['snippet']
        stats = video.get('statistics', {})
        content = video['contentDetails']
        
        # Duration parsing
        duration = content['duration']
        duration_secs = parse_duration(duration)
        
        # Category
        category_id = snippet.get('categoryId', '0')
        category_name = get_category_name(category_id)
        
        return {
            'title': snippet['title'],
            'tags': snippet.get('tags', []),
            'category': category_name,
            'duration_secs': duration_secs,
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0)),
            'engagement': int(stats.get('likeCount', 0)) + int(stats.get('commentCount', 0)),
            'channel': snippet['channelTitle']
        }
    return None


def parse_duration(duration_str):
    """Convert ISO 8601 duration to seconds"""
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration_str)
    if match:
        hours, minutes, seconds = match.groups()
        return (int(hours or 0) * 3600 + 
                int(minutes or 0) * 60 + 
                int(seconds or 0))
    return 0


def get_category_name(cat_id):
    """Map category ID to name"""
    categories = {
        '10': 'Music', '2': 'Autos', '1': 'Film', '22': 'People', '26': 'Howto',
        '24': 'Entertainment', '20': 'Gaming', '15': 'Pets', '28': 'Science',
        '25': 'News', '17': 'Sports', '19': 'Travel', '23': 'Comedy'
    }
    return categories.get(cat_id, 'Other')


def get_search_results_with_stats(query, max_results=20, region='IN'):  # 🔥 LOCATION ADDED
    """🔥 Get top videos with full stats - LOCATION SPECIFIC ✅"""
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&order=viewCount&regionCode={region}&key={API_KEY}"  # 🔥 regionCode ADDED
    data = safe_api_call(url)
    
    video_ids = [item['id']['videoId'] for item in data.get('items', [])[:15]]
    videos_data = []
    
    # Get detailed stats for top videos
    if video_ids:
        details_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={','.join(video_ids)}&key={API_KEY}"
        details = safe_api_call(details_url)
        
        for item in details.get('items', []):
            snippet = item['snippet']
            stats = item.get('statistics', {})
            content = item['contentDetails']
            
            duration = parse_duration(content['duration'])
            videos_data.append({
                'title': snippet['title'],
                'tags': snippet.get('tags', []),
                'category': get_category_name(snippet.get('categoryId', '0')),
                'duration': duration,
                'duration_secs': duration,
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0)),
                'engagement': int(stats.get('likeCount', 0)) + int(stats.get('commentCount', 0))
            })
    return videos_data


def analyze_trends(videos_data):
    """🔥 Analyze all 13 metrics"""
    results = {
        'tags': Counter(),
        'hooks': Counter(),
        'category_stats': Counter(),
        'duration_stats': Counter(),
        'engagement_by_category': {},
        'music_category': [],
        'top_performers': {
            'highest_views': None,
            'highest_engagement': None
        }
    }
    
    total_views = 0
    total_likes = 0
    
    for video in videos_data:
        # 5. TAGS analysis
        for tag in video['tags']:
            results['tags'][tag.lower()] += 1
        
        # 6. HOOKS (first 15 chars of title)
        hook = video['title'][:15].lower().strip('?!.')
        results['hooks'][hook] += 1
        
        # 7. Category trends
        cat = video['category']
        results['category_stats'][cat] += 1
        if cat not in results['engagement_by_category']:
            results['engagement_by_category'][cat] = {'views': 0, 'likes': 0, 'comments': 0, 'count': 0}
        results['engagement_by_category'][cat]['views'] += video['views']
        results['engagement_by_category'][cat]['likes'] += video['likes']
        results['engagement_by_category'][cat]['comments'] += video['comments']
        results['engagement_by_category'][cat]['count'] += 1
        
        # 9. Music category specific
        if cat == 'Music':
            results['music_category'].append(video)
        
        # 10. Duration analysis
        duration_bucket = get_duration_bucket(video['duration'])
        results['duration_stats'][duration_bucket] += 1
        
        # Track top performers
        if not results['top_performers']['highest_views'] or video['views'] > results['top_performers']['highest_views']['views']:
            results['top_performers']['highest_views'] = video
        if not results['top_performers']['highest_engagement'] or video['engagement'] > results['top_performers']['highest_engagement']['engagement']:
            results['top_performers']['highest_engagement'] = video
        
        total_views += video['views']
        total_likes += video['likes']
    
    results['avg_engagement'] = total_views / max(total_likes, 1)
    return results


def get_duration_bucket(seconds):
    """Categorize video length"""
    if seconds < 300: return 'Under 5min'
    elif seconds < 600: return '5-10min'
    elif seconds < 1200: return '10-20min'
    else: return '20+min'


def print_advanced_analysis(results, query, region):
    """🔥 Print all 13 metrics - LOCATION WISE ✅"""
    print(f"\n🚀 ADVANCED TREND ANALYSIS FOR: '{query}' in {region}")
    print("=" * 80)
    
    # 5. Top Tags
    print(f"\n🏷️  TOP 10 TAGS:")
    for i, (tag, count) in enumerate(results['tags'].most_common(10), 1):
        print(f"{i:2d}. #{tag:<25} ({count})")
    
    # 6. Top Hooks
    print(f"\n🎣 TOP HOOKS (Title starts):")
    for i, (hook, count) in enumerate(results['hooks'].most_common(8), 1):
        print(f"{i:2d}. '{hook:<20}' ({count})")
    
    # 7. Category trends
    print(f"\n📊 CATEGORY WISE TRENDS:")
    print("-" * 40)
    for i, (cat, count) in enumerate(results['category_stats'].most_common(), 1):
        print(f"{i}. {cat:<15} | Videos: {count}")
    
    # 8. Category wise hooks + tags
    print(f"\n🔥 TOP 3 CATEGORIES - TAGS:")
    for cat, _ in results['category_stats'].most_common(3):
        cat_tags = [tag for tag, _ in results['tags'].most_common(5)]
        print(f"  {cat}: {', '.join(cat_tags[:3])}")
    
    # 9. Music category
    if results['music_category']:
        print(f"\n🎵 MUSIC CATEGORY TRENDING:")
        top_music = max(results['music_category'], key=lambda x: x['views'])
        print(f"TOP: {top_music['title'][:50]}...")
    
    # 10. Optimal duration
    print(f"\n⏱️  BEST VIDEO LENGTH:")
    if results['duration_stats']:
        top_duration = results['duration_stats'].most_common(1)[0]
        print(f"WINNER: {top_duration[0]} ({top_duration[1]} videos)")
    
    # 11. Avg attention time (estimation)
    print(f"\n👁️  ATTENTION ANALYSIS:")
    print(f"Avg engagement: {results['avg_engagement']:.0f} views per like")
    
    # 12. Best engagement videos
    print(f"\n💎 TOP PERFORMERS:")
    if results['top_performers']['highest_views']:
        print(f"🔥 Most Views: {results['top_performers']['highest_views']['title'][:50]}...")
    if results['top_performers']['highest_engagement']:
        print(f"⭐ Most Engagement: {results['top_performers']['highest_engagement']['title'][:50]}...")
    
    # 13. Algorithm recommendations
    print(f"\n🤖 ALGORITHM TIPS:")
    if results['category_stats']:
        top_cat = results['category_stats'].most_common(1)[0][0]
        print(f"• Push {top_cat} content")
    if results['hooks']:
        top_hooks = list(results['hooks'].keys())[:2]
        hooks_str = ', '.join(['"' + h + '"' for h in top_hooks])
        print(f"• Use hooks: {hooks_str}")


def master_advanced_analyzer(query, region='IN'):  # 🔥 LOCATION PARAMETER ADDED
    """🔥 MAIN FUNCTION - LOCATION WISE ✅"""
    print(f"\n🎯 ADVANCED ANALYSIS FOR: '{query}' in {region}")
    print("=" * 80)
    
    search_time = time.strftime("%Y-%m-%d %H:%M:%S IST")
    videos_data = get_search_results_with_stats(query, region=region)  # 🔥 LOCATION PASSED
    
    if not videos_data:
        print("❌ No video data found!")
        return
    
    print(f"✅ Analyzed {len(videos_data)} top videos from {region}")
    trends = analyze_trends(videos_data)
    print_advanced_analysis(trends, query, region)
    
    # Save complete analysis
    results = {
        'query': query,
        'region': region,  # 🔥 LOCATION SAVED
        'search_time': search_time,
        'videos_analyzed': len(videos_data),
        'trends': trends
    }
    
    filename = f"new_{query.replace(' ', '_')}_{region}_{int(time.time())}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Saved: {filename}")


# 🔥 TERMINAL MODE - LOCATION INPUT ✅
def main():
    print("🔥 YOUTUBE TREND ANALYZER v6.0 - LOCATION WISE ✅")
    print("=" * 70)
    print("📍 Now searches INDIA-SPECIFIC trends (Kanpur/Delhi/Mumbai etc)")
    print("📊 Tags + Hooks + Category + Duration + Engagement + Algorithm")
    print("💡 Try: 'moisturizer review', 'face serum', 'music trends'")
    
    while True:
        try:
            print("\n🌍 CITIES: kanpur, lucknow, delhi, mumbai, bangalore, india")
            query = input("🔍 Enter query: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            city = input("🏙️  City (or press Enter for INDIA): ").strip().lower()
            region = CITIES.get(city, 'IN')  # 🔥 AUTO MAP CITY TO REGION
            
            if query:
                master_advanced_analyzer(query, region)
                print("\n" + "="*80)
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"💥 Error: {e}")
            continue


if __name__ == "__main__":
    main()

