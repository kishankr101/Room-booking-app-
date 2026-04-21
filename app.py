import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium
import random

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="StayEase India | Search. Book. Stay.", layout="wide")

# ----------------------------
# CSS
# ----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f7f7f7;
    }

    .top-brand {
        display:flex;
        align-items:center;
        gap:10px;
        font-size:26px;
        font-weight:800;
        color:#222;
        margin-bottom: 12px;
    }

    .top-bar {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 14px;
        padding: 14px 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 14px;
    }

    .search-chip {
        display:inline-block;
        padding: 8px 14px;
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 999px;
        margin: 6px 8px 0 0;
        font-size: 13px;
        color: #444;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .section-card {
        background: white;
        border: 1px solid #e9e9e9;
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 14px;
    }

    .filter-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
        color: #2d6cdf;
    }

    .listing-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 14px;
    }

    .listing-title {
        font-size: 18px;
        font-weight: 700;
        color: #202124;
        margin-bottom: 4px;
    }

    .listing-sub {
        font-size: 13px;
        color: #666;
        margin-bottom: 10px;
    }

    .badge {
        display:inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        background: #f3f4f6;
        color: #374151;
    }

    .badge-student {
        background: #e8f1ff;
        color: #1d4ed8;
    }

    .badge-traveler {
        background: #e8fff1;
        color: #15803d;
    }

    .badge-family {
        background: #fff6e5;
        color: #b45309;
    }

    .spec-grid {
        display:grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .spec-box {
        border: 1px solid #ececec;
        border-radius: 12px;
        padding: 10px;
        background: #fafafa;
    }

    .spec-value {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
    }

    .spec-label {
        font-size: 12px;
        color: #6b7280;
    }

    .mini-grid {
        display:grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        margin-top: 10px;
    }

    .mini-box {
        border: 1px solid #ececec;
        border-radius: 10px;
        padding: 8px 10px;
        background: #fff;
        font-size: 13px;
        color: #333;
    }

    .photo-box {
        border: 1px dashed #cfd8e3;
        border-radius: 12px;
        background: linear-gradient(180deg, #f8fafc, #eef2ff);
        min-height: 150px;
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center;
        color:#475569;
        font-weight:600;
    }

    .legend-dot {
        display:inline-block;
        width:10px;
        height:10px;
        border-radius:50%;
        margin-right:6px;
        vertical-align:middle;
    }

    .header-count {
        font-size: 18px;
        font-weight: 700;
        color: #202124;
    }

    .small-muted {
        color: #6b7280;
        font-size: 13px;
    }

    .sidebar-box {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# DATA
# ----------------------------
district_blocks = {
    "Chennai": ["T. Nagar", "Velachery", "Anna Nagar", "OMR", "Adyar"],
    "Coimbatore": ["Peelamedu", "Gandhipuram", "RS Puram", "Saravanampatti", "Singanallur"],
    "Madurai": ["Anna Nagar", "KK Nagar", "Thirunagar", "Villapuram", "Simmakkal"],
    "Tiruchirappalli": ["Srirangam", "Thillai Nagar", "Woraiyur", "Cantonment", "TVS Tollgate"],
    "Salem": ["Gugai", "Fairlands", "Hasthampatti", "Ammapet", "Suramangalam"],
    "Tirunelveli": ["Palayamkottai", "Mela Thiruvenkadam", "KTC Nagar", "Vannarpettai", "Tirunelveli Town"],
    "Erode": ["Perundurai Road", "Surampatti", "Brough Road", "Gandhiji Road", "Nasiyanur"],
    "Vellore": ["Katpadi", "Sathuvachari", "Gandhi Nagar", "Bagayam", "Viruthampet"],
    "Tiruppur": ["Avinashi Road", "Palladam Road", "Gandhi Nagar", "Anupparpalayam", "Kumaran Road"],
    "Thoothukudi": ["Kamaraj Nagar", "Millerpuram", "Tuticorin Town", "Sri Sankar Nagar", "Korampallam"],
}

district_centers = {
    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Tiruchirappalli": (10.7905, 78.7047),
    "Salem": (11.6643, 78.1460),
    "Tirunelveli": (8.7139, 77.7567),
    "Erode": (11.3410, 77.7172),
    "Vellore": (12.9165, 79.1325),
    "Tiruppur": (11.1085, 77.3411),
    "Thoothukudi": (8.7642, 78.1348),
}

property_types = ["Student", "Traveler", "Family"]
bhk_types = ["1 RK", "1 BHK", "2 BHK", "3 BHK", "4 BHK"]
furnishings = ["Fully Furnished", "Semi Furnished", "Unfurnished"]
availability_options = ["Immediate", "Within 15 Days", "Within 30 Days", "After 30 Days"]
parking_options = ["2 Wheeler", "4 Wheeler", "Both", "No Parking"]
property_styles = ["Apartment", "House/Villa", "PG/Shared"]
preferred_tenants = ["Student", "Traveler", "Family"]
security_pool = ["CCTV", "24/7 Guard", "Biometric Entry", "Fire Safety", "Emergency Alarm", "Gated Security"]

def _seeded_rng():
    return random.Random(42)

@st.cache_data
def load_data():
    rng = _seeded_rng()
    rows = []
    pid = 1

    for district, blocks in district_blocks.items():
        dlat, dlon = district_centers[district]
        for block in blocks:
            for i in range(3):
                category = property_types[(pid + i) % len(property_types)]
                bhk = bhk_types[(pid + i) % len(bhk_types)]
                furnishing = furnishings[(pid + i) % len(furnishings)]
                availability = availability_options[(pid + i) % len(availability_options)]
                parking = parking_options[(pid + i) % len(parking_options)]
                style = property_styles[(pid + i) % len(property_styles)]
                security = rng.sample(security_pool, k=rng.randint(2, 5))
                preferred = preferred_tenants[(pid + i) % len(preferred_tenants)]
                room_status = rng.choice(["Empty", "Partly Occupied", "Full"])

                rent = rng.randint(5500, 28000)
                deposit = rng.randint(15000, 120000)
                builtup = rng.randint(320, 1450)
                floor = rng.randint(1, 12)
                bathrooms = rng.randint(1, 3)
                age = rng.randint(1, 20)
                balcony = rng.randint(0, 2)
                safety_score = rng.randint(3, 5)
                rank = round(rng.uniform(3.8, 4.9), 1)

                lat = dlat + rng.uniform(-0.045, 0.045)
                lon = dlon + rng.uniform(-0.045, 0.045)

                rows.append(
                    {
                        "id": pid,
                        "title": f"{bhk} in {block}, {district}",
                        "district": district,
                        "block": block,
                        "property_style": style,
                        "category": category,
                        "bhk": bhk,
                        "rent": rent,
                        "deposit": deposit,
                        "builtup": builtup,
                        "furnishing": furnishing,
                        "availability": availability,
                        "parking": parking,
                        "preferred_tenant": preferred,
                        "room_status": room_status,
                        "security": security,
                        "safety_score": safety_score,
                        "floor": floor,
                        "bathrooms": bathrooms,
                        "balcony": balcony,
                        "age_of_building": age,
                        "rank": rank,
                        "lat": lat,
                        "lon": lon,
                        "photos": rng.randint(2, 6),
                        "source": "Base",
                    }
                )
                pid += 1

    return pd.DataFrame(rows)

def get_all_properties():
    base_df = load_data().copy()
    provider_listings = st.session_state.get("provider_listings", [])
    if provider_listings:
        extra_df = pd.DataFrame(provider_listings)
        full_df = pd.concat([base_df, extra_df], ignore_index=True)
    else:
        full_df = base_df
    return full_df

def marker_color_for_category(category: str) -> str:
    if category == "Student":
        return "blue"
    if category == "Traveler":
        return "green"
    return "orange"

def badge_class_for_category(category: str) -> str:
    if category == "Student":
        return "badge badge-student"
    if category == "Traveler":
        return "badge badge-traveler"
    return "badge badge-family"

def build_filters(df: pd.DataFrame, search_district: str, search_block: str, search_category: str):
    filtered = df.copy()

    if search_district != "All Tamil Nadu":
        filtered = filtered[filtered["district"] == search_district]

    if search_block != "All Blocks":
        filtered = filtered[filtered["block"] == search_block]

    if search_category != "All":
        filtered = filtered[filtered["category"] == search_category]

    return filtered

def render_listing_card(row):
    st.markdown(
        f"""
        <div class="listing-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">
                <div>
                    <div class="listing-title">{row['title']}</div>
                    <div class="listing-sub">{row['block']}, {row['district']} • {row['property_style']} • {row['source']}</div>
                </div>
                <div style="font-weight:700;color:#ef4444;">★ {row['rank']}</div>
            </div>

            <div>
                <span class="{badge_class_for_category(row['category']).replace(' ', ' ')}">{row['category']}</span>
                <span class="badge">{row['bhk']}</span>
                <span class="badge">{row['furnishing']}</span>
                <span class="badge">{row['availability']}</span>
            </div>

            <div class="spec-grid">
                <div class="spec-box">
                    <div class="spec-value">₹ {row['rent']:,}</div>
                    <div class="spec-label">Monthly Rent</div>
                </div>
                <div class="spec-box">
                    <div class="spec-value">₹ {row['deposit']:,}</div>
                    <div class="spec-label">Deposit</div>
                </div>
                <div class="spec-box">
                    <div class="spec-value">{row['builtup']} sq.ft</div>
                    <div class="spec-label">Built-up Area</div>
                </div>
            </div>

            <div style="display:grid;grid-template-columns: 1.05fr 1fr;gap:12px;align-items:stretch;">
                <div class="photo-box">
                    <div>
                        <div style="font-size:16px;">Photos Available</div>
                        <div style="font-size:30px;margin:4px 0;">{row['photos']}</div>
                        <div style="font-size:12px;">Room preview placeholder</div>
                    </div>
                </div>

                <div>
                    <div class="mini-grid">
                        <div class="mini-box"><b>Preferred:</b> {row['preferred_tenant']}</div>
                        <div class="mini-box"><b>Rooms:</b> {row['room_status']}</div>
                        <div class="mini-box"><b>Parking:</b> {row['parking']}</div>
                        <div class="mini-box"><b>Security:</b> {row['safety_score']}/5</div>
                        <div class="mini-box"><b>Floor:</b> {row['floor']}</div>
                        <div class="mini-box"><b>Bathrooms:</b> {row['bathrooms']}</div>
                        <div class="mini-box"><b>Balcony:</b> {row['balcony']}</div>
                        <div class="mini-box"><b>Age:</b> {row['age_of_building']} years</div>
                    </div>
                </div>
            </div>

            <div style="margin-top:10px;">
                <span class="small-muted"><b>Security:</b> {" • ".join(row["security"])}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def map_for_properties(df_map: pd.DataFrame, district_focus: str):
    if df_map.empty:
        st.warning("No properties found for this search. Try changing the filters.")
        return

    if district_focus != "All Tamil Nadu" and district_focus in district_centers:
        center = district_centers[district_focus]
        zoom = 11
    else:
        center = (11.1271, 78.6569)
        zoom = 7

    m = folium.Map(location=center, zoom_start=zoom, control_scale=True)

    for _, row in df_map.iterrows():
        color = marker_color_for_category(row["category"])
        popup = folium.Popup(
            f"""
            <b>{row['title']}</b><br>
            {row['property_style']}<br>
            Category: {row['category']}<br>
            Rent: ₹{row['rent']:,}<br>
            Block: {row['block']}<br>
            District: {row['district']}
            """,
            max_width=300,
        )
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup,
            tooltip=row["title"],
            icon=folium.Icon(color=color, icon="home"),
        ).add_to(m)

    st_folium(m, height=470, width=None)

# ----------------------------
# SESSION STATE
# ----------------------------
if "auth_stage" not in st.session_state:
    st.session_state.auth_stage = "register"

if "users" not in st.session_state:
    st.session_state.users = {}

if "provider_listings" not in st.session_state:
    st.session_state.provider_listings = []

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "search_state" not in st.session_state:
    st.session_state.search_state = {
        "district": "All Tamil Nadu",
        "block": "All Blocks",
        "category": "All",
    }

# ----------------------------
# AUTH FLOW
# ----------------------------
if st.session_state.auth_stage == "register":
    st.markdown('<div class="top-brand">StayEase India</div>', unsafe_allow_html=True)
    st.title("Register")
    st.write("Create your account first, then login to open the dashboard.")

    with st.form("register_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            email = st.text_input("Email ID")
            password = st.text_input("Password", type="password")
        with c2:
            role = st.selectbox(
                "You are",
                ["Student", "Traveler", "Family", "Service Provider"],
            )

        submitted = st.form_submit_button("Complete Registration", use_container_width=True)

    if submitted:
        if not email or not password:
            st.error("Please fill all required details before continuing.")
        elif email in st.session_state.users:
            st.error("This email is already registered. Please login.")
        else:
            st.session_state.users[email] = {
                "password": password,
                "role": role,
                "name": "",
                "phone": "",
                "properties": [],
            }
            st.success("Registration completed. Now login with your email and password.")
            st.session_state.auth_stage = "login"
            st.rerun()

elif st.session_state.auth_stage == "login":
    st.markdown('<div class="top-brand">StayEase India</div>', unsafe_allow_html=True)
    st.title("Login")
    st.write("Enter the same email and password you used during registration.")

    with st.form("login_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            login_email = st.text_input("Email ID")
        with c2:
            login_password = st.text_input("Password", type="password")

        login_submit = st.form_submit_button("Login", use_container_width=True)

    if login_submit:
        user = st.session_state.users.get(login_email)
        if not login_email or not login_password:
            st.error("Please fill email and password.")
        elif not user or user["password"] != login_password:
            st.error("Invalid email or password.")
        else:
            st.session_state.current_user = login_email
            st.session_state.auth_stage = "main"
            st.rerun()

# ----------------------------
# MAIN DASHBOARD
# ----------------------------
elif st.session_state.auth_stage == "main":
    user_email = st.session_state.current_user
    user = st.session_state.users[user_email]

    st.markdown('<div class="top-brand">StayEase India</div>', unsafe_allow_html=True)

    menu = st.sidebar.radio("Menu", ["Home", "Profile", "Logout"], index=0)

    # ---------------- HOME ----------------
    if menu == "Home":
        st.markdown(
            """
            <div class="top-bar">
                <div style="font-size:20px;font-weight:700;color:#202124;">Find rooms, homes and stays across Tamil Nadu</div>
                <div class="small-muted">Search district wise, block wise, and by user type. Map updates based on your filter.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Search bar
        districts = ["All Tamil Nadu"] + sorted(district_blocks.keys())
        search_district_default = st.session_state.search_state["district"]
        search_district_index = districts.index(search_district_default) if search_district_default in districts else 0

        current_district = st.selectbox("District", districts, index=search_district_index)

        if current_district == "All Tamil Nadu":
            blocks = ["All Blocks"]
        else:
            blocks = ["All Blocks"] + district_blocks[current_district]

        current_block_default = st.session_state.search_state["block"]
        current_block_index = blocks.index(current_block_default) if current_block_default in blocks else 0
        current_block = st.selectbox("Block / Locality", blocks, index=current_block_index)

        category_options = ["All", "Student", "Traveler", "Family"]
        current_category_default = st.session_state.search_state["category"]
        current_category_index = category_options.index(current_category_default) if current_category_default in category_options else 0
        current_category = st.selectbox("Category", category_options, index=current_category_index)

        if st.button("Search", use_container_width=True):
            st.session_state.search_state = {
                "district": current_district,
                "block": current_block,
                "category": current_category,
            }
            st.rerun()

        st.markdown("**Nearby Localities**")
        chip_source = []
        if st.session_state.search_state["district"] != "All Tamil Nadu":
            chip_source = district_blocks[st.session_state.search_state["district"]]
        else:
            for lst in district_blocks.values():
                chip_source.extend(lst)
            chip_source = chip_source[:8]

        if chip_source:
            chips_html = "".join([f"<span class='search-chip'>{loc}</span>" for loc in chip_source[:6]])
            st.markdown(chips_html, unsafe_allow_html=True)

        # Build combined data
        full_df = get_all_properties()

        # Sidebar-like filters inside the page to match the screenshot
        left_col, filter_col, result_col = st.columns([1.15, 0.85, 1.7], gap="large")

        with filter_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)

            bhk_filter = st.selectbox("BHK Type", ["All"] + bhk_types)
            rent_max = st.slider("Rent Range (₹)", 3000, 50000, 25000)
            furnishing_filter = st.selectbox("Furnishing", ["All"] + furnishings)
            availability_filter = st.selectbox("Availability", ["All"] + availability_options)
            tenant_filter = st.selectbox("Preferred Tenants", ["All"] + preferred_tenants)
            style_filter = st.selectbox("Property Type", ["All"] + property_styles)
            parking_filter = st.selectbox("Parking", ["All"] + parking_options)

            if st.button("Reset Filters", use_container_width=True):
                st.session_state.search_state = {
                    "district": "All Tamil Nadu",
                    "block": "All Blocks",
                    "category": "All",
                }
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        filtered_df = build_filters(
            full_df,
            st.session_state.search_state["district"],
            st.session_state.search_state["block"],
            st.session_state.search_state["category"],
        )

        if bhk_filter != "All":
            filtered_df = filtered_df[filtered_df["bhk"] == bhk_filter]
        if rent_max:
            filtered_df = filtered_df[filtered_df["rent"] <= rent_max]
        if furnishing_filter != "All":
            filtered_df = filtered_df[filtered_df["furnishing"] == furnishing_filter]
        if availability_filter != "All":
            filtered_df = filtered_df[filtered_df["availability"] == availability_filter]
        if tenant_filter != "All":
            filtered_df = filtered_df[filtered_df["preferred_tenant"] == tenant_filter]
        if style_filter != "All":
            filtered_df = filtered_df[filtered_df["property_style"] == style_filter]
        if parking_filter != "All":
            filtered_df = filtered_df[filtered_df["parking"] == parking_filter]

        with result_col:
            sort_by = st.selectbox(
                "Sort By",
                ["NoBroker Rank", "Price Low to High", "Price High to Low", "Rent Low to High", "Rent High to Low"],
            )

            if sort_by == "NoBroker Rank":
                filtered_df = filtered_df.sort_values(["rank", "rent"], ascending=[False, True])
            elif sort_by in ["Price Low to High", "Rent Low to High"]:
                filtered_df = filtered_df.sort_values("rent", ascending=True)
            else:
                filtered_df = filtered_df.sort_values("rent", ascending=False)

            district_text = st.session_state.search_state["district"]
            block_text = st.session_state.search_state["block"]
            cat_text = st.session_state.search_state["category"]

            title_line = f"{len(filtered_df)} Properties for Rent"
            if district_text != "All Tamil Nadu":
                title_line += f" in {block_text if block_text != 'All Blocks' else district_text}, {district_text}"
            else:
                title_line += " in Tamil Nadu"

            st.markdown(f"<div class='header-count'>{title_line}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='small-muted'>Showing {cat_text if cat_text != 'All' else 'all categories'} with live map markers.</div>",
                unsafe_allow_html=True,
            )

            if not filtered_df.empty:
                st.markdown(
                    """
                    <div style="margin:8px 0 12px 0;">
                        <span class="legend-dot" style="background:#2563eb;"></span>Student
                        &nbsp;&nbsp;
                        <span class="legend-dot" style="background:#16a34a;"></span>Traveler
                        &nbsp;&nbsp;
                        <span class="legend-dot" style="background:#f59e0b;"></span>Family
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            map_for_properties(filtered_df, st.session_state.search_state["district"])

            for _, row in filtered_df.iterrows():
                render_listing_card(row)

                btn1, btn2 = st.columns(2)
                with btn1:
                    if st.button("Contact Owner", key=f"contact_{row['id']}"):
                        st.success(f"Request sent for {row['title']}.")
                with btn2:
                    if st.button("Shortlist", key=f"shortlist_{row['id']}"):
                        st.info("Added to shortlist.")

            if filtered_df.empty:
                st.warning("No properties found. Try a different district, block, category, or rent range.")

        with left_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(
                "<div class='filter-title'>Map View</div>"
                "<div class='small-muted'>Markers update by district, block and category.</div>",
                unsafe_allow_html=True,
            )

            small_df = filtered_df[["title", "district", "block", "category", "lat", "lon", "rent"]].copy() if not filtered_df.empty else filtered_df
            map_for_properties(filtered_df, st.session_state.search_state["district"])
            st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- PROFILE ----------------
    elif menu == "Profile":
        st.header("Profile")

        st.markdown(
            """
            <div class="section-card">
                <div class="filter-title">Complete Your Profile</div>
                <div class="small-muted">You can edit your name, phone number and save details here.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        name_val = st.text_input("Name", value=user.get("name", ""))
        phone_val = st.text_input("Phone Number", value=user.get("phone", ""))

        if st.button("Save Profile", use_container_width=True):
            user["name"] = name_val
            user["phone"] = phone_val
            st.success("Profile saved successfully.")

        if user["role"] == "Service Provider":
            st.markdown(
                """
                <div class="section-card">
                    <div class="filter-title">List House / Room</div>
                    <div class="small-muted">Add safety, security, rooms status, and who can stay there.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form("provider_listing_form", clear_on_submit=False):
                p1, p2 = st.columns(2)
                with p1:
                    prop_name = st.text_input("Property Name")
                    district = st.selectbox("District", sorted(district_blocks.keys()), key="provider_district")
                    block = st.selectbox("Block / Area", district_blocks[district], key="provider_block")
                    prop_style = st.selectbox("Property Style", property_styles)
                    bhk = st.selectbox("BHK Type", bhk_types)
                with p2:
                    rent = st.number_input("Rent (₹)", min_value=1000, step=500)
                    deposit = st.number_input("Deposit (₹)", min_value=0, step=1000)
                    furnishing = st.selectbox("Furnishing", furnishings)
                    availability = st.selectbox("Availability", availability_options)
                    preferred_tenant = st.selectbox("Preferred Tenant", preferred_tenants)

                p3, p4 = st.columns(2)
                with p3:
                    parking = st.selectbox("Parking", parking_options)
                    room_status = st.selectbox("Rooms Status", ["Empty", "Partly Occupied", "Full"])
                    floor = st.number_input("Floor", min_value=0, step=1)
                with p4:
                    builtup = st.number_input("Built-up Area (sq.ft)", min_value=100, step=10)
                    bathrooms = st.number_input("Bathrooms", min_value=1, step=1)
                    balcony = st.number_input("Balcony Count", min_value=0, step=1)

                security = st.multiselect(
                    "Safety / Security",
                    ["CCTV", "24/7 Guard", "Biometric Entry", "Fire Safety", "Emergency Alarm", "Gated Security"],
                )

                submit_listing = st.form_submit_button("Add Property", use_container_width=True)

            if submit_listing:
                if not prop_name:
                    st.error("Please enter property name.")
                elif rent <= 0:
                    st.error("Please enter a valid rent.")
                else:
                    dlat, dlon = district_centers[district]
                    rng = random.Random(len(st.session_state.provider_listings) + 100)

                    new_listing = {
                        "id": 10000 + len(st.session_state.provider_listings) + 1,
                        "title": prop_name,
                        "district": district,
                        "block": block,
                        "property_style": prop_style,
                        "category": preferred_tenant,
                        "bhk": bhk,
                        "rent": int(rent),
                        "deposit": int(deposit),
                        "builtup": int(builtup),
                        "furnishing": furnishing,
                        "availability": availability,
                        "parking": parking,
                        "preferred_tenant": preferred_tenant,
                        "room_status": room_status,
                        "security": security if security else ["CCTV"],
                        "safety_score": rng.randint(3, 5),
                        "floor": int(floor),
                        "bathrooms": int(bathrooms),
                        "balcony": int(balcony),
                        "age_of_building": rng.randint(1, 18),
                        "rank": round(rng.uniform(3.8, 4.9), 1),
                        "lat": dlat + rng.uniform(-0.03, 0.03),
                        "lon": dlon + rng.uniform(-0.03, 0.03),
                        "photos": rng.randint(2, 5),
                        "source": "Provider",
                    }

                    st.session_state.provider_listings.append(new_listing)
                    st.session_state.users[user_email]["properties"].append(new_listing)
                    st.success("Property added successfully.")

            if user.get("properties"):
                st.subheader("Your Listed Properties")
                user_props_df = pd.DataFrame(user["properties"])
                st.dataframe(
                    user_props_df[
                        ["title", "district", "block", "bhk", "rent", "preferred_tenant", "room_status", "availability"]
                    ],
                    use_container_width=True,
                )

    # ---------------- LOGOUT ----------------
    elif menu == "Logout":
        st.session_state.current_user = None
        st.session_state.auth_stage = "login"
        st.rerun()

    # Night safety logic
    curr_h = datetime.now().hour
    if 20 <= curr_h or curr_h <= 5:
        st.sidebar.markdown(
            """
            <div class="sidebar-box">
                <b>🚨 Night Safety Active</b><br>
                It is late. Stay alert.
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.sidebar.button("I am Safe ✅"):
            st.sidebar.success("Status updated.")
        if st.sidebar.button("SOS / Help 🆘"):
            st.sidebar.error("Emergency help requested.")

    if st.sidebar.button("Log Out"):
        st.session_state.current_user = None
        st.session_state.auth_stage = "login"
        st.rerun()
