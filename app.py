import streamlit as st
from auth import login_signup_page
from dashboards import guest_dashboard, provider_dashboard

# --- PAGE CONFIG ---
st.set_page_config(page_title="OYO Clone | Room Booking", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# --- ROUTING ---
if not st.session_state.logged_in:
    login_signup_page()
else:
    # Sidebar for logout and role info
    with st.sidebar:
        st.title(f"👤 {st.session_state.user_role}")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.rerun()
    
    # Switch Dashboards
    if st.session_state.user_role in ["Student", "Traveler", "Family"]:
        guest_dashboard()
    else:
        provider_dashboard()
      
