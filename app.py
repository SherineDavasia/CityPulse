import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os
from twilio.rest import Client


st.set_page_config(page_title="CityPulse - Live AQI", layout="centered")

st.title("🌆 CityPulse - Live Air Quality Tracker")

# Input fields
city = st.text_input("City", "Moradabad")
state = st.text_input("State", "Uttar Pradesh")
country = st.text_input("Country", "India")

# API Key
api_key = "56f20452-9276-4c35-91c8-a1bacb4cb32f"

if st.button("Get AQI"):
    url = f"https://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    try:
        # ✅ Check if API response is successful
        if data.get("status") != "success":
            raise Exception("API error: " + data.get("data", {}).get("message", "Unknown error"))

        # ✅ Extract AQI value
        aqi = data['data']['current']['pollution']['aqius']
        st.metric(label="Current AQI", value=aqi)

        # ✅ Health Tip Generator
        def get_health_advice(aqi):
            if aqi <= 50:
                return "🟢 Good – Enjoy your outdoor activities!", "green"
            elif aqi <= 100:
                return "🟡 Moderate – Acceptable air quality.", "yellow"
            elif aqi <= 150:
                return "🟠 Unhealthy for Sensitive Groups – Consider reducing outdoor exertion.", "orange"
            elif aqi <= 200:
                return "🔴 Unhealthy – Avoid outdoor activity.", "red"
            elif aqi <= 300:
                return "🟣 Very Unhealthy – Health alert: everyone may experience serious effects.", "purple"
            else:
                return "⚫ Hazardous – Stay indoors, wear a mask.", "maroon"

        # ✅ Show tip
        tip, color = get_health_advice(aqi)
        st.markdown(
            f"<div style='color:{color}; font-weight:bold; font-size:18px'>{tip}</div>",
            unsafe_allow_html=True
        )

        # ✅ Log AQI with timestamp
        log_file = "aqi_log.csv"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = pd.DataFrame([[current_time, aqi]], columns=["timestamp", "aqi"])

        if os.path.exists(log_file):
            old_data = pd.read_csv(log_file)
            updated_data = pd.concat([old_data, new_entry], ignore_index=True)
        else:
            updated_data = new_entry

        updated_data.to_csv(log_file, index=False)

        # ✅ Line Chart
        st.line_chart(updated_data.set_index("timestamp")["aqi"])

    except Exception as e:
        st.error(f"❌ Could not retrieve AQI. Error: {e}")

