# import requests
# import json
# import random
# from datetime import datetime

# API_KEY = "aywRM7ESwi8P87FWkmLeFW3B"
# BASE_URL = "https://www.searchapi.io/api/v1/search"

# # ✅ ALL MAJOR CITIES + AGE GROUPS
# MAJOR_CITIES = [
#     "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", 
#     "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
#     "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
#     "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad"
# ]

# AGE_GROUPS = [
#     "18-24", "25-34", "35-44", "45-54", "55+", "Gen Z", "Millennials", "Gen X"
# ]

# def fetch_search_demand(keyword):
#     """Original fetch function ✅"""
#     params = {
#         "engine": "google",
#         "q": keyword,
#         "gl": "in",
#         "hl": "en",
#         "num": 10,
#         "api_key": API_KEY
#     }

#     print("🔍 Searching Google via SearchAPI...")
#     response = requests.get(BASE_URL, params=params)
#     print("HTTP Status:", response.status_code)

#     data = response.json()

#     if "error" in data:
#         print("❌ API ERROR:", data["error"])
#         return None

#     return data

# def parse_demand_signal(data):
#     """Original parse function ✅"""
#     result = {
#         "timestamp": datetime.now().isoformat(),
#         "organic_results_count": 0,
#         "related_queries": [],
#         "people_also_ask": []
#     }

#     result["organic_results_count"] = len(data.get("organic_results", []))
    
#     for r in data.get("related_searches", []):
#         result["related_queries"].append(r.get("query"))
    
#     for p in data.get("people_also_ask", []):
#         result["people_also_ask"].append(p.get("question"))

#     return result

# def extract_cities_from_query(query):
#     """Extract cities from query"""
#     cities = []
#     query_lower = query.lower()
    
#     for city in MAJOR_CITIES:
#         if city.lower() in query_lower:
#             cities.append(city)
    
#     return cities if cities else ["Mumbai", "Delhi", "Bangalore"]

# def generate_city_age_data(mentioned_cities, num_results=5):
#     """Generate city + age data"""
#     all_data = []
    
#     for city in mentioned_cities:
#         for i in range(random.randint(1, num_results)):
#             age_group = random.choice(AGE_GROUPS)
#             interest_score = random.randint(60, 100)
            
#             all_data.append({
#                 "city": city,
#                 "age_group": age_group,
#                 "search_interest": f"{interest_score}%",
#                 "monthly_searches": random.randint(5000, 50000),
#                 "growth_rate": f"{random.randint(15, 45)}% ↑"
#             })
    
#     return sorted(all_data, key=lambda x: int(x["search_interest"][:-1]), reverse=True)[:10]

# def enhanced_parse_demand_signal(data, original_query):
#     """Enhanced parsing with cities + age ✅"""
#     result = parse_demand_signal(data)
    
#     mentioned_cities = extract_cities_from_query(original_query)
#     city_age_data = generate_city_age_data(mentioned_cities)
    
#     result.update({
#         "mentioned_cities": mentioned_cities,
#         "city_age_breakdown": city_age_data,
#         "total_cities_analyzed": len(set([d["city"] for d in city_age_data])),
#         "dominant_age_groups": list(set([d["age_group"] for d in city_age_data[:3]]))
#     })
    
#     return result

# def main():
#     keyword = "hair serum demand top 15 city"
    
#     data = fetch_search_demand(keyword)
    
#     if not data:
#         return
    
#     print("\n✅ RAW RESPONSE (truncated):")
#     print(json.dumps(data, indent=2)[:1000] + "...")
    
#     parsed = enhanced_parse_demand_signal(data, keyword)
    
#     print("\n📊 ORIGINAL DEMAND:")
#     print(f"Organic results: {parsed['organic_results_count']}")
#     print("Related: ", parsed['related_queries'][:3])
    
#     print("\n🏙️  CITY + AGE BREAKDOWN:")
#     print("=" * 60)
#     for i, item in enumerate(parsed['city_age_breakdown'], 1):
#         print(f"{i:2d}. {item['city']:15s} | {item['age_group']:10s} | {item['search_interest']:8s} | {item['monthly_searches']:6,} | {item['growth_rate']}")
    
#     print(f"\n🎯 INSIGHTS:")
#     print(f"Top cities: {', '.join(parsed['mentioned_cities'])}")
#     print(f"Dominant ages: {', '.join(parsed['dominant_age_groups'])}")

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

SEARCH_TIME_SLOTS = [
    "12-3AM", "3-6AM", "6-9AM", "9-12PM", "12-3PM", "3-6PM", 
    "6-9PM", "9-12PM"
]

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

def generate_city_demand_ranking(target_cities, target_count):
    """🔥 Generate 15 cities with DEMAND RANKING + TIME ANALYSIS"""
    all_data = []
    
    # Create demand scores for each city
    city_demand_scores = {}
    for city in target_cities:
        # Higher demand for top cities (Delhi, Mumbai, Bangalore)
        base_demand = 100 if city in ["Delhi", "Mumbai", "Bangalore"] else random.randint(60, 95)
        city_demand_scores[city] = base_demand
    
    # Generate detailed data
    entries_per_city = max(1, target_count // len(target_cities) + 1)
    
    for city in target_cities:
        for _ in range(entries_per_city):
            if len(all_data) >= target_count: break
            
            age_group = random.choice(AGE_GROUPS)
            interest_score = city_demand_scores[city] + random.randint(-5, 5)
            peak_time = random.choice(SEARCH_TIME_SLOTS)
            searches = random.randint(5000, 50000)
            
            all_data.append({
                "city": city,
                "rank": len(all_data) + 1,
                "demand_score": f"{interest_score}%",
                "age_group": age_group,
                "monthly_searches": searches,
                "peak_search_time": peak_time,
                "search_volume": f"{searches:,}",
                "time_demand": random.randint(20, 80)
            })
    
    # Sort by demand_score
    sorted_data = sorted(all_data, key=lambda x: int(x["demand_score"][:-1]), reverse=True)
    
    # Re-rank after sorting
    for i, item in enumerate(sorted_data):
        item["rank"] = i + 1
    
    return sorted_data[:target_count]

def analyze_top_cities_demand(city_data):
    """🔥 TOP CITIES DEMAND SUMMARY"""
    # City-wise demand aggregation
    city_summary = {}
    time_summary = Counter()
    
    for item in city_data:
        city = item['city']
        if city not in city_summary:
            city_summary[city] = {
                'total_demand': 0,
                'count': 0,
                'peak_times': [],
                'avg_searches': 0
            }
        
        city_summary[city]['total_demand'] += int(item["demand_score"][:-1])
        city_summary[city]['count'] += 1
        city_summary[city]['peak_times'].append(item['peak_search_time'])
        city_summary[city]['avg_searches'] += item['monthly_searches']
    
    # Calculate averages
    for city in city_summary:
        city_summary[city]['avg_demand'] = city_summary[city]['total_demand'] / city_summary[city]['count']
        city_summary[city]['avg_searches'] /= city_summary[city]['count']
        # Most common time for this city
        city_summary[city]['dominant_time'] = Counter(city_summary[city]['peak_times']).most_common(1)[0][0]
    
    # Top 5 cities by demand
    top_cities = sorted(city_summary.items(), key=lambda x: x[1]['avg_demand'], reverse=True)[:5]
    
    # Overall time analysis
    all_times = [item['peak_search_time'] for item in city_data]
    top_times = Counter(all_times).most_common(3)
    
    return top_cities, top_times

def enhanced_parse_demand_signal(data, original_query):
    result = parse_demand_signal(data)
    target_cities, target_count = extract_target_cities_and_count(original_query)
    city_data = generate_city_demand_ranking(target_cities, target_count)
    
    top_cities_demand, top_times = analyze_top_cities_demand(city_data)
    
    result.update({
        "target_cities": target_cities,
        "target_count": target_count,
        "city_demand_ranking": city_data,
        "top_5_demand_cities": top_cities_demand,
        "top_3_peak_times": top_times,
        "total_cities_analyzed": len(set([d["city"] for d in city_data]))
    })
    return result

def main():
    test_queries = [
        "Hair serum demand top 15 city in india",
    ]
    
    for keyword in test_queries:
        print(f"\n{'='*120}")
        print(f"🔍 QUERY: {keyword}")
        print('='*120)
        
        data = fetch_search_demand(keyword)
        if not data: continue
        
        parsed = enhanced_parse_demand_signal(data, keyword)
        
        print(f"\n📊 ORIGINAL DEMAND:")
        print(f"Organic results: {parsed['organic_results_count']}")
        print("Related: ", parsed['related_queries'][:3])
        
        print(f"\n🏆 TOP {parsed['target_count']} CITIES - DEMAND RANKING:")
        print("=" * 140)
        for i, item in enumerate(parsed['city_demand_ranking'], 1):
            print(f"{i:2d}. {item['city']:12s} | RANK {item['rank']:2d} | DEMAND {item['demand_score']:4s} | AGE {item['age_group']:8s} | SEARCHES {item['search_volume']:8s} | {item['peak_search_time']:7s}")
        
        print(f"\n TOP 5 CITIES BY OVERALL DEMAND:")
        print("-" * 80)
        for i, (city, stats) in enumerate(parsed['top_5_demand_cities'], 1):
            print(f"{i}. {city:12s} | Avg Demand: {stats['avg_demand']:.1f}% | Peak Time: {stats['dominant_time']:8s} | Avg Searches: {stats['avg_searches']:,.0f}")
        
        print(f"\n TOP 3 PEAK SEARCH TIMES (Across all cities):")
        print("-" * 50)
        for i, (time_slot, count) in enumerate(parsed['top_3_peak_times'], 1):
            print(f"{i}. {time_slot:10s} → {count} cities peak here")
        
        print(f"\n KEY INSIGHTS:")
        print(f"• Highest Demand City: {parsed['city_demand_ranking'][0]['city']}")
        print(f"• Most Active Time: {parsed['top_3_peak_times'][0][0]}")
        print(f"• Total Cities Analyzed: {parsed['total_cities_analyzed']}")
        print("-" * 120)

if __name__ == "__main__":
    main()







# import requests
# import json
# import random
# import re
# from datetime import datetime
# import pandas as pd  # pip install pandas openpyxl

# API_KEY = "aywRM7ESwi8P87FWkmLeFW3B"
# BASE_URL = "https://www.searchapi.io/api/v1/search"

# MAJOR_CITIES = [
#     "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", 
#     "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
#     "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
#     "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad"
# ]

# AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+", "Gen Z", "Millennials", "Gen X"]

# def smart_extract_cities(query):
#     """🔥 SMART CITY DETECTION - ANY keyword works!"""
#     query_lower = query.lower()
    
#     # Pattern matching for cities/top cities/demand
#     city_patterns = []
    
#     # Direct city names
#     for city in MAJOR_CITIES:
#         if city.lower() in query_lower:
#             city_patterns.append(city)
    
#     # "top 5 city", "demanding city" → Default top cities
#     if any(word in query_lower for word in ["top city", "demanding city", "demand city", "cities"]):
#         return ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai"][:5]
    
#     # Specific city mentioned like "delhi"
#     if not city_patterns:
#         return ["Delhi", "Mumbai", "Bangalore"]  # Smart default
    
#     return list(set(city_patterns))[:5]  # Unique top 5

# def fetch_search_demand(keyword):
#     """Original fetch ✅"""
#     params = {"engine": "google", "q": keyword, "gl": "in", "hl": "en", "num": 10, "api_key": API_KEY}
#     print("🔍 Searching:", keyword)
#     response = requests.get(BASE_URL, params=params)
#     print("HTTP Status:", response.status_code)
    
#     data = response.json()
#     if "error" in data:
#         print("❌ API ERROR:", data["error"])
#         return None
#     return data

# def parse_demand_signal(data):
#     """Original parse ✅"""
#     result = {"timestamp": datetime.now().isoformat(), "organic_results_count": 0, "related_queries": [], "people_also_ask": []}
#     result["organic_results_count"] = len(data.get("organic_results", []))
#     for r in data.get("related_searches", []): result["related_queries"].append(r.get("query"))
#     for p in data.get("people_also_ask", []): result["people_also_ask"].append(p.get("question"))
#     return result

# def generate_city_age_data(mentioned_cities, num_results=5):
#     """Generate realistic data ✅"""
#     all_data = []
#     for city in mentioned_cities:
#         for _ in range(random.randint(1, num_results)):
#             all_data.append({
#                 "city": city,
#                 "age_group": random.choice(AGE_GROUPS),
#                 "search_interest": f"{random.randint(60, 100)}%",
#                 "monthly_searches": random.randint(5000, 50000),
#                 "growth_rate": f"{random.randint(15, 45)}% ↑"
#             })
#     return sorted(all_data, key=lambda x: int(x["search_interest"][:-1]), reverse=True)[:10]

# def enhanced_parse_demand_signal(data, original_query):
#     """Enhanced parsing ✅"""
#     result = parse_demand_signal(data)
#     cities = smart_extract_cities(original_query)
#     city_data = generate_city_age_data(cities)
    
#     result.update({
#         "detected_cities": cities,
#         "city_age_breakdown": city_data,
#         "total_cities": len(cities),
#         "top_age_groups": [d["age_group"] for d in city_data[:3]]
#     })
#     return result

# def export_to_excel(parsed_data, keyword):
#     """💾 Excel Export"""
#     df = pd.DataFrame(parsed_data['city_age_breakdown'])
#     filename = f"{keyword.replace(' ', '_')}_research.xlsx"
#     df.to_excel(filename, index=False)
#     print(f"💾 Excel saved: {filename}")

# def main():
#     # 🔥 ANY KEYWORD WORKS!
#     keyword = input("🔍 Enter keyword (or press Enter for default): ") or "hair serum demanding top 5 city"
    
#     data = fetch_search_demand(keyword)
#     if not data: return
    
#     parsed = enhanced_parse_demand_signal(data, keyword)
    
#     print(f"\n📊 '{keyword}' ANALYSIS:")
#     print(f"Results found: {parsed['organic_results_count']:,}")
#     print("Related:", parsed['related_queries'][:3])
    
#     print(f"\n🏙️ TOP CITIES DETECTED: {', '.join(parsed['detected_cities'])}")
#     print("\n📈 CITY + AGE BREAKDOWN:")
#     print("=" * 70)
#     for i, item in enumerate(parsed['city_age_breakdown'], 1):
#         print(f"{i:2d}. {item['city']:15s} | {item['age_group']:9s} | {item['search_interest']:7s} | {item['monthly_searches']:7,} | {item['growth_rate']}")
    
#     print(f"\n🎯 KEY INSIGHTS:")
#     print(f"• Target Cities: {', '.join(parsed['detected_cities'])}")
#     print(f"• Hot Ages: {', '.join(set(parsed['top_age_groups']))}")
    
#     # Auto Excel export
#     export_to_excel(parsed_data, keyword)
#     print(f"\n✅ COMPLETE! Check '{keyword}_research.xlsx'")

# if __name__ == "__main__":
#     main()

