import streamlit as st


# -----------------------------
# LOGIN
# -----------------------------


valid_pass = "fridge1503"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_email" not in st.session_state:
  st.session_state.user_email = None

def login_page():
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Entrer votre courriel")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if password == valid_pass:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.success("Login réussi!")

            st.switch_page("pages/app.py")
        else:
            st.error("Invalid email or password")

if not st.session_state.authenticated:
    login_page()
else:
    st.switch_page("pages/app.py")
