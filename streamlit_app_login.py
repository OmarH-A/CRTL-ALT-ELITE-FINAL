import streamlit as st


# -----------------------------
# LOGIN
# -----------------------------


valid_email = "ctrlaltelite.alertsystem@gmail.com"
valid_pass = "fridge1503"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if email == valid_email and password == valid_pass:
            st.session_state.authenticated = True
            st.success("Login successful!")

            # Rediriger vers l'app
            st.switch_page("pages/app.py")
        else:
            st.error("Invalid email or password")

if not st.session_state.authenticated:
    login_page()
else:
    st.switch_page("pages/app.py")
