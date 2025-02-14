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

# Durchschnittliche Arbeitsstunden pro Woche pro Position berechnen
df_avg = df.groupby("Position")[weeks].mean().reset_index()
df_avg["Average_Stunden"] = df_avg[weeks].mean(axis=1)

# Anzahl der Personen pro Position berechnen
position_counts = df["Position"].value_counts().to_dict()

# Nach Durchschnitt sortieren
df_avg = df_avg.sort_values(by="Average_Stunden", ascending=False)

# Farben definieren
colors = ["#1b9e77", "#d95f02", "#7570b3", "#984ea3", "#ff7f00", "#ffff33", "#a65628"]

# Balkendiagramm erstellen
fig = go.Figure()

# Für jede Position eine separate Spur erstellen
for i, position in enumerate(df_avg["Position"]):
    anzahl_personen = position_counts.get(position, 0)  # Anzahl der Personen in der Position
    fig.add_trace(go.Bar(
        x=[position],  # Nur eine Position pro Spur
        y=[df_avg.loc[df_avg["Position"] == position, "Average_Stunden"].values[0]],
        name=f"{position} ({anzahl_personen} Personen)",  # Legendenname mit Anzahl der Personen
        marker=dict(color=colors[i % len(colors)]),
        width=0.7,  # Balkenbreite
        showlegend=True  # Legende für diese Spur anzeigen
    ))

# Layout anpassen
fig.update_layout(
    title="Durchschnittliche Arbeitsstunden pro Woche pro Position",
    xaxis_title="Position",
    yaxis_title="Durchschnittliche Arbeitsstunden",
    xaxis=dict(
        tickmode='array',
        tickvals=df_avg["Position"],
        ticktext=df_avg["Position"],
        tickfont=dict(size=14)  # Schriftgröße der X-Achsen-Beschriftung
    ),
    yaxis=dict(
        tickfont=dict(size=12)  # Schriftgröße der Y-Achsen-Beschriftung
    ),
    height=700,  # Höhe des Diagramms
    width=500,  # Breite des Diagramms
    legend=dict(
        title="Positionen",
        font=dict(size=12)  # Schriftgröße der Legende
    ),
    barmode='group'  # Balken gruppieren
)

# Balkendiagramm in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=False)  # `use_container_width=False`, damit Breite greift
