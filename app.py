import streamlit as st
from datetime import datetime
from storage import load_settings, save_settings

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

if "settings_loaded" not in st.session_state:
    st.session_state.settings = load_settings()
    st.session_state.settings_loaded = True


# -----------------------------
# SHARED TOP BAR
# -----------------------------
def top_section(title, avg_value, extra_info):
    st.markdown(
        f"""
        <div style="padding: 15px; 
                    background-color: #00A4FC; 
                    border-radius: 12px; 
                    border: 1px solid #e1e1e1;">
            <h2 style="margin: 0; color: white;">{title}</h2>
            <p style="margin: 4px 0; color: white;">Heure Actuelle: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p style="margin: 4px 0; color: white;">Moyenne: <b>{avg_value}</b></p>
            <p style="margin: 4px 0; color: white;">{extra_info}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# TOP SETTINGS BAR 
# -----------------------------

def top_section_settings(title, extra_info):
    st.markdown(
        f"""
        <div style="padding: 15px; 
                    background-color: #00A4FC; 
                    border-radius: 12px; 
                    border: 1px solid #e1e1e1;">
            <h2 style="margin: 0; color: white;">{title}</h2>
            <p style="margin: 4px 0; color: white;">Date Actuelle: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p style="margin: 4px 0; color: white;">{extra_info}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# PAGE: TEMPERATURE
# -----------------------------
def temperature_page():
    top_section(
        title="Température",
        avg_value="-- °C",
        extra_info="Dernière mise à jour: Automatiquement depuis ThingSpeak"
    )

    st.write("")
    st.markdown("### Graphique de la température")

    # Temperature iframe
    html = """
    <style>
      .scrollbox {
        height: 560px;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 12px;
        box-sizing: border-box;
      }
      .chart {
        width: 100%;
        max-width: 450px; 
        margin: 12px auto;
        border: 1px solid #cccccc;
        border-radius: 8px;
        padding: 8px;
        background: #fff;
      }
      .chart h4 {
        margin: 8px 12px;
        font-family: Arial, sans-serif;
      }
      /* scrollbar styling (optional) */
      .scrollbox::-webkit-scrollbar { width: 10px; }
      .scrollbox::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 5px; }
    </style>

    <div class="scrollbox">
      <div class="chart">
        <h4>Graphique de la température (Capteur 1)</h4>
        <iframe width="100%" height="260" style="border:0"
          src="https://thingspeak.com/channels/3163867/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
      </div>

      <div class="chart">
        <h4>Graphique de la température (Capteur 2)</h4>
        <iframe width="100%" height="260" style="border:0"
          src="https://thingspeak.com/channels/3163867/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
      </div>

    </div>
    """

    st.components.v1.html(html, height=600, scrolling=True)


# -----------------------------
# PAGE: HUMIDITY
# -----------------------------
def humidity_page():
    top_section(
        title="Humidité",
        avg_value="-- %",             
        extra_info="Dernière mise à jour: Automatiquement depuis ThingSpeak"
    )

    st.write("")
    st.markdown("### Graphique de l'humidité")

    # Humidity iframe
    html = """
    <style>
      .scrollbox {
        height: 560px;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 12px;
        box-sizing: border-box;
      }
      .chart {
        width: 100%;
        max-width: 450px; 
        margin: 12px auto;
        border: 1px solid #cccccc;
        border-radius: 8px;
        padding: 8px;
        background: #fff;
      }
      .chart h4 {
        margin: 8px 12px;
        font-family: Arial, sans-serif;
      }
      /* scrollbar styling (optional) */
      .scrollbox::-webkit-scrollbar { width: 10px; }
      .scrollbox::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 5px; }
    </style>

      <div class="chart">
        <h4>Graphique de l'humidité (Capteur 1)</h4>
        <iframe width="100%" height="260" style="border:0"
          src="https://thingspeak.com/channels/3163867/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
      </div>

      <div class="chart">
        <h4>Graphique de l'humidité (Capteur 2)</h4>
        <iframe width="100%" height="260" style="border:0"
          src="https://thingspeak.com/channels/3163867/charts/4?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
      </div>

      <!-- add more charts here if needed -->
    </div>
    """

    st.components.v1.html(html, height=600, scrolling=True)


# -----------------------------
# PAGE: HISTORY
# -----------------------------
def history_page():
    top_section_settings(
        title="Historique",
        extra_info="Dernière mise à jour: 2025-11-15 12:00:00"
    )

    st.write("")

    html = """
    <style>
      .scrollbox {
        height: 560px;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 12px;
        box-sizing: border-box;
      }
      .chart {
        width: 100%;
        max-width: 450px; 
        margin: 12px auto;
        border: 1px solid #cccccc;
        border-radius: 8px;
        padding: 8px;
        background: #fff;
      }
      .chart h4 {
        margin: 8px 12px;
        font-family: Arial, sans-serif;
      }
      /* scrollbar styling (optional) */
      .scrollbox::-webkit-scrollbar { width: 10px; }
      .scrollbox::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 5px; }
    </style>

    <div class="scrollbox">
      <div class="chart">
        <h4>Graphique de la température (Capteur 1)</h4>
        <iframe width="100%" height="260" style="border:0"
          src="https://thingspeak.com/channels/3163867/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
      </div>

      <div class="chart">
        <h4>Graphique de l'humidité (Capteur 1)</h4>
        <iframe width="100%" height="260" style="border:0"
          src="https://thingspeak.com/channels/3163867/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
      </div>

      <div class="chart">
        <h4>Graphique de la température (Capteur 2)</h4>
        <iframe width="100%" height="260" style="border:0"
          src="https://thingspeak.com/channels/3163867/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
      </div>

      <div class="chart">
        <h4>Graphique de l'humidité (Capteur 2)</h4>
        <iframe width="100%" height="260" style="border:0"
          src="https://thingspeak.com/channels/3163867/charts/4?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
        </iframe>
      </div>

      <!-- add more charts here if needed -->
    </div>
    """

    st.components.v1.html(html, height=600, scrolling=True)


# -----------------------------
# PAGE: SETTINGS
# -----------------------------

# TEMPERATURE

def settings_page():
    top_section_settings(
        title="Paramètres",
        extra_info="Information Globale"
    )

    st.write("")
    st.markdown("<h3 style='color:#000;'>Température (°C):</h3>", unsafe_allow_html=True)

    temp = st.slider(
        "Seuil de Température (°C)",
        min_value=-40,
        max_value=100,
        value=st.session_state.settings["temp_threshold"]
    )

    st.write("Seuil d'alerte:", temp)

    if temp != st.session_state.settings["temp_threshold"]:
        st.session_state.settings["temp_threshold"] = temp
        save_settings(st.session_state.settings)
        st.success("Paramètres sauvegardés!")

#   HUMIDITÉ

    st.markdown("<h3 style='color:#000;'>Humidité (%):</h3>", unsafe_allow_html=True)

    hum = st.slider(
        "Seuil d'Humidité (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.settings["hum_threshold"]
    )

    st.write("Seuil d'alerte:", hum)
    
    if hum != st.session_state.settings["hum_threshold"]:
        st.session_state.settings["hum_threshold"] = hum
        save_settings(st.session_state.settings)
        st.success("Paramètres sauvegardés!")


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
    background-color: #195DB5;
    padding: 10px 0;
    border-top: 1px solid #ddd;
    display: flex;
    justify-content: space-around;
}
.navbutton button {
    background-color: #00A4FC ;
    border: 1px solid #0086D1 ;
    border-radius: 10px ;
    padding: 10px 20px ;
    color: white ;
    font-weight: 600 ;
}
</style>
""", unsafe_allow_html=True)


nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button("Température", icon=":material/device_thermostat:"):
        st.session_state.page = "Temperature"
        st.rerun()

with nav2:
    if st.button("Humidité", icon=":material/humidity_percentage:"):
        st.session_state.page = "Humidity"
        st.rerun()

with nav3:
    if st.button("Historique", icon=":material/history:"):
        st.session_state.page = "History"
        st.rerun()

with nav4:
    if st.button("Paramètres", icon=":material/settings:"):
        st.session_state.page = "Settings"
        st.rerun()
