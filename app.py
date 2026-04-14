import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIG ---
st.set_page_config(page_title="StayEase India", layout="wide")

# --- UI ---
st.markdown("""
<style>
.stApp { background-color: #F8FAFC; }
.prop-card { background:white; padding:20px; border-radius:12px; margin-bottom:15px;}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
@st.cache_data
def load_data():
    data = []
    cities = ["Delhi","Mumbai","Bangalore","Chennai"]
    types = ["Student","Traveler","Family"]

    for i in range(1,31):
        data.append({
            "id": i,
            "name": f"Stay {i}",
            "city": cities[i % len(cities)],
            "type": types[i % 3],
            "price": 3000 + i*200,
            "lat": 20 + i*0.1,
            "lon": 78 + i*0.1
        })
    return pd.DataFrame(data)

df = load_data()

# --- SESSION ---
if "auth_stage" not in st.session_state:
    st.session_state.auth_stage = "register"

# --- REGISTER ---
if st.session_state.auth_stage == "register":

    st.title("Register")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    role = st.selectbox("Role", ["Student","Traveler","Family (Renter)","Service Provider"])

    if st.button("Complete Registration"):

        if not name or not email or not phone:
            st.error("Fill all fields")
        else:
            # Save user
            st.session_state.user_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "role": role
            }
            st.session_state.auth_stage = "login"
            st.success("Registration Done → Please Login")
            st.rerun()

# --- LOGIN ---
elif st.session_state.auth_stage == "login":

    st.title("Login")

    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone")

    if st.button("Login"):

        if not email or not phone:
            st.error("Fill all fields")
        else:
            saved = st.session_state.get("user_data", {})

            # simple match
            if email == saved.get("email") and phone == saved.get("phone"):
                st.session_state.user_role = saved.get("role")
                st.session_state.auth_stage = "main"
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

# --- MAIN ---
elif st.session_state.auth_stage == "main":

    # Provider
    if st.session_state.user_role == "Service Provider":
        st.title("Provider Dashboard")
        st.info("Add property feature here")

    # User
    else:
        st.title("Find Stay")

        city = st.selectbox("City", df["city"].unique())
        budget = st.slider("Budget", 2000,20000,10000)
        typ = st.selectbox("Type", ["Student","Traveler","Family"])

        f = df[(df.city==city)&(df.price<=budget)&(df.type==typ)]

        for _,row in f.iterrows():
            st.markdown(f"""
            <div class="prop-card">
            <h3>{row['name']}</h3>
            <p>{row['city']} - ₹{row['price']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Book", key=row["id"]):
                st.success("Booked!")

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.auth_stage = "register"
        st.rerun()
