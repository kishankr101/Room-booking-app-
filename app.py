import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="StayEase India", layout="wide")

# --- UI ---
st.markdown("""
<style>
.prop-card {
    background: white; padding: 20px; border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
@st.cache_data
def load_data():
    data = []
    cities = ["Delhi","Mumbai","Bangalore","Hyderabad","Chennai"]
    types = ["Student","Traveler","Family"]

    for i in range(1, 51):
        data.append({
            "id": i,
            "name": f"Property {i}",
            "city": cities[i % len(cities)],
            "type": types[i % 3],
            "price": 3000 + i*100,
            "lat": 20.5 + i*0.1,
            "lon": 78.9 + i*0.1
        })
    return pd.DataFrame(data)

df = load_data()

# --- SESSION ---
if 'auth_stage' not in st.session_state:
    st.session_state.auth_stage = 'register'

# ---------------- REGISTER ----------------
if st.session_state.auth_stage == 'register':

    st.title("Register")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", 
        ["Student", "Traveler", "Family (Renter)", "Service Provider"])

    if st.button("Complete Registration"):

        if not name or not email or not phone or not password:
            st.error("⚠️ Fill all fields")
        else:
            # store credentials
            st.session_state.reg_email = email
            st.session_state.reg_password = password
            st.session_state.user_role = role
            st.session_state.user_cat = role if role != "Service Provider" else "Traveler"

            st.session_state.auth_stage = 'login'
            st.success("Registration successful! Please login.")
            st.rerun()

# ---------------- LOGIN ----------------
elif st.session_state.auth_stage == 'login':

    st.title("Login")

    login_email = st.text_input("Enter Email")
    login_password = st.text_input("Enter Password", type="password")

    if st.button("Login"):

        if not login_email or not login_password:
            st.error("⚠️ Fill all fields")
        elif (login_email == st.session_state.get("reg_email") and 
              login_password == st.session_state.get("reg_password")):

            st.session_state.auth_stage = 'main'
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

# ---------------- MAIN ----------------
elif st.session_state.auth_stage == 'main':

    if st.session_state.user_role == "Service Provider":

        st.title("Provider Panel")

        p_name = st.text_input("Property Name")
        p_city = st.selectbox("City", df['city'].unique())

        if st.button("Add Property"):
            if not p_name:
                st.error("Enter property name")
            else:
                st.success("Property added!")

    else:
        st.title("Find Stay")

        city = st.selectbox("City", df['city'].unique())
        budget = st.slider("Budget", 2000, 20000, 10000)
        category = st.selectbox("Category", ["Student","Traveler","Family"])

        filtered = df[(df.city==city)&(df.price<=budget)&(df.type==category)]

        for _, row in filtered.iterrows():
            st.markdown(f"""
            <div class="prop-card">
            <h3>{row['name']}</h3>
            <p>{row['city']} - ₹{row['price']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Book {row['id']}"):
                st.success("Booked!")

    # --- NIGHT SAFETY ---
    if 20 <= datetime.now().hour or datetime.now().hour <= 5:
        st.sidebar.error("Night Safety Active")

    if st.sidebar.button("Logout"):
        st.session_state.auth_stage = 'register'
        st.rerun()
