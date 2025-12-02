import streamlit as st
import smtplib
from datetime import datetime, timedelta
from storage import load_settings, save_settings
from Data_readings import load_google_sheets
from streamlit_autorefresh import st_autorefresh
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


if "user_email" not in st.session_state:
  st.session_state.user_email = None

sender_email = "ctrlaltelite.alertsystem@gmail.com"
rec_email = st.session_state.user_email
valid_pass = "zrea mfjb ougy jzti"

# -----------------------------
# ALARM LOGIC
# -----------------------------

def send_alert(subject, body, sender, receiver_email, app_password):
      msg = MIMEMultipart()
      msg["From"] = sender
      msg["To"] = receiver_email
      msg["Subject"] = subject  

      msg.attach(MIMEText(body, "plain", "utf-8"))

      server = smtplib.SMTP('smtp.gmail.com',587)
      server.starttls()
      server.login(sender_email,app_password)
      server.sendmail(sender_email,rec_email,msg.as_string())

# -----------------------------
# NOTIFICATIONS INTERVAL + LOGIC
# -----------------------------

if "last_temp1_email" not in st.session_state:
    st.session_state.last_temp1_email = None

if "last_temp2_email" not in st.session_state:
    st.session_state.last_temp2_email = None

if "last_hum1_email" not in st.session_state:
    st.session_state.last_hum1_email = None

if "last_hum2_email" not in st.session_state:
    st.session_state.last_hum2_email = None
  

def should_send_email(last_time, interval_minutes):
    if last_time is None:
        return True
    return datetime.now() - last_time >= timedelta(minutes=interval_minutes)

# -----------------------------
# AUTHENTIFICATION
# -----------------------------

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Veuillez vous connecter pour accéder à l'application.")
    st.switch_page("streamlit_app_login.py")

# -----------------------------
# DATA READINGS
# -----------------------------

def latest_value(sensor):
    df = load_google_sheets(5)
    latest = df.iloc[-1][sensor]
    return latest

def realtime_monitor_temp():
  temp1 = latest_value(1)

  temp2 = latest_value(3)
  

  temp_threshold = st.session_state.settings["temp_threshold"]
  
  EMAIL_INTERVAL_MINUTES = st.session_state.settings["alert_interval"]

  if (temp1 >= temp_threshold):
      alert_msg = (f"⚠️ Alerte: Température {temp1}°C du capteur 1 dépasse le seuil ({temp_threshold}°C)!")
      st.error(alert_msg)
      
      if should_send_email(st.session_state.last_temp1_email, EMAIL_INTERVAL_MINUTES):
            send_alert("Alerte de température!", alert_msg, sender_email, rec_email, valid_pass)
            st.session_state.last_temp1_email = datetime.now()
  
  if (temp2 >= temp_threshold):
      alert_msg = (f"⚠️ Alerte: Température {temp2}°C du capteur 2 dépasse le seuil ({temp_threshold}°C)!")
      st.error(alert_msg)

      if should_send_email(st.session_state.last_temp2_email, EMAIL_INTERVAL_MINUTES):
            send_alert("Alerte de température!", alert_msg, sender_email, rec_email, valid_pass)
            st.session_state.last_temp2_email = datetime.now()



def realtime_monitor_hum():
  
  hum1 = latest_value(2)
  hum2 = latest_value(4)
  hum_threshold = st.session_state.settings["hum_threshold"]

  EMAIL_INTERVAL_MINUTES = st.session_state.settings["alert_interval"]

  if (hum1 >= hum_threshold):
      alert_msg = (f"⚠️ Alerte: Humidite {hum1}% du capteur 1 dépasse le seuil ({hum_threshold}%)!")
      st.error(alert_msg)

      if should_send_email(st.session_state.last_hum1_email, EMAIL_INTERVAL_MINUTES):
            send_alert("Alerte d'humidité!", alert_msg, sender_email, rec_email, valid_pass)
            st.session_state.last_hum1_email = datetime.now()
  
  if (hum2 >= hum_threshold):
      alert_msg = (f"⚠️ Alerte: Humidite {hum2}% du capteur 2 dépasse le seuil ({hum_threshold}%)!")
      st.error(alert_msg)

      if should_send_email(st.session_state.last_hum2_email, EMAIL_INTERVAL_MINUTES):
            send_alert("Alerte d'humidité!", alert_msg, sender_email, rec_email, valid_pass)
            st.session_state.last_hum2_email = datetime.now()

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
# STATUS LOGIC
# -----------------------------

def status(threshold, value):

    if value < (threshold - 10):
        text = "Bon"
  
    elif (threshold - 10) <= value < (threshold):
        text = "Moyen"
        
    else:
        text = "En danger!"
    
    return text

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
            <p style="margin: 4px 0; color: white;">État: <b>{avg_value}</b></p>
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
        avg_value=status(st.session_state.settings["temp_threshold"], latest_value(1)),
        extra_info=f"Dernière mise à jour: {latest_value(0)}"
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
        avg_value=status(st.session_state.settings["hum_threshold"], latest_value(2)),
        extra_info=f"Dernière mise à jour: {latest_value(0)}"
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
        extra_info="État - Temp: " + status(st.session_state.settings["temp_threshold"], latest_value(1)) +" | Hum: " + status(st.session_state.settings["hum_threshold"], latest_value(2)) 
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

# -----------------------------
# Autorefresh every 3 seconds
# -----------------------------

# TEMPERATURE

def settings_page():
    st_autorefresh(10000, key="refresh")
    top_section_settings(
        title="Paramètres",
        extra_info="État - Temp: " + status(st.session_state.settings["temp_threshold"], latest_value(1)) +" | Hum: " + status(st.session_state.settings["hum_threshold"], latest_value(2)) 
    )

    st.write("")
    st.markdown("<h3 style='color:#000;'>Température (°C):</h3>", unsafe_allow_html=True)

    if "temp_slider" not in st.session_state:
        st.session_state.temp_slider = st.session_state.settings["temp_threshold"]

    temp = st.slider(
        "Seuil de Température (°C)",
        min_value=-40,
        max_value=100, #En temps normal, la température interne d'un réfrigérateur devrait se situer entre 1.7°C et 3.3°C (mais pour la démo, on la garde à 100)
        key = "temp_slider"
    )

    st.write("Seuil d'alerte:", temp)

    if temp != st.session_state.settings["temp_threshold"]:
        st.session_state.settings["temp_threshold"] = temp
        save_settings(st.session_state.settings)
        st.success("Paramètres sauvegardés!")
      
    realtime_monitor_temp()

#   HUMIDITÉ

    st.markdown("<h3 style='color:#000;'>Humidité (%):</h3>", unsafe_allow_html=True)

    if "hum_slider" not in st.session_state:
        st.session_state.hum_slider = st.session_state.settings["hum_threshold"]

    hum = st.slider(
        "Seuil d'Humidité (%)",
        min_value=0,
        max_value=100,
        key = "hum_slider"
    )

    st.write("Seuil d'alerte:", hum)
    
    if hum != st.session_state.settings["hum_threshold"]:
        st.session_state.settings["hum_threshold"] = hum
        save_settings(st.session_state.settings)
        st.success("Paramètres sauvegardés!")
    
    realtime_monitor_hum()

#   ALERTES

    st.markdown("<h3 style='color:#000;'>Alertes ⚠️:</h3>", unsafe_allow_html=True)

    if "alert_interval" not in st.session_state.settings:
      st.session_state.settings["alert_interval"] = 5.0  

    if "alert_interval_input" not in st.session_state:
        st.session_state.alert_interval_input = st.session_state.settings["alert_interval"]

    intervalle = st.number_input("Intervalle des notifications (minutes):", 
                                 value=st.session_state.settings["alert_interval"],
                                 min_value=0.0,
                                 step=0.25, 
                                 icon="🚨", 
                                 format="%0.2f",
                                 key="alert_interval_input")

    if intervalle != st.session_state.settings["alert_interval"]:
      st.session_state.settings["alert_interval"] = intervalle
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
