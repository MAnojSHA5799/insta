import streamlit as st
import json
import pandas as pd
import random

# ------------------------
# Load JSON
# ------------------------
with open("product_intelligence.json", "r") as f:
    data = json.load(f)

st.set_page_config("YouTube Product Intelligence", layout="wide")
st.title("📊 YouTube Product Intelligence Tool (Search Mode)")

# ------------------------
# Select Category and Product Type
# ------------------------
category = st.selectbox("Select Category", list(data.keys()))
sub_category_list = list(data[category].keys())
search_query = st.text_input("Search Product/Sub-Category").lower()

# Filter sub-categories based on search
filtered_sub_categories = [sc for sc in sub_category_list if search_query in sc.lower()]

if filtered_sub_categories:
    sub_category = filtered_sub_categories[0]  # Take first match
    base = data[category][sub_category]

    st.markdown(f"### 🔍 Showing Data for: **{sub_category.title()}**")

    # ------------------------
    # AGE GROUP TABLE
    # ------------------------
    st.subheader("👥 Age Group Wise Search Data")
    age_df = pd.DataFrame({
        "Age Group": list(base["age_group_search"].keys()),
        "Search Volume": [v + random.randint(-5, 10) for v in base["age_group_search"].values()]
    })
    st.dataframe(age_df)

    # ------------------------
    # INGREDIENT TABLE
    # ------------------------
    st.subheader("🧪 Ingredient Usage Data")
    ingredient_df = pd.DataFrame({
        "Ingredient": base["ingredients"],
        "Usage Score": [random.randint(60, 100) for _ in base["ingredients"]]
    })
    st.dataframe(ingredient_df)

    # ------------------------
    # KEYWORD TABLE
    # ------------------------
    st.subheader("🔥 Top Hookups & Keywords")
    keyword_df = pd.DataFrame({
        "Keyword": base["top_hookups_keywords"],
        "Search Trend Score": [random.randint(50, 100) for _ in base["top_hookups_keywords"]]
    })
    st.dataframe(keyword_df)

    # ------------------------
    # PEAK TIME TABLE
    # ------------------------
    st.subheader("⏰ Peak Search Time Data")
    peak_df = pd.DataFrame({
        "Time Slot": base["peak_times"],
        "Traffic Index": [random.randint(60, 120) for _ in base["peak_times"]]
    })
    st.dataframe(peak_df)

    # ------------------------
    # PRICE ANALYSIS TABLE
    # ------------------------
    st.subheader("💰 Price Analysis")
    price_df = pd.DataFrame({
        "Min Price": [base["price_analysis"]["min_price"] + random.randint(-20, 50)],
        "Avg Price": [base["price_analysis"]["average_price"] + random.randint(-50, 50)],
        "Max Price": [base["price_analysis"]["max_price"] + random.randint(-50, 100)]
    })
    st.dataframe(price_df)

    # ------------------------
    # CITY DEMAND TABLE
    # ------------------------
    st.subheader("📍 City Wise Demand")
    city_df = pd.DataFrame({
        "City": list(base["city_demand"].keys()),
        "Demand Index": [v + random.randint(-5, 10) for v in base["city_demand"].values()]
    })
    st.dataframe(city_df)

    # ------------------------
    # PRODUCT RANKING TABLE
    # ------------------------
    st.subheader("🏆 Live Product Ranking")
    product_names = [p["name"] for p in base.get("products", [{"name": sub_category.title() + " Variant"}])]
    product_df = pd.DataFrame({
        "Product Name": product_names,
        "Price": [p.get("price", base["price_analysis"]["average_price"]) for p in base.get("products", [{} for _ in product_names])],
        "Rank": list(range(1, len(product_names)+1))
    })
    st.dataframe(product_df)

else:
    st.info("Type product/sub-category in the search box to display data.")
