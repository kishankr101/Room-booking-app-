import streamlit as st

def login_signup_page():
    st.markdown("<h1 style='text-align: center; color: #d32f2f;'>OYO STYLE BOOKING</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Create Account"])
        
        with tab1:
            email = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            if st.button("Login Now", use_container_width=True, type="primary"):
                # Simple logic for demo: If email has 'admin', it's a provider
                st.session_state.logged_in = True
                st.session_state.user_role = "Service Provider" if "admin" in email else "Student"
                st.rerun()
        
        with tab2:
            st.subheader("Register Yourself")
            name = st.text_input("Full Name")
            phone = st.text_input("Mobile Number")
            role = st.selectbox("I am a...", ["Select Role", "Student", "Traveler", "Family", "Service Provider"])
            if st.button("Register & Continue", use_container_width=True):
                if role != "Select Role":
                    st.session_state.logged_in = True
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("Please select a role first!")
                  
