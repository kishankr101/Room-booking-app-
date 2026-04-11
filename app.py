import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIG & PREMIUM UI ---
st.set_page_config(page_title="StayEase India | Premium Stay", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a SaaS-like Modern Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main { background: #fdfdfd; }
    .stButton>button { 
        border-radius: 10px; height: 3.5em; font-weight: 700; 
        background: linear-gradient(90deg, #6366F1 0%, #4F46E5 100%); color: white; border: none;
    }
    .city-card {
        border-radius: 20px; overflow: hidden; position: relative;
        margin-bottom: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    .property-card {
        background: white; padding: 20px; border-radius: 15px;
        border: 1px solid #f1f1f1; margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .property-card:hover { transform: translateY(-5px); border-color: #6366F1; }
    .rating-badge { background: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE INITIALIZATION ---
if 'auth_stage' not in st.session_state:
    st.session_state.auth_stage = 'register'  # Stages: register, login, main_app
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# --- 3. AUTHENTICATION FLOW ---

# REGISTRATION SCREEN
if st.session_state.auth_stage == 'register':
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("Create Account 🚀")
        st.subheader("Join India's most trusted stay network")
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email ID")
        user_type = st.selectbox("I am a...", ["Student", "Traveler", "Family"])
        
        if st.button("Sign Up"):
            if name and phone and email:
                st.session_state.user_data = {"name": name, "type": user_type}
                st.session_state.auth_stage = 'login'
                st.rerun()
            else:
                st.error("Please fill all details")

# LOGIN SCREEN
elif st.session_state.auth_stage == 'login':
    st.title("Welcome Back 👋")
    login_email = st.text_input("Enter Registered Email")
    if st.button("Login to Dashboard"):
        if login_email:
            st.session_state.auth_stage = 'main_app'
            st.rerun()

# MAIN APPLICATION
elif st.session_state.auth_stage == 'main_app':
    
    # --- SIDEBAR & SAFETY ---
    st.sidebar.title(f"Hi, {st.session_state.user_data['name']}")
    st.sidebar.info(f"Role: {st.session_state.user_data['type']}")
    
    current_hour = datetime.now().hour
    if 20 <= current_hour or current_hour <= 4:
        st.sidebar.warning("🌙 Night Safety Active")
        st.sidebar.button("I'm Home Safe")
    
    # --- TOP NAVIGATION & SEARCH ---
    st.title("Discover Your Next Stay")
    
    states = ["Delhi", "Maharashtra", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "Rajasthan"]
    
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        loc_search = st.text_input("🔍 Search India-wide", placeholder="Try 'Indiranagar, Bangalore'")
    with c2:
        state_sel = st.selectbox("State", states)
    with c3:
        price_limit = st.select_slider("Budget", options=[1000, 2000, 5000, 10000, 20000])
    with c4:
        # Category is pre-locked based on registration but can be changed here
        cat_filter = st.selectbox("Category", ["Student", "Traveler", "Family"], 
                                 index=["Student", "Traveler", "Family"].index(st.session_state.user_data['type']))

    # --- CITY HIGHLIGHTS (UI/UX Improvement) ---
    st.write("### Popular in India")
    city_cols = st.columns(3)
    cities = [
        {"name": "Bangalore", "img": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=400", "desc": "IT Hub & Student PGs"},
        {"name": "Mumbai", "img": "https://images.unsplash.com/photo-1566550970634-08db530302ba?w=400", "desc": "Business & Luxury Stays"},
        {"name": "Jaipur", "img": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=400", "desc": "History & Family Tourism"}
    ]
    
    for i, city in enumerate(cities):
        with city_cols[i]:
            st.markdown(f"""
                <div class="city-card">
                    <img src="{city['img']}" style="width:100%; height:150px; object-fit:cover;">
                    <div style="padding:10px;"><b>{city['name']}</b><br><small>{city['desc']}</small></div>
                </div>
            """, unsafe_allow_html=True)

    # --- PROPERTY LISTINGS ---
    st.write("---")
    st.subheader(f"Available {cat_filter} Stays in {state_sel}")
    
    # Mock Database
    properties = [
        {"name": "Stanza Living - Blue Bell", "price": 8500, "rating": 4.8, "services": "WiFi, Gym, Meals", "city": "Bangalore"},
        {"name": "Zolo Scholars", "price": 4500, "rating": 4.2, "services": "Laundry, CCTV, WiFi", "city": "Delhi"},
        {"name": "Heritage Villa", "price": 12000, "rating": 4.9, "services": "Pool, Kitchen, Garden", "city": "Jaipur"}
    ]
    
    for p in properties:
        if p['price'] <= price_limit:
            with st.container():
                st.markdown(f"""
                <div class="property-card">
                    <div style="display: flex; justify-content: space-between;">
                        <h4 style="margin:0;">{p['name']}</h4>
                        <span class="rating-badge">★ {p['rating']} (120 reviews)</span>
                    </div>
                    <p style="color:#666; font-size: 0.9em;">📍 {p['city']} • {cat_filter} Friendly</p>
                    <p style="margin: 5px 0;"><b>Services:</b> {p['services']}</p>
                    <h3 style="color:#6366F1;">₹{p['price']}<small>/mo</small></h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Reserve Now - {p['name']}", key=p['name']):
                    st.success("Booking Request Sent to Provider!")

    if st.button("Log Out", type="secondary"):
        st.session_state.auth_stage = 'register'
        st.rerun()
        
