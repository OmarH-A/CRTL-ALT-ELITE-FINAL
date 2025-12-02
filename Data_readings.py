import pandas as pd
import streamlit as st
import time


SHEET_URL = "https://docs.google.com/spreadsheets/d/1XQyMxnbtav3cQM6aGdskCCEul3lViw20_8-ppIuoJZw/edit?gid=0#gid=0"
SHEET_URL_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjeNw-6JbrtfT34XOWGguf5r8EURD_pXvms5qQ6lHKG2LXjcGfNfiQ4Vrran4HJJqPyMGm0wH2jaHm/pub"


@st.cache_data(ttl=5)
def load_google_sheets(n):

    range_str = "A1000000:E1000005"

    cache_bust = int(time.time())

    url = (
        f"{SHEET_URL_csv}?gid=0&single=true&output=csv&range={range_str}"
        f"&nocache={cache_bust}"
    )
    
    df = pd.read_csv(url)

    return df.tail(n)
