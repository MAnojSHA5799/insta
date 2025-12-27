import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random
from datetime import datetime, timedelta
import io
import re

try:
    import openpyxl
    EXCEL_AVAILABLE = True
except:
    EXCEL_AVAILABLE = False

st.set_page_config(page_title="🔍 **SEARCH DATA v52.1**", layout="wide", page_icon="📊")

@st.cache_data
def generate_search_data(query):
    """Generate data based on user search query"""
    query_lower = query.lower()
    
    # Dynamic data based on query
    if any(word in query_lower for word in ['hair', 'serum', 'oil', 'growth', 'fall']):
        categories = ["Hair Serum", "Hair Oil", "Anti Hairfall", "Growth Serum"]
        brands = ["Mamaearth", "Minimalist", "Biotique", "Indulekha", "L'Oreal"]
        products = ['Redensyl Serum', 'Onion Hair Oil', 'Hair Growth Serum']
        cities = ['Kanpur', 'Delhi', 'Lucknow', 'Mumbai']
        
    elif any(word in query_lower for word in ['skin', 'face', 'wash', 'cream', 'sunscreen']):
        categories = ["Face Wash", "Serum", "Moisturizer", "Sunscreen"]
        brands = ["Minimalist", "The Ordinary", "Plum", "Mamaearth"]
        products = ['Vitamin C Serum', 'Niacinamide Serum', 'Salicylic Facewash']
        cities = ['Delhi', 'Bangalore', 'Mumbai']
        
    else:  # Cosmetics
        categories = ["Lipstick", "Kajal", "Foundation"]
        brands = ["Maybelline", "Lakme", "Nykaa", "MAC"]
        products = ['Matte Lipstick', 'Waterproof Kajal']
        cities = ['Mumbai', 'Delhi']
    
    data = []
    for i in range(500):
        data.append({
            'Video_ID': f'VID_{i+1001}',
            'Brand': random.choice(brands),
            'Category': random.choice(categories),
            'Product': random.choice(products),
            'Views': random.randint(8_000, 900_000),
            'Likes': random.randint(300, 40_000),
            'Comments': random.randint(15, 3_000),
            'Shares': random.randint(60, 6_000),
            'Price': random.choice([299, 399, 499, 599, 799]),
            'City': random.choice(cities),
            'State': random.choice(['UP', 'Delhi', 'MH', 'KA']),
            'Sentiment': random.choice(['🟢 Positive', '🟡 Neutral', '🔴 Negative']),
            'Engagement': 0,
            'CTR': 0,
            'Conversion': random.uniform(1.0, 12.0),
            'ROI': 0,
            'Date': datetime(2025, 1, 1) + timedelta(days=random.randint(0, 60))
        })
    
    df = pd.DataFrame(data)
    df['Engagement'] = df['Likes'] + df['Comments'] * 3 + df['Shares'] * 5
    df['CTR'] = (df['Engagement'] / df['Views'] * 100).clip(0, 50)
    df['ROI'] = df['Views'] * df['Conversion'] * 0.02
    return df

# 🔥 MAIN APP - NO RERUN
st.title("🔍 **SEARCH DRIVEN ANALYZER v52.1** 🔥")
st.markdown("***JO SEARCH KARO WO DATA | 500 ROWS | NO ERRORS***")

# 🔥 SEARCH INPUT - FIXED
st.sidebar.header("🔍 **SEARCH QUERY**")
query = st.sidebar.text_input("Enter product:", value="hair growth serum")
generate_btn = st.sidebar.button("🚀 **GENERATE DATA**", type="primary")

if generate_btn or 'df' not in st.session_state:
    with st.spinner("Generating query data..."):
        st.session_state.df = generate_search_data(query)
        st.session_state.query = query

df = st.session_state.get('df', generate_search_data(query))
current_query = st.session_state.get('query', query)

# 🔥 SHOW RESULTS
st.markdown(f"***🔍 Searched: '{current_query}' | 📊 Found: {len(df):,} videos***")

# 🔥 METRICS
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("📹 Videos", f"{len(df):,}")
col2.metric("👁️ Views", f"{df['Views'].sum():,}")
col3.metric("❤️ Likes", f"{df['Likes'].sum():,}")
col4.metric("💰 ROI", f"₹{df['ROI'].sum():,.0f}")
col5.metric("📈 CTR", f"{df['CTR'].mean():.1f}%")
col6.metric("🎯 Conv", f"{df['Conversion'].mean():.1f}%")

st.markdown("─" * 120)

# 🔥 3 GRAPHS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 **1. BRAND WISE**")
    brand_data = df.groupby('Brand', as_index=False)['Views'].sum()
    fig1 = px.bar(brand_data.head(7), x='Brand', y='Views', color='Views')
    fig1.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 🏙️ **2. CITY WISE**")
    city_data = df.groupby('City', as_index=False).agg({
        'Views': 'sum', 'Video_ID': 'count'
    })
    fig2 = px.bar(city_data.head(6), x='City', y='Views')
    fig2.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.markdown("### 💰 **3. PRICE ROI**")
    price_data = df.groupby('Price', as_index=False)['ROI'].sum()
    fig3 = px.bar(price_data, x='Price', y='ROI', color='ROI')
    fig3.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("─" * 120)

# 🔥 DATA TABS
tab1, tab2, tab3 = st.tabs(["🏆 TOP 50", "📊 FULL DATA", "🏅 RANKING"])

with tab1:
    st.markdown("**🏆 TOP 50 VIDEOS**")
    top50 = df.nlargest(50, 'Views')[['Video_ID', 'Brand', 'Product', 'Views', 'ROI', 'City']].round(0)
    st.dataframe(top50, height=600, use_container_width=True)

with tab2:
    st.markdown("**📊 COMPLETE DATA**")
    st.dataframe(df[['Video_ID', 'Brand', 'Category', 'Views', 'Price', 'City', 'CTR', 'ROI']], 
                height=700, use_container_width=True)

with tab3:
    st.markdown("**🏅 BRAND RANKING**")
    ranking = df.groupby('Brand', as_index=False).agg({
        'Views': 'sum', 'ROI': 'sum', 'CTR': 'mean'
    }).round(1).sort_values('Views', ascending=False)
    ranking['Rank'] = range(1, len(ranking)+1)
    st.dataframe(ranking, use_container_width=True)

# 🔥 EXPORT
st.markdown("─" * 120)
if EXCEL_AVAILABLE:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, 'SEARCH_DATA', index=False)
        top50.to_excel(writer, 'TOP_50', index=False)
    st.download_button("📥 **DOWNLOAD DATA**", output.getvalue(), "search_data.xlsx")

st.success(f"✅ **'{current_query}' ANALYSIS COMPLETE | NO ERRORS** 🔥")
