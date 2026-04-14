import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="StayEase India", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
.prop-card {background:white;padding:20px;border-radius:12px;margin-bottom:10px;}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
@st.cache_data
def load_data():
    data = []
    cities = ["Delhi","Mumbai","Bangalore","Chennai"]
    types = ["Student","Traveler","Family"]

    for i in range(1, 31):
        data.append({
            "id": i,
            "name": f"Stay #{i}",
            "city": cities[i % len(cities)],
            "type": types[i % 3],
            "price": 3000 + i * 200,
            "lat": 20.5 + i*0.1,
            "lon": 78.9 + i*0.1
        })
    return pd.DataFrame(data)

df = load_data()

# --- SESSION ---
if "page" not in st.session_state:
    st.session_state.page = "register"

if "users" not in st.session_state:
    st.session_state.users = {}

# ---------------- REGISTER ----------------
if st.session_state.page == "register":
    st.title("Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Student","Traveler","Family","Service Provider"])

    if st.button("Register"):
        if not email or not password:
            st.error("Fill all fields")
        else:
            st.session_state.users[email] = {
                "password": password,
                "role": role,
                "name": "",
                "phone": "",
                "properties": []
            }
            st.success("Registered Successfully")
            st.session_state.page = "login"
            st.rerun()

# ---------------- LOGIN ----------------
elif st.session_state.page == "login":
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in st.session_state.users and st.session_state.users[email]["password"] == password:
            st.session_state.current_user = email
            st.session_state.page = "main"
            st.rerun()
        else:
            st.error("Invalid login")

# ---------------- MAIN ----------------
elif st.session_state.page == "main":

    user = st.session_state.users[st.session_state.current_user]

    # --- SIDEBAR ---
    menu = st.sidebar.radio("Menu", ["Home","Profile","Logout"])

    # -------- HOME --------
    if menu == "Home":
        st.title("Home")

        city = st.selectbox("City", df["city"].unique())
        budget = st.slider("Budget", 2000, 20000, 10000)
        category = st.selectbox("Category", ["Student","Traveler","Family"])

        filtered = df[(df["city"]==city) & (df["price"]<=budget) & (df["type"]==category)]

        tab1, tab2 = st.tabs(["Map","List"])

        with tab1:
            if not filtered.empty:
                m = folium.Map(location=[filtered.iloc[0]["lat"], filtered.iloc[0]["lon"]])
                for _, r in filtered.iterrows():
                    folium.Marker([r["lat"], r["lon"]], popup=r["name"]).add_to(m)
                st_folium(m, width=700)

        with tab2:
            for _, r in filtered.iterrows():
                st.markdown(f"<div class='prop-card'>{r['name']} - ₹{r['price']}</div>", unsafe_allow_html=True)
                if st.button("Book", key=r["id"]):
                    st.success("Request Sent")

    # -------- PROFILE --------
    elif menu == "Profile":
        st.title("Profile")

        name = st.text_input("Name", value=user["name"])
        phone = st.text_input("Phone", value=user["phone"])

        if st.button("Save Profile"):
            user["name"] = name
            user["phone"] = phone
            st.success("Saved")

        # --- SERVICE PROVIDER EXTRA ---
        if user["role"] == "Service Provider":
            st.subheader("Add Property")

            p_name = st.text_input("Property Name")
            p_city = st.selectbox("City", df["city"].unique())
            p_type = st.selectbox("For", ["Student","Traveler","Family"])
            p_rooms = st.selectbox("Rooms", ["Available","Full"])
            p_security = st.multiselect("Security", ["CCTV","Guard","Fire Safety"])
            p_price = st.number_input("Price", min_value=1000)

            if st.button("Add Property"):
                user["properties"].append({
                    "name": p_name,
                    "city": p_city,
                    "type": p_type,
                    "rooms": p_rooms,
                    "security": p_security,
                    "price": p_price
                })
                st.success("Added")

            st.subheader("Your Properties")
            for p in user["properties"]:
                st.write(p)

    # -------- LOGOUT --------
    elif menu == "Logout":
        st.session_state.page = "login"
        st.rerun()

# --- NIGHT SAFETY ---
curr_h = datetime.now().hour
if 20 <= curr_h or curr_h <= 5:
    st.sidebar.warning("Night Safety Active")
