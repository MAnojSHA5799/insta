# import requests
# import json
# import random
# from datetime import datetime
# import re
# from collections import Counter

# API_KEY = "aywRM7ESwi8P87FWkmLeFW3B"
# BASE_URL = "https://www.searchapi.io/api/v1/search"

# MAJOR_CITIES = [
#     "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", 
#     "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
#     "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
#     "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", 
#     "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut"
# ]

# AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+", "Gen Z", "Millennials", "Gen X"]
# SEARCH_TIME_SLOTS = ["12-3AM", "3-6AM", "6-9AM", "9-12PM", "12-3PM", "3-6PM", "6-9PM", "9-12PM"]

# PLATFORMS = [
#     "Amazon", "Flipkart", "Meesho", "Myntra", "Nykaa", 
#     "Zepto", "Blinkit", "Instamart", "Personal Website"
# ]

# PRICE_RANGES = ["₹200-500", "₹500-1000", "₹1000-2000", "₹2000-5000", "₹5000+"]
# BRAND_KEYWORDS = {
#     "hair": ["Mamaearth", "The Ordinary", "Minimalist", "WOW", "Biotique"],
#     "general": ["best", "top 10", "review", "price", "buy online"]
# }

# # 🔥 WINTER SERUM RECOMMENDATIONS
# WINTER_SERUMS = [
#     {"brand": "Minimalist", "product": "10% Niacinamide + Winter Hydration", "rating": "4.8⭐", "price": "₹599"},
#     {"brand": "Mamaearth", "product": "Onion Winter Repair Serum", "rating": "4.6⭐", "price": "₹399"},
#     {"brand": "The Ordinary", "product": "Multi-Peptide Winter Serum", "rating": "4.7⭐", "price": "₹1,299"},
#     {"brand": "WOW", "product": "Winter Argan + Almond Serum", "rating": "4.5⭐", "price": "₹499"},
#     {"brand": "Biotique", "product": "Winter Bio Morning Nectar", "rating": "4.4⭐", "price": "₹299"}
# ]

# def generate_winter_serum_recommendations():
#     recommendations = []
#     for item in WINTER_SERUMS:
#         demand = random.randint(25000, 95000)
#         recommendations.append({
#             "brand": item["brand"],
#             "product": item["product"],
#             "rating": item["rating"],
#             "price": item["price"],
#             "winter_searches": f"{demand:,}",
#             "demand_score": f"{random.randint(85, 98)}%"
#         })
#     return sorted(recommendations, key=lambda x: int(x["winter_searches"].replace(',', '')), reverse=True)

# def fetch_search_demand(keyword):
#     params = {"engine": "google", "q": keyword, "gl": "in", "hl": "en", "num": 10, "api_key": API_KEY}
#     print("🔍 Searching Google via SearchAPI...")
#     response = requests.get(BASE_URL, params=params)
#     print("HTTP Status:", response.status_code)
#     data = response.json()
#     if "error" in data:
#         print("❌ API ERROR:", data["error"])
#         return None
#     return data

# def parse_demand_signal(data):
#     result = {"timestamp": datetime.now().isoformat(), "organic_results_count": 0, "related_queries": [], "people_also_ask": []}
#     result["organic_results_count"] = len(data.get("organic_results", []))
#     for r in data.get("related_searches", []): result["related_queries"].append(r.get("query"))
#     for p in data.get("people_also_ask", []): result["people_also_ask"].append(p.get("question"))
#     return result

# def extract_target_cities_and_count(query):
#     query_lower = query.lower()
#     target_count = 15
#     numbers = re.findall(r'top\s+(\d+)', query_lower)
#     if numbers:
#         target_count = min(int(numbers[0]), len(MAJOR_CITIES))
#     cities = [city for city in MAJOR_CITIES if city.lower() in query_lower]
#     if cities:
#         target_cities = cities[:target_count]
#     else:
#         target_cities = MAJOR_CITIES[:target_count]
#     print(f"🎯 Target: {target_count} cities | Selected: {', '.join(target_cities[:5])}...")
#     return target_cities, target_count

# def generate_brand_keywords(base_keyword):
#     keywords = []
#     category = "hair" if "hair" in base_keyword.lower() else "general"
#     base_kws = BRAND_KEYWORDS.get(category, BRAND_KEYWORDS["general"])
#     for brand in base_kws:
#         keywords.append({
#             "keyword": f"{brand} {base_keyword}",
#             "monthly_searches": random.randint(10000, 80000),
#             "search_volume": f"{random.randint(10000, 80000):,}",
#             "brand_score": random.randint(70, 98)
#         })
#     return sorted(keywords, key=lambda x: x["monthly_searches"], reverse=True)[:5]

# def generate_platform_analysis():
#     platform_data = []
#     for platform in PLATFORMS:
#         traffic = random.randint(50000, 300000)
#         conversion = random.uniform(2.5, 8.5)
#         platform_data.append({
#             "platform": platform,
#             "traffic_share": f"{traffic:,}",
#             "conversion_rate": f"{conversion:.1f}%",
#             "market_share": random.randint(8, 35)
#         })
#     return sorted(platform_data, key=lambda x: x["market_share"], reverse=True)

# def generate_price_range_analysis(city_data):
#     price_data = []
#     top_cities = [item['city'] for item in city_data[:5]]
#     for price_range in PRICE_RANGES:
#         for city in top_cities:
#             traffic = random.randint(2000, 15000)
#             price_data.append({
#                 "price_range": price_range,
#                 "city": city,
#                 "traffic": f"{traffic:,}",
#                 "searches": random.randint(500, 3000)
#             })
#     return sorted(price_data, key=lambda x: int(x["searches"]), reverse=True)[:8]

# def generate_city_demand_ranking(target_cities, target_count):
#     all_data = []
#     city_demand_scores = {city: (100 if city in ["Delhi", "Mumbai", "Bangalore"] else random.randint(60, 95)) for city in target_cities}
#     entries_per_city = max(1, target_count // len(target_cities) + 1)
    
#     for city in target_cities:
#         for _ in range(entries_per_city):
#             if len(all_data) >= target_count: break
#             age_group = random.choice(AGE_GROUPS)
#             interest_score = min(100, city_demand_scores[city] + random.randint(-5, 5))
#             peak_time = random.choice(SEARCH_TIME_SLOTS)
#             searches = random.randint(5000, 50000)
#             all_data.append({
#                 "city": city, "rank": len(all_data) + 1, "demand_score": f"{interest_score}%",
#                 "age_group": age_group, "monthly_searches": searches, "peak_search_time": peak_time,
#                 "search_volume": f"{searches:,}"
#             })
    
#     sorted_data = sorted(all_data, key=lambda x: int(x["demand_score"][:-1]), reverse=True)
#     for i, item in enumerate(sorted_data): item["rank"] = i + 1
#     return sorted_data[:target_count]

# def analyze_top_cities_demand(city_data):
#     city_summary = {}
#     for item in city_data:
#         city = item['city']
#         if city not in city_summary:
#             city_summary[city] = {'total_demand': 0, 'count': 0, 'peak_times': [], 'avg_searches': 0}
#         city_summary[city]['total_demand'] += int(item["demand_score"][:-1])
#         city_summary[city]['count'] += 1
#         city_summary[city]['peak_times'].append(item['peak_search_time'])
#         city_summary[city]['avg_searches'] += item['monthly_searches']
    
#     for city in city_summary:
#         city_summary[city]['avg_demand'] = city_summary[city]['total_demand'] / city_summary[city]['count']
#         city_summary[city]['avg_searches'] /= city_summary[city]['count']
#         city_summary[city]['dominant_time'] = Counter(city_summary[city]['peak_times']).most_common(1)[0][0]
    
#     top_cities = sorted(city_summary.items(), key=lambda x: x[1]['avg_demand'], reverse=True)[:5]
#     top_times = Counter([item['peak_search_time'] for item in city_data]).most_common(3)
#     return top_cities, top_times

# def enhanced_parse_demand_signal(data, original_query):
#     result = parse_demand_signal(data)
#     target_cities, target_count = extract_target_cities_and_count(original_query)
#     city_data = generate_city_demand_ranking(target_cities, target_count)
#     top_cities_demand, top_times = analyze_top_cities_demand(city_data)
    
#     brand_keywords = generate_brand_keywords(original_query)
#     platform_data = generate_platform_analysis()
#     price_data = generate_price_range_analysis(city_data)
#     winter_recommendations = generate_winter_serum_recommendations()
    
#     result.update({
#         "target_cities": target_cities, "target_count": target_count,
#         "city_demand_ranking": city_data, "top_5_demand_cities": top_cities_demand,
#         "top_3_peak_times": top_times, "total_cities_analyzed": len(set([d["city"] for d in city_data])),
#         "brand_keywords": brand_keywords, "platform_analysis": platform_data,
#         "price_range_traffic": price_data, "winter_serum_recommendations": winter_recommendations
#     })
#     return result

# def main():
#     test_queries = ["Hair serum demand top 15 city in india"]
    
#     for keyword in test_queries:
#         print(f"\n{'='*150}")
#         print(f" QUERY: {keyword}")
#         print('='*150)
        
#         data = fetch_search_demand(keyword)
#         if not data: continue
        
#         parsed = enhanced_parse_demand_signal(data, keyword)
        
#         print(f"\n ORIGINAL DEMAND:")
#         print(f"Organic results: {parsed['organic_results_count']}")
#         print("Related: ", parsed['related_queries'][:3])
        
#         print(f"\n TOP 10 CITIES - DEMAND RANKING:")
#         print("=" * 140)
#         for i, item in enumerate(parsed['city_demand_ranking'][:10], 1):
#             print(f"{i:2d}. {item['city']:12s} | DEMAND {item['demand_score']:4s} | AGE {item['age_group']:8s} | {item['search_volume']:8s} | {item['peak_search_time']:7s}")
        
#         print(f"\n TOP 5 CITIES OVERALL:")
#         for i, (city, stats) in enumerate(parsed['top_5_demand_cities'], 1):
#             print(f"{i}. {city:12s} | {stats['avg_demand']:5.1f}% | {stats['dominant_time']:7s}")
        
#         print(f"\n TOP 3 PEAK TIMES:")
#         for i, (time_slot, count) in enumerate(parsed['top_3_peak_times'], 1):
#             print(f"{i}. {time_slot:10s} → {count} cities")
        
#         print(f"\n TOP 5 BRAND KEYWORDS:")
#         print("-" * 80)
#         for i, kw in enumerate(parsed['brand_keywords'], 1):
#             print(f"{i}. '{kw['keyword']}' → {kw['search_volume']} | Score: {kw['brand_score']}%")
        
#         print(f"\n BEST HAIR SERUM FOR WINTER (Top 5):")
#         print("=" * 80)
#         for i, winter_serum in enumerate(parsed['winter_serum_recommendations'], 1):
#             print(f"{i}. {winter_serum['brand']:12s} | {winter_serum['product']}")
#             print(f"    {winter_serum['rating']} | {winter_serum['price']} | Winter Searches: {winter_serum['winter_searches']} | Demand: {winter_serum['demand_score']}")
        
#         print(f"\n ALL 9 PLATFORMS (COMPLETE LIST):")
#         print("=" * 90)
#         for i, platform in enumerate(parsed['platform_analysis'], 1):
#             print(f"{i:2d}. {platform['platform']:14s} | Traffic: {platform['traffic_share']:9s} | Conv: {platform['conversion_rate']:5s} | Share: {platform['market_share']}%")
        
#         print(f"\n PRICE RANGE TRAFFIC (Top Cities):")
#         print("-" * 70)
#         for i, pr in enumerate(parsed['price_range_traffic'][:6], 1):
#             print(f"{i}. {pr['city']:12s} | {pr['price_range']:10s} | {pr['traffic']}")
        
#         print(f"\n KEY INSIGHTS:")
#         print(f"• #1 City: {parsed['city_demand_ranking'][0]['city']}")
#         print(f"• #1 Brand KW: '{parsed['brand_keywords'][0]['keyword']}'")
#         print(f"• #1 Platform: {parsed['platform_analysis'][0]['platform']} ({parsed['platform_analysis'][0]['market_share']}%)")
#         print(f"• Hot Price Range: {parsed['price_range_traffic'][0]['price_range']}")
#         print(f"• #1 Winter Serum: {parsed['winter_serum_recommendations'][0]['brand']} ({parsed['winter_serum_recommendations'][0]['winter_searches']})")
#         print("=" * 150)

# if __name__ == "__main__":
#     main()






import requests
import json
import random
from datetime import datetime
import re
from collections import Counter

API_KEY = "aywRM7ESwi8P87FWkmLeFW3B"
BASE_URL = "https://www.searchapi.io/api/v1/search"

MAJOR_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", 
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
    "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", 
    "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut"
]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+", "Gen Z", "Millennials", "Gen X"]
SEARCH_TIME_SLOTS = ["12-3AM", "3-6AM", "6-9AM", "9-12PM", "12-3PM", "3-6PM", "6-9PM", "9-12PM"]

PLATFORMS = ["Amazon", "Flipkart", "Meesho", "Myntra", "Nykaa", "Zepto", "Blinkit", "Instamart", "Personal Website"]
PRICE_RANGES = ["₹200-500", "₹500-1000", "₹1000-2000", "₹2000-5000", "₹5000+"]

# 🔥 SEASONAL CATEGORY CONFIG
CATEGORY_CONFIG = {
    "hair_serum": {
        "type": "spiky",  # Winter + festive spikes
        "brands": ["Mamaearth", "The Ordinary", "Minimalist", "WOW", "Biotique"],
        "winter_keywords": ["dry hair winter", "hair repair winter", "frizz control winter", "winter hair serum"],
        "summer_keywords": ["anti frizz summer", "light hair serum", "summer hair serum"],
        "peak_times": ["6-9PM", "9-12PM", "3-6AM"]  # Evening research
    },
    "body_lotion": {
        "type": "always_on",  # Year-round with seasonal shift
        "brands": ["Nivea", "Vaseline", "Cetaphil", "Lakme", "Ponds"],
        "winter_keywords": ["dry skin lotion", "intense moisture lotion", "winter body lotion", "cracked skin repair"],
        "summer_keywords": ["lightweight lotion", "non sticky lotion", "SPF body lotion", "cooling lotion"],
        "peak_times": ["6-9PM", "9-12PM", "9-12AM"]  # Evening + morning refill
    },
    "lip_balm": {
        "type": "always_on",  # Year-round essential
        "brands": ["Maybelline", "Nivea", "Vaseline", "Biotique", "Lotus"],
        "winter_keywords": ["chapped lips balm", "repair lip balm", "overnight lip mask", "shea butter lip balm"],
        "summer_keywords": ["SPF lip balm", "tinted lip balm", "non heavy lip balm", "matte lip balm"],
        "peak_times": ["6-9PM", "9-12PM"]  # Evening routine
    },
    "auto": {
        "brands": ["Maruti", "Hyundai", "Tata", "Mahindra", "Honda"],
        "special_recommendations": [
            {"brand": "Maruti", "model": "Swift", "rating": "4.6⭐", "price": "₹6.49L"},
            {"brand": "Hyundai", "model": "Creta", "rating": "4.7⭐", "price": "₹11.11L"},
            {"brand": "Tata", "model": "Nexon", "rating": "4.5⭐", "price": "₹8.15L"}
        ]
    }
}

# Current season detection (Dec = Winter)
CURRENT_MONTH = datetime.now().month
CURRENT_SEASON = "winter" if CURRENT_MONTH in [12, 1, 2] else "summer"

def detect_category(query):
    """🔥 Auto-detect category from query"""
    query_lower = query.lower()
    for category in CATEGORY_CONFIG:
        if category in query_lower or any(word in query_lower for word in [category.replace("_", " "), category.replace("_", "-")]):
            return category
    return "general"

def get_seasonal_keywords(category, season):
    """🔥 Seasonal keywords based on category + season"""
    config = CATEGORY_CONFIG.get(category, {})
    return config.get(f"{season}_keywords", config.get("summer_keywords", []))

def get_peak_search_times(category):
    """🔥 Category-specific peak times"""
    return CATEGORY_CONFIG.get(category, {}).get("peak_times", SEARCH_TIME_SLOTS)

def adjust_platform_weights(category, season):
    """🔥 Adjust platform shares based on category + season"""
    base_data = []
    quick_commerce_boost = 1.3 if category in ["body_lotion", "lip_balm"] else 1.0
    nykaa_boost = 1.4 if category == "hair_serum" and season == "winter" else 1.0
    
    for platform in PLATFORMS:
        traffic = random.randint(50000, 300000)
        conversion = random.uniform(2.5, 8.5)
        market_share = random.randint(8, 35)
        
        # Boost quick commerce for always_on categories
        if platform in ["Zepto", "Blinkit", "Instamart"] and category in ["body_lotion", "lip_balm"]:
            market_share = int(market_share * quick_commerce_boost)
        
        # Boost Nykaa for hair winter
        if platform == "Nykaa" and category == "hair_serum" and season == "winter":
            market_share = int(market_share * nykaa_boost)
            
        base_data.append({
            "platform": platform,
            "traffic_share": f"{traffic:,}",
            "conversion_rate": f"{conversion:.1f}%",
            "market_share": min(40, market_share)  # Cap at 40%
        })
    return sorted(base_data, key=lambda x: x["market_share"], reverse=True)

# YOUR ORIGINAL FUNCTIONS (unchanged)
def fetch_search_demand(keyword):
    params = {"engine": "google", "q": keyword, "gl": "in", "hl": "en", "num": 10, "api_key": API_KEY}
    print("🔍 Searching Google via SearchAPI...")
    response = requests.get(BASE_URL, params=params)
    print("HTTP Status:", response.status_code)
    data = response.json()
    if "error" in data:
        print("❌ API ERROR:", data["error"])
        return None
    return data

def parse_demand_signal(data):
    result = {"timestamp": datetime.now().isoformat(), "organic_results_count": 0, "related_queries": [], "people_also_ask": []}
    result["organic_results_count"] = len(data.get("organic_results", []))
    for r in data.get("related_searches", []): result["related_queries"].append(r.get("query"))
    for p in data.get("people_also_ask", []): result["people_also_ask"].append(p.get("question"))
    return result

def extract_target_cities_and_count(query):
    query_lower = query.lower()
    target_count = 15
    numbers = re.findall(r'top\s+(\d+)', query_lower)
    if numbers:
        target_count = min(int(numbers[0]), len(MAJOR_CITIES))
    cities = [city for city in MAJOR_CITIES if city.lower() in query_lower]
    if cities:
        target_cities = cities[:target_count]
    else:
        target_cities = MAJOR_CITIES[:target_count]
    print(f"🎯 Target: {target_count} cities | Selected: {', '.join(target_cities[:5])}...")
    return target_cities, target_count

def generate_brand_keywords(base_keyword, category):
    config = CATEGORY_CONFIG.get(category, {"brands": ["best", "top 10", "review", "price", "buy online"]})
    seasonal_kws = get_seasonal_keywords(category, CURRENT_SEASON)
    keywords = []
    
    # Mix brand + seasonal keywords
    all_brands = config["brands"] + seasonal_kws[:2]
    for brand in all_brands[:5]:
        keywords.append({
            "keyword": f"{brand} {base_keyword}",
            "monthly_searches": random.randint(10000, 80000),
            "search_volume": f"{random.randint(10000, 80000):,}",
            "brand_score": random.randint(70, 98)
        })
    return sorted(keywords, key=lambda x: x["monthly_searches"], reverse=True)[:5]

def generate_price_range_analysis(city_data):
    price_data = []
    top_cities = [item['city'] for item in city_data[:5]]
    for price_range in PRICE_RANGES:
        for city in top_cities:
            traffic = random.randint(2000, 15000)
            price_data.append({
                "price_range": price_range,
                "city": city,
                "traffic": f"{traffic:,}",
                "searches": random.randint(500, 3000)
            })
    return sorted(price_data, key=lambda x: int(x["searches"]), reverse=True)[:8]

def generate_city_demand_ranking(target_cities, target_count, category):
    all_data = []
    city_demand_scores = {city: (100 if city in ["Delhi", "Mumbai", "Bangalore"] else random.randint(60, 95)) for city in target_cities}
    entries_per_city = max(1, target_count // len(target_cities) + 1)
    peak_times = get_peak_search_times(category)
    
    for city in target_cities:
        for _ in range(entries_per_city):
            if len(all_data) >= target_count: break
            age_group = random.choice(AGE_GROUPS)
            interest_score = min(100, city_demand_scores[city] + random.randint(-5, 5))
            peak_time = random.choice(peak_times)  # 🔥 Category-specific peaks!
            searches = random.randint(5000, 50000)
            all_data.append({
                "city": city, "rank": len(all_data) + 1, "demand_score": f"{interest_score}%",
                "age_group": age_group, "monthly_searches": searches, "peak_search_time": peak_time,
                "search_volume": f"{searches:,}"
            })
    
    sorted_data = sorted(all_data, key=lambda x: int(x["demand_score"][:-1]), reverse=True)
    for i, item in enumerate(sorted_data): item["rank"] = i + 1
    return sorted_data[:target_count]

def analyze_top_cities_demand(city_data):
    city_summary = {}
    for item in city_data:
        city = item['city']
        if city not in city_summary:
            city_summary[city] = {'total_demand': 0, 'count': 0, 'peak_times': [], 'avg_searches': 0}
        city_summary[city]['total_demand'] += int(item["demand_score"][:-1])
        city_summary[city]['count'] += 1
        city_summary[city]['peak_times'].append(item['peak_search_time'])
        city_summary[city]['avg_searches'] += item['monthly_searches']
    
    for city in city_summary:
        city_summary[city]['avg_demand'] = city_summary[city]['total_demand'] / city_summary[city]['count']
        city_summary[city]['avg_searches'] /= city_summary[city]['count']
        city_summary[city]['dominant_time'] = Counter(city_summary[city]['peak_times']).most_common(1)[0][0]
    
    top_cities = sorted(city_summary.items(), key=lambda x: x[1]['avg_demand'], reverse=True)[:5]
    top_times = Counter([item['peak_search_time'] for item in city_data]).most_common(3)
    return top_cities, top_times

def enhanced_parse_demand_signal(data, original_query, category):
    result = parse_demand_signal(data)
    target_cities, target_count = extract_target_cities_and_count(original_query)
    city_data = generate_city_demand_ranking(target_cities, target_count, category)
    top_cities_demand, top_times = analyze_top_cities_demand(city_data)
    
    brand_keywords = generate_brand_keywords(original_query, category)
    platform_data = adjust_platform_weights(category, CURRENT_SEASON)
    price_data = generate_price_range_analysis(city_data)
    
    result.update({
        "target_cities": target_cities, "target_count": target_count,
        "city_demand_ranking": city_data, "top_5_demand_cities": top_cities_demand,
        "top_3_peak_times": top_times,
        "brand_keywords": brand_keywords, "platform_analysis": platform_data,
        "price_range_traffic": price_data, "detected_category": category,
        "current_season": CURRENT_SEASON
    })
    return result

def main():
    test_queries = [
        "Hair serum demand top 15 city in india",
        "Body lotion demand top 10 city", 
        "Lip balm demand top 8 city"
    ]
    
    for keyword in test_queries:
        category = detect_category(keyword)
        print(f"\n{'='*160}")
        print(f"🔍 QUERY: {keyword} | 🏷️ CATEGORY: {category.upper()} | ❄️ SEASON: {CURRENT_SEASON.upper()}")
        print('='*160)
        
        data = fetch_search_demand(keyword)
        if not data: continue
        
        parsed = enhanced_parse_demand_signal(data, keyword, category)
        
        print(f"\n📊 ORIGINAL DEMAND:")
        print(f"Organic results: {parsed['organic_results_count']}")
        print("Related: ", parsed['related_queries'][:3])
        
        print(f"\n🏆 TOP 10 CITIES - DEMAND RANKING ({CURRENT_SEASON.upper()}):")
        print("=" * 140)
        for i, item in enumerate(parsed['city_demand_ranking'][:10], 1):
            print(f"{i:2d}. {item['city']:12s} | DEMAND {item['demand_score']:4s} | AGE {item['age_group']:8s} | {item['search_volume']:8s} | ⏰{item['peak_search_time']:7s}")
        
        print(f"\n🔥 TOP 5 CITIES ({category.upper()}):")
        for i, (city, stats) in enumerate(parsed['top_5_demand_cities'], 1):
            print(f"{i}. {city:12s} | {stats['avg_demand']:5.1f}% | {stats['dominant_time']:7s}")
        
        print(f"\n⏰ TOP 3 PEAK TIMES ({CURRENT_SEASON.upper()}):")
        for i, (time_slot, count) in enumerate(parsed['top_3_peak_times'], 1):
            print(f"{i}. {time_slot:10s} → {count} cities")
        
        print(f"\n🔑 TOP 5 KEYWORDS ({category.upper()} - {CURRENT_SEASON.upper()}):")
        print("-" * 90)
        for i, kw in enumerate(parsed['brand_keywords'], 1):
            print(f"{i}. '{kw['keyword']}' → {kw['search_volume']} | Score: {kw['brand_score']}%")
        
        print(f"\n🛒 ALL 9 PLATFORMS ({category.upper()} - {CURRENT_SEASON.upper()}):")
        print("=" * 90)
        for i, platform in enumerate(parsed['platform_analysis'], 1):
            print(f"{i:2d}. {platform['platform']:14s} | Traffic: {platform['traffic_share']:9s} | Conv: {platform['conversion_rate']:5s} | Share: {platform['market_share']}%")
        
        print(f"\n💰 PRICE RANGE TRAFFIC:")
        print("-" * 70)
        for i, pr in enumerate(parsed['price_range_traffic'][:6], 1):
            print(f"{i}. {pr['city']:12s} | {pr['price_range']:10s} | {pr['traffic']}")
        
        print(f"\n🎯 KEY INSIGHTS ({category.upper()} - {CURRENT_SEASON.upper()}):")
        print(f"• #1 City: {parsed['city_demand_ranking'][0]['city']} ({parsed['city_demand_ranking'][0]['demand_score']})")
        print(f"• #1 Keyword: '{parsed['brand_keywords'][0]['keyword']}'")
        print(f"• #1 Platform: {parsed['platform_analysis'][0]['platform']} ({parsed['platform_analysis'][0]['market_share']}%)")
        print(f"• Peak Time: {parsed['top_3_peak_times'][0][0]}")
        print(f"• Category Type: {CATEGORY_CONFIG[category]['type']}")
        print("=" * 160)

if __name__ == "__main__":
    main()

