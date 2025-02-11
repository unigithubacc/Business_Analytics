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
data = fetch_arbeitszeiten_days_data()

# Daten in ein DataFrame umwandeln
df = pd.DataFrame(data)

# Wochentage definieren
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Gesamtarbeitsstunden pro Person berechnen
df["Total Hours"] = df[weekdays].sum(axis=1)

# Nach der Gesamtarbeitszeit absteigend sortieren
df_sorted = df.sort_values(by="Total Hours", ascending=False)

# Heatmap-Daten vorbereiten (Transponiert, um Namen auf der X-Achse und Wochentage auf der Y-Achse anzuzeigen)
heatmap_data = df_sorted[weekdays].T.values  # Transposition
names_sorted = df_sorted["Name"].tolist()

# Heatmap mit Plotly erstellen
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,          # Arbeitsstunden
    x=names_sorted,          # Sortierte Namen auf der X-Achse
    y=weekdays,              # Wochentage auf der Y-Achse
    colorscale="Viridis",   # Farbschema
    colorbar=dict(
        title="Arbeitsstunden", 
        tickmode="auto",    # Automatische Tick-Einstellung
        ticks="outside"     # Ticks außerhalb anzeigen
    )
))

# Layout anpassen
fig.update_layout(
    title="Arbeitsstunden pro Wochentag und Person (sortiert nach Gesamtarbeitszeit)",
    xaxis_title="Name",
    yaxis_title="Wochentag",
    xaxis_nticks=len(names_sorted),
    yaxis=dict(
        automargin=True,
        tickmode="array",
        tickvals=list(range(len(weekdays))),
        ticktext=weekdays,
        tickangle=0,
        tickfont=dict(size=10)
    ),
    margin=dict(l=150, r=50, t=50, b=150),
    height=600
)

# Heatmap in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=True)