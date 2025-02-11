import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd


@st.cache_data
def fetch_arbeitszeiten_days_data() -> dict:
    response = requests.get('http://localhost:8000/arbeitszeiten-days')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data.")
        return {}

@st.cache_data
def fetch_all_hours_worked_data() -> dict:
    response = requests.get('http://localhost:8000/all-hours-worked')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data.")
        return {}

@st.cache_data
def fetch_abteilung_data() -> dict:
    response = requests.get('http://localhost:8000/Abteilung')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data.")
        return {}


st.title("Hello World page 2")



