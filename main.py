import streamlit as st
from src.services import scrape_and_store_product, fetch_and_store_competitors
from src.db import Database
from src.llm import analyze_competitors

# Custom CSS for better styling
def apply_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .product-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            transition: transform 0.2s;
        }
        .product-card:hover {
            transform: translateY(-5px);
        }
        .metric-container {
            background: #f8f9fa;
            padding: 0.5rem;
            border-radius: 5px;
            text-align: center;
        }
        .competitor-section {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
        }
        .input-section {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div class="main-header">
            <h1>Price Radar</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">Enter your ASIN to get detailed product insights and competitor analysis</p>
        </div>
    """, unsafe_allow_html=True)

def render_inputs():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    cols = st.columns([2, 1, 1])
    
    with cols[0]:
        asin = st.text_input("ASIN", placeholder="e.g., B0CX23VSAS", 
                            help="Enter the Amazon Standard Identification Number")
    
    with cols[1]:
        geo = st.text_input("Zip/Postal Code", placeholder="e.g., 83980",
                           help="Enter your location for accurate pricing")
    
    with cols[2]:
        domain = st.selectbox("Amazon Domain", [
            "com", "ca", "co.uk", "de", "fr", "it", "ae", "in"
        ], help="Select the Amazon marketplace domain")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return asin.strip(), geo.strip(), domain

def render_product_card(product):
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    cols = st.columns([1, 2])

    try:
        images = product.get("images", [])
        if images and len(images) > 0:
            cols[0].image(images[0], width=200, use_column_width=True)
        else:
            cols[0].info("No image available")
    except:
        cols[0].warning("Error loading image")

    with cols[1]:
        st.markdown(f"### {product.get('title') or product['asin']}")
        
        info_cols = st.columns(3)
        with info_cols[0]:
            currency = product.get("currency", "")
            price = product.get("price", "-")
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Price", f"{currency} {price}" if currency else price)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with info_cols[1]:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Brand", product.get('brand', '-'))
            st.markdown('</div>', unsafe_allow_html=True)
            
        with info_cols[2]:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Product ID", product.get('product', '-'))
            st.markdown('</div>', unsafe_allow_html=True)

        domain_info = f"amazon.{product.get('amazon_domain', 'com')}"
        geo_info = product.get("geo_location", "-")
        st.caption(f"📍 {geo_info} | 🌐 {domain_info}")

        st.markdown(f"[View on Amazon]({product.get('url', '')})")
        
        st.button("🔍 Analyze Competitors", 
                 key=f"analyze_{product['asin']}", 
                 type="primary",
                 on_click=lambda: setattr(st.session_state, "analyzing_asin", product["asin"]))
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Amazon Competitor Analysis",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_custom_css()
    render_header()
    asin, geo, domain = render_inputs()

    if st.button("🔎 Scrape Product", type="primary") and asin:
        with st.spinner("🔄 Scraping product details..."):
            scrape_and_store_product(asin, geo, domain)
        st.success("✅ Product scraped successfully!")

    db = Database()
    products = db.get_all_products()
    if products:
        st.markdown("---")
        st.markdown("### 📦 Scraped Products")

        items_per_page = 10
        total_pages = (len(products) + items_per_page - 1) // items_per_page

        cols = st.columns([2, 3, 2])
        with cols[1]:
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1) - 1

        start_idx = page * items_per_page
        end_idx = min(start_idx + items_per_page, len(products))

        st.markdown(f"*Showing {start_idx + 1} - {end_idx} of {len(products)} products*")

        for p in products[start_idx:end_idx]:
            render_product_card(p)

    selected_asin = st.session_state.get("analyzing_asin")
    if selected_asin:
        st.markdown("---")
        st.markdown(f"### 📊 Competitor Analysis for {selected_asin}")

        st.markdown('<div class="competitor-section">', unsafe_allow_html=True)
        db = Database()
        existing_comps = db.search_products({"parent_asin": selected_asin})

        if not existing_comps:
            with st.spinner("🔍 Searching for competitors..."):
                comps = fetch_and_store_competitors(selected_asin, domain, geo)
            st.success(f"✨ Found {len(comps)} competitors!")
        else:
            st.info(f"📋 Found {len(existing_comps)} existing competitors in the database")

        cols = st.columns([3, 1])
        with cols[1]:
            if st.button("🔄 Refresh Competitors"):
                with st.spinner("Updating competitor data..."):
                    comps = fetch_and_store_competitors(selected_asin, domain, geo)
                st.success(f"✅ Found {len(comps)} competitors!")

        with cols[0]:
            if st.button("🤖 Analyze with AI", type="primary"):
                with st.spinner("🧠 Running AI analysis..."):
                    analysis = analyze_competitors(selected_asin)
                    st.markdown(analysis)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()