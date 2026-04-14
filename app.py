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

# --- 2. DATA ENGINE ---
@st.cache_data
def load_data():
    data = []
    cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow", "Patna", "Indore", "Bhopal", "Chandigarh", "Guwahati", "Kochi", "Noida", "Gurgaon", "Amritsar", "Dehradun"]
    types = ["Student", "Traveler", "Family"]

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
            "lat": 20.5937 + (i * 0.1),
            "lon": 78.9629 + (i * 0.1)
        })
    return pd.DataFrame(data)

df = load_data()

# --- 3. SESSION STATE ---
if 'auth_stage' not in st.session_state:
    st.session_state.auth_stage = 'register'
if 'user_role' not in st.session_state:
    st.session_state.user_role = ''
if 'reg_email' not in st.session_state:
    st.session_state.reg_email = ''
if 'reg_phone' not in st.session_state:
    st.session_state.reg_phone = ''

# --- 4. REGISTER PAGE ---
if st.session_state.auth_stage == 'register':
    st.title("🇮🇳 StayEase: Registration")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
    with col2:
        phone = st.text_input("Phone Number")

    role = st.selectbox("Select Your Role", 
                        ["Student", "Traveler", "Family (Renter)", "Service Provider"])

    if st.button("Complete Registration", use_container_width=True):

        if not name or not email or not phone:
            st.error("⚠️ Please fill all required fields before continuing.")
        else:
            st.session_state.user_role = role
            st.session_state.user_cat = role if role != "Service Provider" else "Traveler"
            st.session_state.reg_email = email
            st.session_state.reg_phone = phone
            st.session_state.auth_stage = 'login'
            st.rerun()

# --- 5. LOGIN PAGE ---
elif st.session_state.auth_stage == 'login':
    st.title("🔐 Login to StayEase")

    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone Number")

    if st.button("Login", use_container_width=True):

        if not email or not phone:
            st.error("⚠️ Please fill all fields correctly.")
        elif email != st.session_state.reg_email or phone != st.session_state.reg_phone:
            st.error("❌ Invalid credentials. Try again.")
        else:
            st.success("✅ Login Successful!")
            st.session_state.auth_stage = 'main'
            st.rerun()

# --- 6. MAIN APP ---
elif st.session_state.auth_stage == 'main':

    if st.session_state.user_role == "Service Provider":
        st.title("🏠 Provider Control Panel")
        tab_a, tab_b = st.tabs(["Manage Listings", "New Inquiries"])
        
        with tab_a:
            p_name = st.text_input("Property Name")
            p_city = st.selectbox("Select City", df['city'].unique())
            p_price = st.number_input("Rent (₹)", min_value=500)

            if st.button("List My Property"):
                if not p_name:
                    st.error("⚠️ Enter property name.")
                else:
                    st.success("Property live!")

        with tab_b:
            st.info("No requests yet.")

    else:
        st.title("Find a Stay in India 🇮🇳")
        
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search_city = st.selectbox("Select City", sorted(df['city'].unique()))
        with c2:
            budget = st.slider("Budget (₹)", 2000, 20000, 10000)
        with c3:
            search_type = st.selectbox("Stay Category", ["Student", "Traveler", "Family"])

        filtered_df = df[(df['city'] == search_city) & (df['price'] <= budget) & (df['type'] == search_type)]

        for _, row in filtered_df.iterrows():
            st.markdown(f"""
            <div class="prop-card">
                <h3>{row['name']} ⭐ {row['rating']}</h3>
                <p>📍 {row['city']}</p>
                <p>₹{row['price']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Book {row['name']}", key=f"btn_{row['id']}"):
                st.success("Booking request sent!")

    # --- NIGHT SAFETY ---
    curr_h = datetime.now().hour
    if 20 <= curr_h or curr_h <= 5:
        st.sidebar.error("🚨 NIGHT SAFETY ACTIVE")

    if st.sidebar.button("Log Out"):
        st.session_state.auth_stage = 'register'
        st.rerun()
