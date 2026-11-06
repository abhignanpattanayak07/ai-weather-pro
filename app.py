import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------
# LOAD ENV
# -------------------
load_dotenv()
WEATHER_API = os.getenv("WEATHER_API")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="Weather Pro AI", page_icon="🌦️", layout="wide")

# -------------------
# WEATHER FUNCTION
# -------------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None

# -------------------
# AI CHAT (GEMINI)
# -------------------
def ask_ai(prompt):
    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content(prompt)
    return response.text

# -------------------
# UI
# -------------------
st.title("🌦️ AI Weather Pro Assistant")

city = st.text_input("Enter City")

if st.button("Get Weather"):
    data = get_weather(city)

    if data:
        st.success(f"Weather for {city}")

        temps = []
        times = []

        for item in data["list"][:10]:
            temps.append(item["main"]["temp"])
            times.append(item["dt_txt"])

        # -------------------
        # METRICS
        # -------------------
        st.metric("🌡️ Current Temp", f"{temps[0]} °C")

        # -------------------
        # CHART
        # -------------------
        df = pd.DataFrame({
            "Time": times,
            "Temperature": temps
        })

        fig = px.line(df, x="Time", y="Temperature", title="Temperature Forecast")
        st.plotly_chart(fig, use_container_width=True)

        # -------------------
        # LIVE MAP
        # -------------------
        st.subheader("🌍 Live Weather Map")
        map_url = f"https://openweathermap.org/weathermap?basemap=map&cities=true&layer=temperature&lat=22.57&lon=88.36&zoom=5"
        st.markdown(f"[Open Live Map]({map_url})")

        # Save state
        st.session_state.weather_data = temps[0]

    else:
        st.error("City not found")

# -------------------
# AI CHATBOT
# -------------------
st.subheader("🤖 AI Weather Chatbot")

user_input = st.text_input("Ask anything about weather")

if st.button("Ask AI"):
    if user_input:
        response = ask_ai(user_input)
        st.success(response)