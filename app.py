import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIG ---
st.set_page_config(page_title="StayEase | Modern Room Booking", layout="wide")

# --- DESIGN SYSTEM / CSS ---
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #6366F1; color: white; }
    .property-card { border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; background: white; margin-bottom: 20px; }
    .price-tag { color: #6366F1; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATA ---
if 'bookings' not in st.session_state:
    st.session_state.bookings = []

properties = [
    {"id": 1, "name": "Global Student Residency", "type": "Student", "price": 5000, "lat": 28.6139, "lon": 77.2090, "status": "Available"},
    {"id": 2, "name": "Skyline Luxury Suites", "type": "Traveler", "price": 2500, "lat": 28.6200, "lon": 77.2100, "status": "Available"},
    {"id": 3, "name": "Family Comfort Stay", "type": "Family", "price": 3500, "lat": 28.6100, "lon": 77.2150, "status": "Full"},
]

# --- SIDEBAR (Role Selection) ---
st.sidebar.title("🏨 StayEase")
role = st.sidebar.selectbox("Access Mode", ["User / Traveler", "Property Owner"])

# --- SAFETY ALERT SYSTEM (8 PM Logic) ---
current_hour = datetime.now().hour
if 20 <= current_hour <= 23 or 0 <= current_hour <= 4:
    with st.sidebar.expander("🚨 SAFETY CHECK-IN", expanded=True):
        st.warning("It's late night. Please confirm your status.")
        if st.button("I am Safe"):
            st.success("Status Updated: Safe")
        if st.button("EMERGENCY HELP", type="primary"):
            st.error("Contacting Local Authorities & Owner...")

# --- MAIN UI LOGIC ---

if role == "User / Traveler":
    st.title("Find your perfect stay")
    
    # 1. Search Bar
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("Search Locality", placeholder="e.g. Connaught Place, Delhi")
    with col2:
        category = st.selectbox("Category", ["All", "Student", "Family", "Traveler"])
    with col3:
        price_range = st.slider("Max Budget (₹)", 1000, 10000, 5000)

    # 2. Tabs for List and Map View
    tab1, tab2 = st.tabs(["📋 Property List", "🗺️ Map View"])

    with tab1:
        for p in properties:
            if (category == "All" or p["type"] == category) and p["price"] <= price_range:
                with st.container():
                    st.markdown(f"""
                    <div class="property-card">
                        <h3>{p['name']}</h3>
                        <p>Type: <b>{p['type']}</b> | Status: <span style="color: {'green' if p['status']=='Available' else 'red'}">{p['status']}</span></p>
                        <p class="price-tag">₹{p['price']} / night</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if p['status'] == "Available":
                        if st.button(f"Book {p['name']}", key=p['id']):
                            st.session_state.bookings.append(p['name'])
                            st.success(f"Booking requested for {p['name']}!")

    with tab2:
        m = folium.Map(location=[28.6139, 77.2090], zoom_start=13)
        for p in properties:
            color = "blue" if p["type"] == "Student" else "orange"
            folium.Marker(
                [p["lat"], p["lon"]], 
                popup=f"{p['name']} - ₹{p['price']}",
                icon=folium.Icon(color=color)
            ).add_to(m)
        st_folium(m, width=1100, height=500)

elif role == "Property Owner":
    st.title("Provider Dashboard")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Bookings", len(st.session_state.bookings))
    col_b.metric("Active Listings", "5")
    col_c.metric("Revenue", "₹45,000")

    st.subheader("Manage Rooms")
    new_prop = st.expander("➕ Add New Property")
    with new_prop:
        st.text_input("Property Name")
        st.number_input("Price per Night", min_value=100)
        st.selectbox("Type", ["Student", "Family", "Traveler"])
        st.button("List Property")

    st.subheader("Recent Inquiries")
    if st.session_state.bookings:
        for b in st.session_state.bookings:
            st.write(f"🔔 New booking request for: **{b}**")
    else:
        st.info("No new inquiries yet.")

