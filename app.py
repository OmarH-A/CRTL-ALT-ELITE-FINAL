import streamlit as st
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Sensor Dashboard",
    layout="centered",
)


# -----------------------------
# NAVIGATION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Temperature"


def go(page):
    st.session_state.page = page


# -----------------------------
# SHARED TOP BAR
# -----------------------------
def top_section(title, avg_value, extra_info):
    st.markdown(
        f"""
        <div style="padding: 15px; 
                    background-color: #f5f5f5; 
                    border-radius: 12px; 
                    border: 1px solid #e1e1e1;">
            <h2 style="margin: 0; color: #333;">{title}</h2>
            <p style="margin: 4px 0; color: #666;">Heure Actuelle: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p style="margin: 4px 0; color: #666;">Moyenne: <b>{avg_value}</b></p>
            <p style="margin: 4px 0; color: #666;">{extra_info}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# PAGE: TEMPERATURE
# -----------------------------
def temperature_page():
    top_section(
        title="Temperature Overview",
        avg_value="-- °C",            # you can compute this later
        extra_info="Last updated: Automatically from ThingSpeak"
    )

    st.write("")
    st.markdown("### Temperature Graph")

    # ThingSpeak Embed (temperature)
    st.components.v1.html(
        """
        <iframe width="450" height="260" style="border: 1px solid #cccccc;"
        src="https://thingspeak.com/channels/3163867/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
        """,
        height=300,
    )


# -----------------------------
# PAGE: HUMIDITY
# -----------------------------
def humidity_page():
    top_section(
        title="Humidity Overview",
        avg_value="-- %",             # you can compute this later
        extra_info="Last updated: Automatically from ThingSpeak"
    )

    st.write("")
    st.markdown("### Humidity Graph")

    # PLACEHOLDER — insert your humidity iframe here
    st.components.v1.html(
        """
        <!-- INSERT HUMIDITY IFRAME HERE -->
        <div style='width: 100%; height: 260px; 
             display: flex; align-items: center; justify-content: center; 
             color: #999; border: 1px dashed #ccc; border-radius: 10px;'>
            Humidity graph iframe goes here
        </div>
        """,
        height=300,
    )


# -----------------------------
# PAGE: HISTORY
# -----------------------------
def history_page():
    top_section(
        title="History Overview",
        avg_value="N/A",
        extra_info="Last history update (simulated): 2025-01-01 12:00:00"
    )

    st.write("")
    st.markdown("### History Data")
    st.info("This page will later show historical data from your database.")


# -----------------------------
# PAGE: SETTINGS
# -----------------------------
def settings_page():
    top_section(
        title="Settings",
        avg_value="-",
        extra_info="System information overview"
    )

    st.write("")
    st.markdown("### App Settings")
    st.info("Configuration options go here.")


# -----------------------------
# PAGE LOADER
# -----------------------------
if st.session_state.page == "Temperature":
    temperature_page()
elif st.session_state.page == "Humidity":
    humidity_page()
elif st.session_state.page == "History":
    history_page()
elif st.session_state.page == "Settings":
    settings_page()


# -----------------------------
# BOTTOM NAVIGATION BAR
# -----------------------------
st.markdown("""
<style>
.navbar {
    position: fixed;
    bottom: 0;
    left: 0; 
    width: 100%;
    background: white;
    padding: 10px 0;
    border-top: 1px solid #ddd;
    display: flex;
    justify-content: space-around;
}
.navbutton {
    background: #f0f0f0;
    padding: 10px 20px;
    border-radius: 10px;
    text-align: center;
    font-weight: 600;
    color: #333;
    cursor: pointer;
    border: 1px solid #ccc;
}
.navbutton:hover {
    background: #e4e4e4;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="navbar">
        <div class="navbutton" onclick="window.location.href='?page=Temperature'">Temperature</div>
        <div class="navbutton" onclick="window.location.href='?page=Humidity'">Humidity</div>
        <div class="navbutton" onclick="window.location.href='?page=History'">History</div>
        <div class="navbutton" onclick="window.location.href='?page=Settings'">Settings</div>
    </div>
    """,
    unsafe_allow_html=True
)
