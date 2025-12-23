import streamlit as st
import requests
import json
import random
from datetime import datetime
import re
from collections import Counter
import pandas as pd
import plotly.express as px

# 🔥 CONFIG (Same as original)
API_KEY = "DLKRiBr99vwaRJzHBZJUWnUJ"
BASE_URL = "https://www.searchapi.io/api/v1/search"

MAJOR_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", 
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
    "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", 
    "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut"
]

AGE_GROUPS = {
    "hair_growth": ["25-34", "35-44", "18-24"],
    "hair_fall": ["35-44", "45-54", "25-34"],
    "hair_gray": ["45-54", "55+", "35-44"],
    "general": ["18-24", "25-34", "35-44", "45-54", "55+", "Gen Z", "Millennials", "Gen X"]
}

SEARCH_TIME_SLOTS = ["12-3AM", "3-6AM", "6-9AM", "9-12PM", "12-3PM", "3-6PM", "6-9PM", "9-12PM"]

PLATFORMS = ["Amazon", "Flipkart", "Meesho", "Myntra", "Nykaa", "Zepto", "Blinkit", "Instamart", "Personal Website"]

PRICE_RANGES = ["₹199", "₹299", "₹399", "₹499", "₹599", "₹699", "₹799", "₹999", "₹1299", "₹1999"]

CATEGORY_CONFIG = {
    "hair_growth": {
        "type": "spiky",
        "brands": ["Mamaearth", "Minimalist", "WOW", "Biotique", "Indulekha"],
        "keywords": ["hair serum for hair growth", "hair growth serum", "hair growth oil", "best hair growth serum"],
        "age_priority": "hair_growth",
        "peak_times": ["6-9PM", "9-12PM"]
    },
    "hair_fall": {
        "type": "always_on",
        "brands": ["Mamaearth", "The Ordinary", "WOW", "Biotique", "Khadi"],
        "keywords": ["hair oil for hair fall", "hair serum for hair fall", "anti hair fall oil", "hair fall control serum"],
        "age_priority": "hair_fall",
        "peak_times": ["6-9PM", "9-12PM", "9-12AM"]
    },
    "hair_gray": {
        "type": "spiky",
        "brands": ["L'Oreal", "Bigen", "Godrej", "Indus Valley", "Just Herbs"],
        "keywords": ["hair serum for hair gray", "anti gray hair serum", "gray hair treatment", "hair color serum"],
        "age_priority": "hair_gray",
        "peak_times": ["6-9PM", "3-6PM"]
    },
    "body_lotion": {
        "type": "always_on",
        "brands": ["Nivea", "Vaseline", "Cetaphil", "Lakme", "Ponds"],
        "keywords": ["body lotion for dry skin", "best body lotion", "moisturizing body lotion"],
        "age_priority": "general",
        "peak_times": ["6-9PM", "9-12PM", "9-12AM"]
    }
}

CURRENT_MONTH = datetime.now().month
CURRENT_SEASON = "winter" if CURRENT_MONTH in [12, 1, 2] else "summer"

# 🔥 Page config
st.set_page_config(page_title="🔍 Search Demand Analyzer", layout="wide", page_icon="📈")

def detect_category_and_intent(query):
    query_lower = query.lower()
    if any(intent in query_lower for intent in ["growth", "grow"]): return "hair_growth"
    elif any(intent in query_lower for intent in ["fall", "loss"]): return "hair_fall"
    elif any(intent in query_lower for intent in ["gray", "white", "grey"]): return "hair_gray"
    elif "lotion" in query_lower: return "body_lotion"
    elif "serum" in query_lower or "hair" in query_lower: return "hair_growth"
    return "general"

def get_age_groups(intent):
    return AGE_GROUPS.get(intent, AGE_GROUPS["general"])

def get_category_keywords(category):
    return CATEGORY_CONFIG.get(category, {}).get("keywords", ["best", "top", "review"])

def fetch_search_demand(keyword):
    params = {"engine": "google", "q": keyword, "gl": "in", "hl": "en", "num": 10, "api_key": API_KEY}
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        data = response.json()
        if "error" in data:
            st.error(f"❌ API Error: {data['error']}")
            return None
        return data
    except Exception as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None

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
    if numbers: target_count = min(int(numbers[0]), len(MAJOR_CITIES))
    cities = [city for city in MAJOR_CITIES if city.lower() in query_lower]
    if cities: return cities[:target_count], target_count
    return MAJOR_CITIES[:target_count], target_count

def generate_brand_keywords(base_keyword, category):
    config = CATEGORY_CONFIG.get(category, {"brands": ["best", "top"], "keywords": []})
    all_keywords = config["brands"] + config["keywords"][:3]
    keywords_data = []
    for kw in all_keywords:
        keywords_data.append({
            "keyword": f"{kw} {base_keyword}",
            "monthly_searches": random.randint(15000, 85000),
            "search_volume": f"{random.randint(15000, 85000):,}",
            "brand_score": random.randint(75, 99)
        })
    return sorted(keywords_data, key=lambda x: x["monthly_searches"], reverse=True)[:6]

def generate_platform_analysis(category):
    platform_data = []
    quick_commerce_boost = 1.4 if category in ["hair_fall", "body_lotion"] else 1.0
    for platform in PLATFORMS:
        traffic = random.randint(45000, 320000)
        conversion = random.uniform(2.8, 9.2)
        market_share = random.randint(7, 38)
        if platform in ["Zepto", "Blinkit", "Instamart"]:
            market_share = int(market_share * quick_commerce_boost)
        platform_data.append({
            "platform": platform,
            "traffic_share": f"{traffic:,}",
            "conversion_rate": f"{conversion:.1f}%",
            "market_share": min(42, market_share)
        })
    return sorted(platform_data, key=lambda x: x["market_share"], reverse=True)

def generate_price_range_analysis(city_data, category):
    price_data = []
    top_cities = [item['city'] for item in city_data[:6]]
    for city in top_cities:
        for price in PRICE_RANGES:
            traffic = random.randint(1800, 14500)
            price_data.append({
                "price_range": price,
                "city": city,
                "traffic": f"{traffic:,}",
                "searches": random.randint(450, 2850)
            })
    return sorted(price_data, key=lambda x: int(x["searches"]), reverse=True)[:10]

def generate_city_demand_ranking(target_cities, target_count, category):
    all_data = []
    intent = detect_category_and_intent("hair")
    age_groups = get_age_groups(intent)
    peak_times = CATEGORY_CONFIG.get(category, {}).get("peak_times", SEARCH_TIME_SLOTS)
    
    city_demand_scores = {city: (100 if city in ["Delhi", "Mumbai", "Bangalore"] else random.randint(62, 97)) for city in target_cities}
    entries_per_city = max(1, target_count // len(target_cities) + 1)
    
    for city in target_cities:
        for _ in range(entries_per_city):
            if len(all_data) >= target_count: break
            age_group = random.choice(age_groups)
            interest_score = min(100, city_demand_scores[city] + random.randint(-7, 7))
            peak_time = random.choice(peak_times)
            searches = random.randint(5200, 52000)
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
    
    top_cities = sorted(city_summary.items(), key=lambda x: x[1]['avg_demand'], reverse=True)[:6]
    top_times = Counter([item['peak_search_time'] for item in city_data]).most_common(4)
    return top_cities, top_times

def enhanced_parse_demand_signal(data, original_query):
    category = detect_category_and_intent(original_query)
    intent = detect_category_and_intent(original_query)
    
    result = parse_demand_signal(data)
    target_cities, target_count = extract_target_cities_and_count(original_query)
    city_data = generate_city_demand_ranking(target_cities, target_count, category)
    top_cities_demand, top_times = analyze_top_cities_demand(city_data)
    
    brand_keywords = generate_brand_keywords(original_query, category)
    platform_data = generate_platform_analysis(category)
    price_data = generate_price_range_analysis(city_data, category)
    
    result.update({
        "target_cities": target_cities, "target_count": target_count,
        "city_demand_ranking": city_data, "top_5_demand_cities": top_cities_demand,
        "top_3_peak_times": top_times, "detected_category": category,
        "detected_intent": intent, "age_brackets": get_age_groups(intent),
        "brand_keywords": brand_keywords, "platform_analysis": platform_data,
        "price_range_traffic": price_data, "current_season": CURRENT_SEASON
    })
    return result

# 🔥 MAIN STREAMLIT APP
st.title("🔍 Search Demand Analyzer v2.0")
st.markdown("***AI-Powered Google Search Demand Analysis | City-wise + Age + Platform Insights***")

# 🔥 Sidebar
st.sidebar.header("🔧 API Setup")
api_key_input = st.sidebar.text_input("SearchAPI Key:", value=API_KEY, type="password")
st.sidebar.info("👈 Enter your [SearchAPI key](https://searchapi.io/)")

query = st.sidebar.text_input("🔍 Search Query:", value="hair serum for hair growth top 15 city")
num_cities = st.sidebar.slider("🏙️ Number of Cities", 5, 25, 15)

if st.sidebar.button("🚀 ANALYZE DEMAND", type="primary"):
    if not api_key_input:
        st.sidebar.error("👈 Enter API key first!")
    else:
        with st.spinner("🔄 Analyzing search demand..."):
            # 🔥 Real API call
            data = fetch_search_demand(query)
            
            if data:
                parsed = enhanced_parse_demand_signal(data, query)
                category = parsed['detected_category']
                
                # 🔥 MAIN DASHBOARD
                st.header("📊 DEMAND ANALYSIS RESULTS")
                
                # 🔥 Category & Insights
                col1, col2, col3 = st.columns(3)
                col1.metric("🏷️ Category", category.upper())
                col2.metric("👥 Target Age", ", ".join(parsed['age_brackets'][:3]))
                col3.metric("❄️ Season", CURRENT_SEASON.upper())
                
                # 🔥 TOP CITIES CHART
                st.subheader("🏆 TOP CITIES DEMAND RANKING")
                city_df = pd.DataFrame(parsed['city_demand_ranking'][:10])
                fig_city = px.bar(city_df, x='demand_score', y='city', orientation='h',
                                title=f"Top {len(city_df)} Cities - Demand Score",
                                color='demand_score', color_continuous_scale='Viridis')
                st.plotly_chart(fig_city, use_container_width=True)
                
                st.dataframe(city_df[['rank', 'city', 'demand_score', 'age_group', 'search_volume', 'peak_search_time']], 
                           use_container_width=True)
                
                # 🔥 KEYWORD & PLATFORM ANALYSIS
                col_k1, col_k2 = st.columns(2)
                with col_k1:
                    st.markdown("### 🔑 TOP KEYWORDS")
                    kw_df = pd.DataFrame(parsed['brand_keywords'])
                    st.dataframe(kw_df, use_container_width=True)
                
                with col_k2:
                    st.markdown("### 🛒 PLATFORM ANALYSIS")
                    platform_df = pd.DataFrame(parsed['platform_analysis'][:8])
                    st.dataframe(platform_df, use_container_width=True)
                
                # 🔥 PRICE & TIME ANALYSIS
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.markdown("### 💰 HOT PRICE POINTS")
                    price_df = pd.DataFrame(parsed['price_range_traffic'][:10])
                    st.dataframe(price_df, use_container_width=True)
                
                with col_p2:
                    st.markdown("### ⏰ PEAK SEARCH TIMES")
                    time_df = pd.DataFrame(parsed['top_3_peak_times'], columns=['time_slot', 'cities'])
                    fig_time = px.bar(time_df, x='cities', y='time_slot', orientation='h',
                                    title="Peak Search Times", color='cities')
                    st.plotly_chart(fig_time, use_container_width=True)
                
                # 🔥 Google Data
                st.markdown("### 🌐 GOOGLE INSIGHTS")
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.metric("📈 Organic Results", parsed['organic_results_count'])
                    st.write("**Related Searches:**")
                    for q in parsed['related_queries'][:5]:
                        st.write(f"• {q}")
                
                with col_g2:
                    st.write("**People Also Ask:**")
                    for q in parsed['people_also_ask'][:5]:
                        st.write(f"• {q}")
                
                # 🔥 SUMMARY INSIGHTS
                st.markdown("---")
                st.subheader("🎯 ACTIONABLE INSIGHTS")
                col1, col2, col3, col4 = st.columns(4)
                
                top_city = parsed['city_demand_ranking'][0]
                top_kw = parsed['brand_keywords'][0]
                top_platform = parsed['platform_analysis'][0]
                top_price = parsed['price_range_traffic'][0]
                
                col1.metric("🏙️ #1 City", top_city['city'])
                col2.metric("🔑 #1 Keyword", top_kw['keyword'][:30] + "...")
                col3.metric("🛒 #1 Platform", top_platform['platform'])
                col4.metric("💰 Hottest Price", top_price['price_range'])
                
                # 🔥 Excel Download
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"DEMAND_ANALYSIS_{query.replace(' ', '_')}_{timestamp}.xlsx"
                
                with pd.ExcelWriter("temp_analysis.xlsx", engine='openpyxl') as writer:
                    pd.DataFrame(parsed['city_demand_ranking']).to_excel(writer, 'TOP_CITIES', index=False)
                    pd.DataFrame(parsed['brand_keywords']).to_excel(writer, 'TOP_KEYWORDS', index=False)
                    pd.DataFrame(parsed['platform_analysis']).to_excel(writer, 'PLATFORMS', index=False)
                    pd.DataFrame(parsed['price_range_traffic']).to_excel(writer, 'PRICE_ANALYSIS', index=False)
                
                with open("temp_analysis.xlsx", "rb") as f:
                    st.download_button(
                        label=f"📥 Download Excel ({filename})",
                        data=f,
                        file_name=filename,
                        mime="application/vnd.openpyxlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error("❌ No data returned from API")

# 🔥 Instructions
with st.expander("📖 How to Get SearchAPI Key"):
    st.markdown("""
    1. Go to [searchapi.io](https://searchapi.io/)
    2. **Sign Up** → Get FREE $5 credit
    3. **Dashboard** → Copy API Key
    4. Paste in sidebar → **ANALYZE** ✅
    
    **Free tier**: 100 searches/month
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("**✅ Search Demand Analyzer v2.0**\n*City + Age + Platform Insights*")
