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



# Daten abrufen
data = fetch_all_hours_worked_data()

# Daten in ein DataFrame umwandeln
df = pd.DataFrame(data)

# Spalten für die Wochen extrahieren
weeks = [col for col in df.columns if col.startswith("Week")]

# Summe der Arbeitsstunden pro Person berechnen
df["Total Hours"] = df[weeks].sum(axis=1)

# Nach der Gesamtarbeitszeit absteigend sortieren
df_sorted = df.sort_values(by="Total Hours", ascending=False)

# Heatmap-Daten vorbereiten
heatmap_data = df_sorted[weeks].values
names_sorted = df_sorted["Name"]

# Heatmap mit Plotly erstellen
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,  # Arbeitsstunden
    x=weeks,         # Wochen auf der X-Achse
    y=names_sorted,  # Sortierte Namen auf der Y-Achse
    colorscale="Viridis",  # Farbschema
    colorbar=dict(title="Arbeitsstunden")  # Legende
))

# Layout anpassen
fig.update_layout(
    title="Arbeitsstunden pro Woche (sortiert nach Gesamtarbeitszeit)",
    xaxis_title="Woche",
    yaxis_title="Name",
    xaxis_nticks=len(weeks),  # Anzahl der Wochenbeschriftungen
    yaxis_nticks=len(names_sorted)   # Anzahl der Namensbeschriftungen
)

# Heatmap in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=True)