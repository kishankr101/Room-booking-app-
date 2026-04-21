import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="StayEase India | Search. Book. Stay.", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
body {font-family: sans-serif;}
.listing-card {background:white;padding:15px;border-radius:10px;margin-bottom:10px;}
.badge {padding:5px 10px;border-radius:20px;font-size:12px;margin-right:5px;}
.student {background:#e0f2fe;color:#0369a1;}
.traveler {background:#dcfce7;color:#166534;}
.family {background:#fef3c7;color:#92400e;}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
district_blocks = {
    "Chennai": ["T Nagar","Velachery","Anna Nagar","OMR","Adyar"],
    "Coimbatore": ["Peelamedu","RS Puram","Saravanampatti","Singanallur","Gandhipuram"],
    "Madurai": ["Anna Nagar","KK Nagar","Thirunagar","Simmakkal","Villapuram"]
}

district_centers = {
    "Chennai": (13.08,80.27),
    "Coimbatore": (11.01,76.95),
    "Madurai": (9.92,78.11)
}

categories = ["Student","Traveler","Family"]

@st.cache_data
def load_data():
    rows=[]
    pid=1
    for d,blocks in district_blocks.items():
        lat,lon=district_centers[d]

        for b in blocks:
            for cat in categories:
                for i in range(4):  # 4 per category
                    rows.append({
                        "id":pid,
                        "title":f"{cat} Room {pid}",
                        "district":d,
                        "block":b,
                        "category":cat,
                        "rent":random.randint(5000,20000),
                        "lat":lat+random.uniform(-0.05,0.05),
                        "lon":lon+random.uniform(-0.05,0.05)
                    })
                    pid+=1

    return pd.DataFrame(rows)

df = load_data()

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page="register"

if "users" not in st.session_state:
    st.session_state.users={}

# ---------------- REGISTER ----------------
if st.session_state.page=="register":
    st.title("Register")

    email=st.text_input("Email")
    password=st.text_input("Password",type="password")
    role=st.selectbox("Role",["Student","Traveler","Family","Service Provider"])

    if st.button("Register"):
        if not email or not password:
            st.error("Fill all details")
        else:
            st.session_state.users[email]={
                "password":password,
                "role":role,
                "name":"",
                "phone":"",
                "properties":[]
            }
            st.session_state.page="login"
            st.rerun()

# ---------------- LOGIN ----------------
elif st.session_state.page=="login":
    st.title("Login")

    email=st.text_input("Email")
    password=st.text_input("Password",type="password")

    if st.button("Login"):
        if email in st.session_state.users and st.session_state.users[email]["password"]==password:
            st.session_state.current_user=email
            st.session_state.page="main"
            st.rerun()
        else:
            st.error("Invalid login")

# ---------------- MAIN ----------------
elif st.session_state.page=="main":

    user=st.session_state.users[st.session_state.current_user]

    menu=st.sidebar.radio("Menu",["Home","Profile","Logout"])

    # -------- HOME --------
    if menu=="Home":
        st.title("Find Rooms in Tamil Nadu")

        col1,col2,col3=st.columns(3)
        with col1:
            district=st.selectbox("District",["All"]+list(district_blocks.keys()))
        with col2:
            block=st.selectbox("Block",["All"]+[b for lst in district_blocks.values() for b in lst])
        with col3:
            category=st.selectbox("Category",["All","Student","Traveler","Family"])

        filtered=df.copy()

        if district!="All":
            filtered=filtered[filtered["district"]==district]
        if block!="All":
            filtered=filtered[filtered["block"]==block]
        if category!="All":
            filtered=filtered[filtered["category"]==category]

        tab1,tab2=st.tabs(["Map","List"])

        with tab1:
            if not filtered.empty:
                m=folium.Map(location=[filtered.iloc[0]["lat"],filtered.iloc[0]["lon"]],zoom_start=7)

                for _,r in filtered.iterrows():
                    color="blue" if r["category"]=="Student" else "green" if r["category"]=="Traveler" else "orange"
                    folium.Marker(
                        [r["lat"],r["lon"]],
                        popup=f"{r['title']} - ₹{r['rent']}",
                        icon=folium.Icon(color=color)
                    ).add_to(m)

                st_folium(m,height=400,width=900)

        with tab2:
            for _,r in filtered.iterrows():
                badge_class = "student" if r["category"]=="Student" else "traveler" if r["category"]=="Traveler" else "family"

                st.markdown(f"""
                <div class="listing-card">
                    <h4>{r['title']}</h4>
                    <p>{r['block']} | {r['district']}</p>
                    <span class="badge {badge_class}">{r['category']}</span>
                    <p>₹{r['rent']}</p>
                </div>
                """,unsafe_allow_html=True)

                if st.button("Book",key=r["id"]):
                    st.success("Booking requested!")

    # -------- PROFILE --------
    elif menu=="Profile":
        st.title("Profile")

        name=st.text_input("Name",value=user["name"])
        phone=st.text_input("Phone",value=user["phone"])

        if st.button("Save"):
            user["name"]=name
            user["phone"]=phone
            st.success("Saved")

        if user["role"]=="Service Provider":
            st.subheader("Add Property")

            pname=st.text_input("Property Name")
            city=st.selectbox("District",list(district_blocks.keys()))
            ptype=st.selectbox("For",["Student","Traveler","Family"])
            rooms=st.selectbox("Rooms",["Empty","Full"])
            price=st.number_input("Price",min_value=1000)

            if st.button("Add"):
                user["properties"].append({
                    "name":pname,
                    "district":city,
                    "type":ptype,
                    "rooms":rooms,
                    "price":price
                })
                st.success("Added")

            for p in user["properties"]:
                st.write(p)

    # -------- LOGOUT --------
    elif menu=="Logout":
        st.session_state.page="login"
        st.rerun()

# ---------------- NIGHT SAFETY ----------------
hour=datetime.now().hour
if 20<=hour or hour<=5:
    st.sidebar.warning("Night Safety Active")
