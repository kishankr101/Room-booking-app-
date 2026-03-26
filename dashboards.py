import streamlit as st
from data import mock_buildings

def guest_dashboard():
    # Detail View Toggle
    if "selected_building" not in st.session_state:
        st.session_state.selected_building = None

    if st.session_state.selected_building:
        show_details_page()
    else:
        show_search_results()

def show_search_results():
    st.title("📍 Find Your Next Room")
    
    # 1. Search Section
    c1, c2 = st.columns([2, 1])
    with c1:
        search_query = st.text_input("Search by Building Name or Region", placeholder="e.g. Sector 45 or Student Stay")
    
    st.divider()

    # 2. Display Buildings in Rectangle Shape
    for b in mock_buildings:
        if search_query.lower() in b['name'].lower() or search_query.lower() in b['region'].lower():
            with st.container(border=True):
                col_img, col_info, col_btn = st.columns([1, 2, 1])
                with col_img:
                    st.image(b['image'], use_container_width=True)
                with col_info:
                    st.subheader(b['name'])
                    st.write(f"📍 {b['region']}")
                    st.write(f"⭐ {b['features']}")
                    # Small availability summary
                    st.write(f"🟢 {b['empty_rooms']} Rooms Available")
                with col_btn:
                    st.markdown(f"### ₹{b['price']}/mo")
                    if st.button("View Details", key=f"view_{b['id']}", use_container_width=True):
                        st.session_state.selected_building = b
                        st.rerun()

def show_details_page():
    b = st.session_state.selected_building
    if st.button("⬅️ Back to Listings"):
        st.session_state.selected_building = None
        st.rerun()

    st.image(b['image'], use_container_width=True)
    
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.header(b['name'])
        st.markdown(f"### Facilities: {b['features']}")
        st.divider()
        
        # STANDARD AVAILABILITY FORMAT
        st.subheader("Room Inventory Status")
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            st.metric("Available (Khali)", b['empty_rooms'], delta="Empty", delta_color="normal")
        with col_st2:
            st.metric("Occupied (Full)", b['full_rooms'], delta="-", delta_color="inverse")
        
        st.progress(b['full_rooms'] / (b['full_rooms'] + b['empty_rooms']), text="Occupancy Level")

    with col_right:
        with st.container(border=True):
            st.subheader("Confirm Booking")
            st.write(f"Monthly Rent: ₹{b['price']}")
            st.write("Electricity: Extra")
            st.text_input("Your Full Name")
            if st.button("Book Now", type="primary", use_container_width=True):
                st.success("Booking Request Sent!")
                st.balloons()

def provider_dashboard():
    st.title("🏢 Owner Control Center")
    tab1, tab2 = st.tabs(["Add Property", "My Bookings"])
    
    with tab1:
        st.subheader("List Your Building")
        scale = st.selectbox("How many buildings?", ["Select", "Less than 5", "Less than 10", "Apartment Complex"])
        total_rooms = st.number_input("Total Rooms", min_value=1)
        if st.button("Save Property Step-by-Step"):
            st.info("Property saved. Please upload images in next step.")
          
