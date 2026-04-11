import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium

# --- 1. PAGE CONFIG & UI THEME ---
st.set_page_config(page_title="StayEase India | Search. Book. Stay.", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    /* Custom Card Design */
    .prop-card {
        background: white; padding: 20px; border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border: 1px solid #E2E8F0; margin-bottom: 20px;
    }
    .security-tag {
        background: #DCFCE7; color: #166534; padding: 4px 10px;
        border-radius: 20px; font-size: 12px; font-weight: 600; margin-right: 5px;
    }
    .price-text { color: #4F46E5; font-size: 22px; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE (50+ City Logic) ---
# In a real app, this would come from a Database (SQL).
@st.cache_data
def load_data():
    data = []
    cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow", "Patna", "Indore", "Bhopal", "Chandigarh", "Guwahati", "Kochi", "Noida", "Gurgaon", "Amritsar", "Dehradun"]
    types = ["Student", "Traveler", "Family"]
    
    # Generating 60+ ground-level listings
    for i in range(1, 61):
        city = cities[i % len(cities)]
        user_type = types[i % 3]
        data.append({
            "id": i,
            "name": f"{city} Residency #{i}",
            "city": city,
            "type": user_type,
            "price": 3000 + (i * 150),
            "rating": round(3.5 + (i % 1.5), 1),
            "security": ["CCTV", "24/7 Guard", "Biometric Entry", "Fire Safety", "Female Warden"][:(i%4)+2],
            "lat": 20.5937 + (i * 0.1), # Spread across India
            "lon": 78.9629 + (i * 0.1)
        })
    return pd.DataFrame(data)

df = load_data()

# --- 3. SESSION STATE ---
if 'auth_stage' not in st.session_state:
    st.session_state.auth_stage = 'register'
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'Traveler'

# --- 4. AUTHENTICATION (Registration & Login) ---

if st.session_state.auth_stage == 'register':
    st.title("🇮🇳 StayEase: Registration")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
    with col2:
        phone = st.text_input("Phone Number")
        role = st.selectbox("Register as", ["User (Guest)", "Service Provider (Owner)"])
    
    user_cat = st.radio("Primary Category", ["Student", "Traveler", "Family"])
    
    if st.button("Complete Registration", use_container_width=True):
        st.session_state.user_role = role
        st.session_state.user_cat = user_cat
        st.session_state.auth_stage = 'main'
        st.rerun()

elif st.session_state.auth_stage == 'main':
    
    # --- SERVICE PROVIDER DASHBOARD ---
    if st.session_state.user_role == "Service Provider (Owner)":
        st.title("🏠 Provider Control Panel")
        tab_a, tab_b = st.tabs(["Manage Listings", "New Inquiries"])
        
        with tab_a:
            st.subheader("Add Your Property to India Database")
            p_name = st.text_input("Property Name (e.g., Sharma Niwas)")
            p_city = st.selectbox("Select City", df['city'].unique())
            p_sec = st.multiselect("Security Features", ["CCTV", "Night Guard", "Fingerprint Lock", "Fire Extinguisher", "Emergency Alarm"])
            p_price = st.number_input("Monthly/Daily Rent (₹)", min_value=500)
            if st.button("List My Property"):
                st.success("Property live! Pending verification from ground team.")
        
        with tab_b:
            st.info("No active booking requests yet. Your property is visible to Students/Travelers.")

    # --- USER DASHBOARD ---
    else:
        st.title(f"Find a Stay in India 🇮🇳")
        
        # Search & Filter Bar
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search_city = st.selectbox("Select City (50+ Cities Available)", sorted(df['city'].unique()))
        with c2:
            budget = st.slider("Your Budget (₹)", 2000, 20000, 10000)
        with c3:
            search_type = st.selectbox("Stay Category", ["Student", "Traveler", "Family"], index=["Student", "Traveler", "Family"].index(st.session_state.user_cat))

        # Filtered Data
        filtered_df = df[(df['city'] == search_city) & (df['price'] <= budget) & (df['type'] == search_type)]

        # Map & List View
        t1, t2 = st.tabs(["🗺️ Interactive Map", "📋 Property List"])

        with t1:
            if not filtered_df.empty:
                m = folium.Map(location=[filtered_df.iloc[0]['lat'], filtered_df.iloc[0]['lon']], zoom_start=11)
                for _, row in filtered_df.iterrows():
                    folium.Marker(
                        [row['lat'], row['lon']],
                        popup=f"{row['name']} - ₹{row['price']}",
                        icon=folium.Icon(color="blue", icon="home")
                    ).add_to(m)
                st_folium(m, width=1200, height=450)
            else:
                st.warning("No properties found on map for this filter.")

        with t2:
            if filtered_df.empty:
                st.error("No properties match your search. Try increasing the budget.")
            for _, row in filtered_df.iterrows():
                st.markdown(f"""
                <div class="prop-card">
                    <div style="display:flex; justify-content:space-between;">
                        <h3 style="margin:0;">{row['name']}</h3>
                        <span style="color:#F59E0B; font-weight:bold;">★ {row['rating']}</span>
                    </div>
                    <p style="color:#64748B;">📍 {row['city']} | Ground Level Verified</p>
                    <div style="margin: 10px 0;">
                        {' '.join([f'<span class="security-tag">{s}</span>' for s in row['security']])}
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="price-text">₹{row['price']}<small style="font-size:12px; color:#94A3B8;">/period</small></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Confirm Booking for {row['name']}", key=f"btn_{row['id']}"):
                    st.success(f"Request sent to owner! They will call you at your registered number.")

    # Night Safety Logic (Always Running)
    curr_h = datetime.now().hour
    if 20 <= curr_h or curr_h <= 5:
        st.sidebar.error("🚨 NIGHT SAFETY ACTIVE")
        st.sidebar.write("It's late. Are you safe?")
        if st.sidebar.button("I am Safe ✅"):
            st.sidebar.success("Status Updated.")
        if st.sidebar.button("SOS / HELP 🆘", type="primary"):
            st.sidebar.write("Calling nearest police station...")

    if st.sidebar.button("Log Out"):
        st.session_state.auth_stage = 'register'
        st.rerun()
        
