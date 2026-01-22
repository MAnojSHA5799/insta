# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# import re
# import random
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# def create_session():
#     """Create robust session with retry strategy"""
#     session = requests.Session()
#     retry_strategy = Retry(
#         total=3,
#         backoff_factor=1,
#         status_forcelist=[403, 429, 500, 502, 503, 504]
#     )
#     adapter = HTTPAdapter(max_retries=retry_strategy)
#     session.mount("http://", adapter)
#     session.mount("https://", adapter)
#     return session

# def get_rotating_headers():
#     """Rotate realistic browser headers"""
#     user_agents = [
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
#     ]
    
#     headers = {
#         'User-Agent': random.choice(user_agents),
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'none',
#         'Sec-Fetch-User': '?1',
#         'Cache-Control': 'no-cache',
#         'Pragma': 'no-cache'
#     }
#     return headers

# def scrape_bihar_events(url):
#     session = create_session()
    
#     # Special handling for blocked sites
#     if any(blocked in url.lower() for blocked in ['bookmyshow', '10times']):
#         # Visit homepage first + longer delay
#         try:
#             homepage = 'https://in.bookmyshow.com/' if 'bookmyshow' in url else 'https://10times.com/'
#             session.get(homepage, headers=get_rotating_headers(), timeout=10)
#             time.sleep(random.uniform(3, 5))
#         except:
#             pass
    
#     headers = get_rotating_headers()
#     session.headers.update(headers)
    
#     for attempt in range(3):  # 3 retries
#         try:
#             response = session.get(url, timeout=20)
            
#             if response.status_code == 403:
#                 print(f"🔄 403 detected on attempt {attempt+1}, rotating headers...")
#                 time.sleep(random.uniform(5, 8))
#                 continue
#             elif response.status_code == 429:
#                 print("⏳ Rate limited, waiting 10s...")
#                 time.sleep(10)
#                 continue
                
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             events = []
            
#             # BookMyShow pattern
#             if 'bookmyshow' in url.lower():
#                 cards = soup.find_all('a', class_=re.compile(r'sc-133848s-11|sc-1ljcxl3'))
#                 for card in cards[:15]:
#                     title = card.find(['h3', '.elfplV'])
#                     title = title.get_text(strip=True) if title else None
                    
#                     if title and len(title) > 3:
#                         venue = card.find('.FnmcD')
#                         venue = venue.get_text(strip=True) if venue else 'Patna'
                        
#                         cats = card.find_all('.bsZIkT')
#                         category = cats[0].get_text(strip=True) if cats else 'Event'
#                         price = cats[-1].get_text(strip=True) if len(cats) > 1 else 'N/A'
                        
#                         events.append({
#                             'Event': title[:100],
#                             'Date': 'Jan-Feb 2026',
#                             'Venue': venue,
#                             'Category': category,
#                             'Price': price,
#                             'Source': url
#                         })
                        
#             # Generic conference parsing  
#             else:
#                 rows = soup.find_all(['div', 'tr', 'li'], class_=re.compile(r'(conf|event|listing|card)', re.I))
#                 for row in rows[:50]:
#                     title_elem = row.find(['h3', 'h4', 'h2', 'a'])
#                     title = title_elem.get_text(strip=True) if title_elem else None
                    
#                     if title and len(title) > 3 and len(title) < 100:
#                         # Filter out country names (your issue)
#                         if any(country in title.lower() for country in ['algeria', 'azerbaijan', 'andorra', 'bahamas']):
#                             continue
                            
#                         events.append({
#                             'Event': title[:100],
#                             'Date': '2026',
#                             'Venue': 'Bihar/Patna',
#                             'Category': 'Conference/Event',
#                             'Price': 'N/A',
#                             'Source': url
#                         })
            
#             print(f"✅ {len(events)} events from {url}")
#             return pd.DataFrame(events)
            
#         except Exception as e:
#             print(f"⚠️ Attempt {attempt+1} failed: {str(e)[:50]}")
#             time.sleep(random.uniform(2, 4))
    
#     print(f"❌ FAILED after 3 attempts: {url}")
#     return pd.DataFrame()

# # ALL YOUR WORKING URLS (removed broken ones)
# urls = [
#     # Conferences (your best sources - 400+ events!)
#     'https://conferencealerts.co.in/bihar',
#     'https://conferencealerts.co.in/bihar/business', 
#     'https://conferencealerts.co.in/bihar/engineering',
#     'https://conferencealerts.co.in/bihar/medical',
#     'https://www.allconferencealert.com/bihar.html',
#     'https://allconferencealert.net/bihar.php',
    
#     # Government (282 events from tourism!)
#     'https://tourism.bihar.gov.in/en/events',
#     'https://betastate.bihar.gov.in/fairs',
    
#     # Working aggregators
#     'https://www.eventalways.com/india/bihar',
#     'https://factohr.com/holiday-list-in-india/bihar/'
# ]

# print("🚀 FIXED Scraping - 500+ Events Expected!")
# all_events = []
# for i, url in enumerate(urls, 1):
#     print(f"\n[{i}/{len(urls)}] Scraping: {url}")
#     df = scrape_bihar_events(url)
#     if not df.empty:
#         all_events.append(df)
#     time.sleep(random.uniform(2, 4))  # Human-like delays

# # Clean & Save
# if all_events:
#     combined_df = pd.concat(all_events, ignore_index=True)
    
#     # Remove country names & duplicates
#     bad_countries = ['algeria', 'azerbaijan', 'andorra', 'bahamas', 'australia']
#     clean_df = combined_df[
#         ~combined_df['Event'].str.contains('|'.join(bad_countries), case=False, na=False)
#     ].drop_duplicates(subset=['Event']).dropna(subset=['Event'])
    
#     clean_df.to_csv('bihar_clean_events_2026.csv', index=False)
#     print(f"\n🎉 SUCCESS: {len(clean_df)} CLEAN EVENTS SAVED!")
#     print("\n📋 CLEAN SAMPLE:")
#     print(clean_df[['Event', 'Venue', 'Category']].head(10))
# else:
#     print("No events found.")



import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import plotly.express as px

# Streamlit page config
st.set_page_config(
    page_title="Bihar Events Scraper 2026",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)  
def create_session():
    """Create robust session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[403, 429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def get_rotating_headers():
    """Rotate realistic browser headers - Updated for 2026"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }
    return headers

@st.cache_data(ttl=1800)
def scrape_bihar_events(url):
    session = create_session()
    
    if any(blocked in url.lower() for blocked in ['bookmyshow', '10times']):
        try:
            homepage = 'https://in.bookmyshow.com/' if 'bookmyshow' in url else 'https://10times.com/'
            session.get(homepage, headers=get_rotating_headers(), timeout=10)
            time.sleep(random.uniform(3, 5))
        except:
            pass
    
    headers = get_rotating_headers()
    session.headers.update(headers)
    
    for attempt in range(3):
        try:
            response = session.get(url, timeout=20)
            
            if response.status_code == 403:
                time.sleep(random.uniform(5, 8))
                continue
            elif response.status_code == 429:
                time.sleep(10)
                continue
                
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            events = []
            
            if 'bookmyshow' in url.lower():
                cards = soup.find_all('a', class_=re.compile(r'sc-133848s-11|sc-1ljcxl3|event-card'))
                for card in cards[:15]:
                    title = card.find(['h3', '.elfplV', '[data-testid="event-title"]'])
                    title = title.get_text(strip=True) if title else None
                    
                    if title and len(title) > 3:
                        venue = card.find(['.FnmcD', '.venue-name', '[data-testid="event-venue"]'])
                        venue = venue.get_text(strip=True) if venue else 'Patna'
                        
                        cats = card.find_all(['.bsZIkT', '.category-tag'])
                        category = cats[0].get_text(strip=True) if cats else 'Event'
                        price = cats[-1].get_text(strip=True) if len(cats) > 1 else 'N/A'
                        
                        events.append({
                            'Event': title[:100],
                            'Date': 'Jan-Feb 2026',
                            'Venue': venue[:50],
                            'Category': category,
                            'Price': price,
                            'Source': url
                        })
            else:
                rows = soup.find_all(['div', 'tr', 'li', '.event-item'], 
                                   class_=re.compile(r'(conf|event|listing|card|upcoming)', re.I))
                for row in rows[:50]:
                    title_elem = row.find(['h1','h2','h3', 'h4', '.event-title', '.conf-title'])
                    title = title_elem.get_text(strip=True) if title_elem else None
                    
                    if title and len(title) > 3 and len(title) < 100:
                        bad_countries = ['algeria', 'azerbaijan', 'andorra', 'bahamas', 'australia']
                        if any(country in title.lower() for country in bad_countries):
                            continue
                            
                        date_elem = row.find(['.date', '.event-date', '[datetime]'])
                        date = date_elem.get_text(strip=True) if date_elem else '2026'
                        
                        events.append({
                            'Event': title[:100],
                            'Date': date[:20],
                            'Venue': 'Bihar/Patna',
                            'Category': 'Conference/Event',
                            'Price': 'N/A',
                            'Source': url
                        })
            
            return pd.DataFrame(events)
            
        except Exception as e:
            time.sleep(random.uniform(2, 4))
    
    return pd.DataFrame()

# Main Streamlit App
st.title("🎉 Bihar Events Scraper 2026")
st.markdown("---")

# Sidebar controls
st.sidebar.header("⚙️ Configuration")
max_sources = st.sidebar.slider("Max sources to scrape", 1, 10, 5)

urls = [
    'https://conferencealerts.co.in/bihar',
    'https://conferencealerts.co.in/bihar/business', 
    'https://conferencealerts.co.in/bihar/engineering',
    'https://www.allconferencealert.com/bihar.html',
    'https://tourism.bihar.gov.in/en/events',
    'https://www.eventalways.com/india/bihar'
][:max_sources]

progress_bar = st.progress(0)
status_text = st.empty()

if st.button("🚀 Start Scraping", type="primary"):
    with st.spinner("Scraping Bihar events..."):
        all_events = []
        total_urls = len(urls)
        
        for i, url in enumerate(urls):
            status_text.text(f"[{i+1}/{total_urls}] Scraping: {url}")
            progress_bar.progress((i + 1) / total_urls)
            
            df = scrape_bihar_events(url)
            if not df.empty:
                all_events.append(df)
            
            time.sleep(random.uniform(1, 3))
        
        if all_events:
            combined_df = pd.concat(all_events, ignore_index=True)
            
            bad_countries = ['algeria', 'azerbaijan', 'andorra', 'bahamas', 'australia']
            mask = combined_df['Event'].str.contains('|'.join(bad_countries), case=False, na=False)
            clean_df = combined_df[~mask].drop_duplicates(subset=['Event']).dropna(subset=['Event'])
            
            st.session_state.events_df = clean_df
            st.session_state.last_updated = pd.Timestamp.now()
            
            st.success(f"🎉 {len(clean_df)} clean events scraped!")
            status_text.text(f"✅ Complete: {len(clean_df)} events")
        else:
            st.warning("No events found.")
            status_text.text("❌ No events found")

# FIXED DISPLAY SECTION - TABLE WILL SHOW NOW!
if 'events_df' in st.session_state:
    df = st.session_state.events_df
    
    # Check if DataFrame actually has data
    if not df.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.metric("Total Events", len(df))
            st.metric("Unique Sources", df['Source'].nunique())
        
        with col2:
            st.metric("Last Updated", st.session_state.last_updated.strftime("%d %b %Y, %H:%M"))
        
        st.markdown("---")
        
        # FIXED FILTERS - Convert to list first
        categories = sorted(df['Category'].unique().tolist())
        venues = sorted(df['Venue'].unique()[:10].tolist())
        
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.multiselect("Filter Category", 
                                           options=categories,
                                           default=categories[:1] if categories else [])
        with col2:
            venue_filter = st.multiselect("Filter Venue", 
                                        options=venues,
                                        default=venues[:1] if venues else [])
        
        # Safe filtering
        filtered_df = df.copy()
        if category_filter:
            filtered_df = filtered_df[filtered_df['Category'].isin(category_filter)]
        if venue_filter:
            filtered_df = filtered_df[filtered_df['Venue'].isin(venue_filter)]
        
        # MAIN TABLE - Always shows!
        st.subheader("📋 Events List")
        st.dataframe(filtered_df[['Event', 'Date', 'Venue', 'Category', 'Price']],
                    use_container_width=True, height=400)
        
        # Download
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"bihar_events_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
            mime='text/csv'
        )
        
        # Charts
        if len(filtered_df) > 0:
            st.subheader("📊 Analytics")
            col1, col2 = st.columns(2)
            
            with col1:
                cat_counts = filtered_df['Category'].value_counts()
                if len(cat_counts) > 0:
                    fig_cat = px.bar(x=cat_counts.index, y=cat_counts.values, 
                                   title="Events by Category")
                    st.plotly_chart(fig_cat, use_container_width=True)
            
            with col2:
                venue_counts = filtered_df['Venue'].value_counts().head(10)
                if len(venue_counts) > 0:
                    fig_venue = px.pie(values=venue_counts.values, names=venue_counts.index,
                                      title="Top Venues")
                    st.plotly_chart(fig_venue, use_container_width=True)
    else:
        st.warning("📭 No events data available. Click 'Start Scraping' first!")
else:
    st.info("👆 Click 'Start Scraping' to collect Bihar events data!")
    st.markdown("**Expected:** 200-500+ events from multiple sources")

st.markdown("---")
st.markdown("*Bihar Events Tracker | Fixed Jan 2026*")
