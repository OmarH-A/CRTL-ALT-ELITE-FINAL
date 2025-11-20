import pandas as pd
import streamlit as st


@st.cache_data
def load_google_sheets():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjeNw-6JbrtfT34XOWGguf5r8EURD_pXvms5qQ6lHKG2LXjcGfNfiQ4Vrran4HJJqPyMGm0wH2jaHm/pub?gid=0&single=true&output=csv"
    return pd.read_csv(url)