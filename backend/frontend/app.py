import streamlit as st
import requests
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Data Detective - Price Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for premium dark-themed design and modern styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Apply font to elements */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Header style with gradient */
.main-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #FF9900, #FF5500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.subtitle {
    font-size: 1.1rem;
    color: #888888;
    margin-bottom: 2rem;
}

/* Premium Card container */
.product-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(4px);
    margin-bottom: 24px;
}

.product-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 8px;
    line-height: 1.3;
}

.product-meta {
    font-size: 0.9rem;
    color: #aaaaaa;
    margin-bottom: 16px;
}

.price-container {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 12px;
}

.current-price {
    font-size: 2rem;
    font-weight: 700;
    color: #FF9900;
}

.mrp-price {
    font-size: 1.2rem;
    text-decoration: line-through;
    color: #888888;
}

.discount-badge {
    background: rgba(255, 85, 0, 0.2);
    color: #FF5500;
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.85rem;
}

.rating-badge {
    background: rgba(255, 153, 0, 0.15);
    color: #FF9900;
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.85rem;
    display: inline-block;
}

.metric-card {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 8px;
    padding: 16px;
    border-left: 4px solid #FF9900;
    margin-top: 12px;
}

.metric-label {
    font-size: 0.8rem;
    color: #888888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: 1.3rem;
    font-weight: 600;
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Data Detective</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time Amazon Price & Review Tracking Engine</div>', unsafe_allow_html=True)

# API Base URL
API_BASE = "http://localhost:8000"

# --- Scrape new product section ---
with st.expander("🔍 Track New Product", expanded=False):
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        new_url = st.text_input("Amazon Product URL", placeholder="https://www.amazon.in/...", label_visibility="collapsed")
    with col_btn:
        scrape_btn = st.button("Start Scraping", use_container_width=True)
    
    if scrape_btn and new_url:
        with st.spinner("Scraping product details..."):
            try:
                res = requests.post(f"{API_BASE}/api/scrape/", json={"url": new_url})
                if res.status_code == 200:
                    data = res.json()
                    if data.get("success"):
                        st.success(f"Successfully tracked: {data['data'].get('name', 'Product')}")
                    else:
                        st.error(f"Failed to scrape: {data.get('message', 'Unknown error')}")
                else:
                    st.error(f"Server returned status code {res.status_code}")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

# --- Fetch products first ---
try:
    products_res = requests.get(f"{API_BASE}/api/")
    if products_res.status_code == 200:
        products = products_res.json().get("data", [])
    else:
        products = []
        st.error("Failed to load products list from database.")
except Exception as e:
    products = []
    st.error(f"Could not connect to backend API: {e}")

st.divider()

if not products:
    st.info("No tracked products found. Enter a URL above to start tracking.")
else:
    # Build a lookup map of product_name -> product object
    product_map = {f"{p['name'][:70]}... ({p['seller_company'] or 'Unknown Brand'})": p for p in products}
    
    col_select, col_rescrape = st.columns([3, 1])
    with col_select:
        selected_display = st.selectbox("Select a Product to View History", list(product_map.keys()))
    with col_rescrape:
        st.write("") # spacing
        st.write("") # spacing
        if st.button("🔄 Sync/Rescrape All Products", use_container_width=True):
            with st.spinner("Requesting data sync..."):
                try:
                    sync_res = requests.get(f"{API_BASE}/api/scrape/all")
                    if sync_res.status_code == 200:
                        st.toast("Sync triggered successfully! Snapshots will be recorded.", icon="🚀")
                    else:
                        st.error("Failed to trigger sync.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # The selected product object
    selected_prod = product_map[selected_display]
    selected_id = selected_prod["id"]

    # --- Fetch snapshots and combine them with the initial product data ---
    try:
        snapshots_res = requests.get(f"{API_BASE}/api/snapshot/")
        if snapshots_res.status_code == 200:
            all_snapshots = snapshots_res.json().get("data", [])
        else:
            all_snapshots = []
    except Exception as e:
        all_snapshots = []
        st.error(f"Could not fetch snapshots: {e}")

    # Filter snapshots for the selected product
    product_snapshots = [s for s in all_snapshots if s["product_id"] == selected_id]

    # Combine initial product data point (created_at) and subsequent snapshots
    history = []
    
    # 1. Add the initial scraped state from the product table
    history.append({
        "scraped_at": pd.to_datetime(selected_prod["created_at"]),
        "price": float(selected_prod["price"]) if selected_prod["price"] is not None else None,
        "mrp": float(selected_prod["mrp"]) if selected_prod["mrp"] is not None else None,
        "discount_percentage": float(selected_prod["discount_percentage"]) if selected_prod["discount_percentage"] is not None else 0.0,
        "review_score": float(selected_prod["review_score"]) if selected_prod["review_score"] is not None else None,
        "review_count": int(selected_prod["review_count"]) if selected_prod["review_count"] is not None else 0,
        "source": "Initial Scrape"
    })

    # 2. Add snapshots
    for snap in product_snapshots:
        history.append({
            "scraped_at": pd.to_datetime(snap["scraped_at"]),
            "price": float(snap["price"]) if snap["price"] is not None else None,
            "mrp": float(snap["mrp"]) if snap["mrp"] is not None else None,
            "discount_percentage": float(snap["discount_percentage"]) if snap["discount_percentage"] is not None else 0.0,
            "review_score": float(snap["review_score"]) if snap["review_score"] is not None else None,
            "review_count": int(snap["review_count"]) if snap["review_count"] is not None else 0,
            "source": "Snapshot"
        })

    # Create sorted DataFrame
    df_history = pd.DataFrame(history)
    df_history = df_history.sort_values("scraped_at")

    # --- Render Beautiful Product Card ---
    col_img, col_info = st.columns([1, 3])
    
    with col_img:
        if selected_prod.get("image_url"):
            st.image(selected_prod["image_url"], width='stretch')
        else:
            st.info("No image available")
            
    with col_info:
        # Determine latest price info
        latest_price = df_history["price"].iloc[-1]
        latest_mrp = df_history["mrp"].iloc[-1]
        latest_discount = df_history["discount_percentage"].iloc[-1]
        latest_rating = df_history["review_score"].iloc[-1]
        latest_reviews = df_history["review_count"].iloc[-1]
        currency_sym = selected_prod.get("currency") or "₹"

        # HTML/CSS Card for metadata details
        st.markdown(f"""
        <div class="product-card">
            <div class="product-title">{selected_prod["name"]}</div>
            <div class="product-meta">
                <b>Brand:</b> {selected_prod["seller_company"] or "Unknown"} | 
                <b>Platform:</b> {selected_prod["source"].capitalize()} | 
                <a href="{selected_prod["product_url"]}" target="_blank">View on Store ↗</a>
            </div>
            <div class="price-container">
                <span class="current-price">{currency_sym}{latest_price:,.2f}</span>
                {f'<span class="mrp-price">{currency_sym}{latest_mrp:,.2f}</span>' if latest_mrp else ''}
                {f'<span class="discount-badge">{latest_discount:.0f}% OFF</span>' if latest_discount else ''}
            </div>
            <div style="margin-top: 8px;">
                <span class="rating-badge">⭐ {latest_rating or '0.0'} ({latest_reviews:,} reviews)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- Plotting Section ---
    st.subheader("📈 Historical Trends (Initial Scrape + Snapshots)")
    
    # We set index to scraped_at for time-series charts
    df_chart = df_history.copy().set_index("scraped_at")
    
    tab1, tab2, tab3 = st.tabs(["💰 Price History", "⭐ Review Score", "👥 Review Count"])
    
    with tab1:
        st.markdown("**Price & MRP Trend Over Time**")
        price_cols = ["price"]
        if "mrp" in df_chart.columns and df_chart["mrp"].notna().any():
            price_cols.append("mrp")
        st.line_chart(df_chart[price_cols])
        
    with tab2:
        st.markdown("**Average Review Rating Trend**")
        st.line_chart(df_chart["review_score"])
        
    with tab3:
        st.markdown("**Total Review Count Trend**")
        st.line_chart(df_chart["review_count"])

    # Show raw historical data table under expander
    with st.expander("📋 View Raw History Log"):
        st.dataframe(
            df_history.rename(columns={
                "scraped_at": "Timestamp",
                "price": "Price",
                "mrp": "MRP",
                "discount_percentage": "Discount (%)",
                "review_score": "Rating",
                "review_count": "Reviews Count",
                "source": "Record Type"
            }).sort_values("Timestamp", ascending=False),
            use_container_width=True
        )