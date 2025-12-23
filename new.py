import streamlit as st
import requests
import json
import re
import time
from collections import Counter
from datetime import datetime
from urllib.parse import quote
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="YouTube Recent Analyzer", layout="wide", page_icon="📺")

API_KEY = 'AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4'
BRAND_KEYWORDS = ['loreal', 'maybelline', 'lakme', 'mamaearth', 'nykaa', 'plum']

INDIA_CITIES = {
    'kanpur': 'Uttar Pradesh', 'lucknow': 'Uttar Pradesh', 'noida': 'Uttar Pradesh', 
    'agra': 'Uttar Pradesh', 'varanasi': 'Uttar Pradesh', 'allahabad': 'Uttar Pradesh',
    'ghaziabad': 'Uttar Pradesh', 'meerut': 'Uttar Pradesh', 'bareilly': 'Uttar Pradesh',
    'mumbai': 'Maharashtra', 'pune': 'Maharashtra', 'nagpur': 'Maharashtra',
    'bangalore': 'Karnataka', 'mysore': 'Karnataka', 'delhi': 'Delhi',
    'chennai': 'Tamil Nadu', 'hyderabad': 'Telangana', 'kolkata': 'West Bengal',
    'ahmedabad': 'Gujarat', 'jaipur': 'Rajasthan', 'kochi': 'Kerala'
}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def safe_api_call(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if 'error' in data:
                time.sleep(2)
                continue
            return data
        except:
            time.sleep(1)
    return None

def is_recent_video(published_date_str):
    try:
        pub_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
        cutoff_date = datetime(2024, 12, 1)
        return pub_date >= cutoff_date
    except:
        return False

def search_keyword_multi_region(query):
    worldwide_ids = set()
    india_ids = set()
    
    # WORLDWIDE
    regions = ['US', 'GB', 'IN', 'CA', 'AU', 'DE', 'FR']
    for region in regions:
        published_after = "2024-12-01T00:00:00Z"
        url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={quote(query)}&type=video&maxResults=30&order=date&publishedAfter={published_after}&regionCode={region}&key={API_KEY}"
        data = safe_api_call(url)
        if data and 'items' in data:
            for item in data['items']:
                worldwide_ids.add(item['id']['videoId'])
        time.sleep(0.3)
    
    # INDIA
    for mode in ['date', 'viewCount', 'relevance']:
        url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={quote(query)}&type=video&maxResults=50&order={mode}&publishedAfter=2024-12-01T00:00:00Z&regionCode=IN&key={API_KEY}"
        data = safe_api_call(url)
        if data and 'items' in data:
            for item in data['items']:
                india_ids.add(item['id']['videoId'])
        time.sleep(0.3)
    
    return {'worldwide': list(worldwide_ids), 'india': list(india_ids)}

@st.cache_data(ttl=3600)
def get_full_video_details(video_ids, region_label=""):
    all_videos = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={','.join(batch)}&key={API_KEY}"
        data = safe_api_call(url)
        
        if data and 'items' in data:
            for item in data['items']:
                try:
                    published_date = item['snippet'].get('publishedAt', '')
                    if not is_recent_video(published_date):
                        continue
                    
                    video = {
                        'Video_ID': item['id'],
                        'Title': item['snippet'].get('title', ''),
                        'Channel': item['snippet'].get('channelTitle', ''),
                        'Description': item['snippet'].get('description', '')[:400],
                        'Published': published_date,
                        'Published_Date': datetime.fromisoformat(published_date.replace('Z', '+00:00')).strftime('%Y-%m-%d'),
                        'Views': int(item['statistics'].get('viewCount', 0)),
                        'Likes': int(item['statistics'].get('likeCount', 0)),
                        'Comments': int(item['statistics'].get('commentCount', 0)),
                        'Duration': item['contentDetails'].get('duration', 'PT0S'),
                        'Video_URL': f"https://youtu.be/{item['id']}",
                        'Region': region_label,
                        'City': 'Other',
                        'State': 'Other',
                        'Is_Recent': 'YES'
                    }
                    
                    duration_match = re.search(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', video['Duration'])
                    if duration_match:
                        h, m, s = duration_match.groups()
                        total_sec = int(h or 0)*3600 + int(m or 0)*60 + int(s or 0)
                        video['Duration_Formatted'] = f"{total_sec//60}m {total_sec%60}s"
                    else:
                        video['Duration_Formatted'] = '0s'
                    
                    all_videos.append(video)
                except:
                    continue
        time.sleep(0.5)
    
    return all_videos

def detect_cities_states(videos):
    city_counter = Counter()
    state_counter = Counter()
    
    for video in videos:
        text_lower = (video['Title'] + ' ' + video['Description']).lower()
        detected_city = None
        
        for city_key, state in INDIA_CITIES.items():
            if city_key in text_lower:
                detected_city = city_key.title()
                video['City'] = detected_city
                video['State'] = state
                city_counter[detected_city] += 1
                state_counter[state] += 1
                break
        
        if not detected_city:
            video['City'] = 'Other'
            video['State'] = 'Other'
    
    return videos, city_counter, state_counter

# Streamlit App
st.title("🚀 YouTube Recent Analyzer v26.0")
st.markdown("📅 **DEC 2024 → TODAY** | 🌍 Worldwide + 🇮🇳 India Cities | 📊 Live Dashboard")

# Sidebar
st.sidebar.header("⚙️ Settings")
query = st.sidebar.text_input("🔍 Search Keyword", value="lip-bam")
if st.sidebar.button("🚀 ANALYZE", type="primary"):
    st.sidebar.success("Analyzing...")

# Main content
col1, col2 = st.columns([2, 1])

if query:
    with st.spinner("🔍 Searching recent videos..."):
        # Get data
        region_data = search_keyword_multi_region(query)
        worldwide_videos = get_full_video_details(region_data['worldwide'], "Worldwide")
        india_videos = get_full_video_details(region_data['india'], "India")
        
        if worldwide_videos or india_videos:
            india_with_cities, city_counter, state_counter = detect_cities_states(india_videos)
            
            # Metrics
            total_ww = len(worldwide_videos)
            total_in = len(india_videos)
            total_views_ww = sum(v['Views'] for v in worldwide_videos)
            total_views_in = sum(v['Views'] for v in india_videos)
            
            with col1:
                st.metric("🌍 Worldwide Videos", f"{total_ww:,}")
                st.metric("🇮🇳 India Videos", f"{total_in:,}")
                st.metric("👀 Worldwide Views", f"{total_views_ww:,}")
                st.metric("👀 India Views", f"{total_views_in:,}")
            
            with col2:
                st.metric("🏙️ Cities Found", len(city_counter))
                st.metric("🌟 States Found", len(state_counter))
            
            # Charts
            st.subheader("📊 Live Dashboard")
            
            # Row 1: Views + Top Cities
            col1, col2 = st.columns(2)
            
            with col1:
                # Top Worldwide Videos
                top_ww = sorted(worldwide_videos, key=lambda x: x['Views'], reverse=True)[:10]
                df_top = pd.DataFrame(top_ww)[['Title', 'Views', 'Likes', 'Published_Date', 'Video_URL']]
                st.dataframe(df_top, use_container_width=True)
            
            with col2:
                # City Ranking
                if city_counter:
                    city_df = pd.DataFrame(city_counter.most_common(10), 
                                         columns=['City', 'Videos']).sort_values('Videos', ascending=False)
                    fig_city = px.bar(city_df, x='Videos', y='City', orientation='h',
                                    title="🏙️ Top Cities", color='Videos', color_continuous_scale='Viridis')
                    st.plotly_chart(fig_city, use_container_width=True)
            
            # Row 2: India Map + State Ranking
            col1, col2 = st.columns(2)
            
            with col1:
                # State Ranking
                state_df = pd.DataFrame(state_counter.most_common(10), 
                                      columns=['State', 'Videos']).sort_values('Videos', ascending=False)
                fig_state = px.bar(state_df, x='Videos', y='State', orientation='h',
                                 title="🌟 Top States", color='Videos')
                st.plotly_chart(fig_state, use_container_width=True)
            
            with col2:
                # Views Distribution
                if worldwide_videos:
                    views_data = pd.DataFrame(worldwide_videos)
                    fig_views = px.histogram(views_data, x='Views', nbins=20,
                                           title="👀 Views Distribution",
                                           labels={'Views': 'Total Views'})
                    st.plotly_chart(fig_views, use_container_width=True)
            
            # Excel Download
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{query.upper().replace('-', '_')}_RECENT_{timestamp}.xlsx"
            
            india_df = pd.DataFrame(india_with_cities)
            ww_df = pd.DataFrame(worldwide_videos)
            
            with pd.ExcelWriter('temp.xlsx', engine='openpyxl') as writer:
                ww_df.to_excel(writer, '🌍RECENT_WORLDWIDE', index=False)
                india_df.to_excel(writer, '🇮🇳RECENT_INDIA', index=False)
                
                # City summary
                city_summary = india_df[india_df['City'] != 'Other'].groupby(['City', 'State']).agg({
                    'Views': 'sum', 'Video_ID': 'count'
                }).reset_index()
                city_summary.columns = ['City', 'State', 'Total_Views', 'Videos']
                city_summary.to_excel(writer, '🏙️CITY_RANKING', index=False)
            
            with open('temp.xlsx', 'rb') as f:
                st.download_button(
                    label="💾 Download Excel",
                    data=f.read(),
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            # Raw Data
            with st.expander("📋 View Raw Data"):
                st.dataframe(ww_df, use_container_width=True)
        else:
            st.warning("❌ No recent videos found (Dec 2024-Today)")
else:
    st.info("👈 Enter keyword in sidebar to start analysis!")

st.sidebar.markdown("---")
st.sidebar.caption("📅 Dec 2024 → Today | 🚀 v26.0")
