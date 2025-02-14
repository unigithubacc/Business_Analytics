import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

@st.cache_data
def fetch_abteilung_data() -> dict:
    response = requests.get('http://localhost:8000/Abteilung')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data.")
        return {}

# Daten abrufen
data = fetch_abteilung_data()

# Daten in ein DataFrame umwandeln
df = pd.DataFrame(data)

# Wochen-Spalten identifizieren
weeks = [col for col in df.columns if col.startswith("Week")]

# Durchschnittliche Arbeitsstunden pro Woche pro Abteilung berechnen
df_avg = df.groupby("Abteilung")[weeks].mean().reset_index()
df_avg["Average_Stunden"] = df_avg[weeks].mean(axis=1)

# Nach Durchschnitt sortieren
df_avg = df_avg.sort_values(by="Average_Stunden", ascending=False)

# Anzahl der Personen pro Abteilung berechnen
abteilung_counts = df["Abteilung"].value_counts().to_dict()

# Farben definieren
colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628"]

# Balkendiagramm erstellen
fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_avg["Abteilung"],
    y=df_avg["Average_Stunden"],
    text=[f"{abteilung} ({abteilung_counts.get(abteilung, 0)} Personen)" for abteilung in df_avg["Abteilung"]],
    textposition='auto',
    marker=dict(color=colors[:len(df_avg["Abteilung"])])
))

# Layout anpassen
fig.update_layout(
    title="Durchschnittliche Arbeitsstunden pro Woche pro Abteilung",
    xaxis_title="Abteilung",
    yaxis_title="Durchschnittliche Arbeitsstunden",
    xaxis=dict(tickmode='array', tickangle=45),
    height=600,
    legend_title="Abteilungen"
)

# Balkendiagramm in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=True)