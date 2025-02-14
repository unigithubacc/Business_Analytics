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

# Anzahl der Personen pro Abteilung berechnen
abteilung_counts = df["Abteilung"].value_counts().to_dict()

# Nach Durchschnitt sortieren
df_avg = df_avg.sort_values(by="Average_Stunden", ascending=False)

# Farben definieren
colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628"]

# Balkendiagramm erstellen
fig = go.Figure()

# Für jede Abteilung eine separate Spur erstellen
for i, abteilung in enumerate(df_avg["Abteilung"]):
    anzahl_personen = abteilung_counts.get(abteilung, 0)  # Anzahl der Personen in der Abteilung
    fig.add_trace(go.Bar(
        x=[abteilung],  # Nur eine Abteilung pro Spur
        y=[df_avg.loc[df_avg["Abteilung"] == abteilung, "Average_Stunden"].values[0]],
        name=f"{abteilung} ({anzahl_personen} Personen)",  # Legendenname mit Anzahl der Personen
        marker=dict(color=colors[i % len(colors)]),  # Farbe zuweisen
        width=0.7,  # Balkenbreite
        showlegend=True  # Legende für diese Spur anzeigen
    ))

# Layout anpassen
fig.update_layout(
    title="Durchschnittliche Arbeitsstunden pro Woche pro Abteilung",
    xaxis_title="Abteilung",
    yaxis_title="Durchschnittliche Arbeitsstunden",
    xaxis=dict(
        tickmode='array',
        tickvals=df_avg["Abteilung"],
        ticktext=df_avg["Abteilung"],
        tickfont=dict(size=14)  # Schriftgröße der X-Achsen-Beschriftung
    ),
    yaxis=dict(
        tickfont=dict(size=12)  # Schriftgröße der Y-Achsen-Beschriftung
    ),
    height=700,  # Höhe des Diagramms anpassen
    width=700,  # Breite des Diagramms anpassen
    legend=dict(
        title="Abteilungen (Anzahl Personen)",
        font=dict(size=12)  # Schriftgröße der Legende
    ),
    barmode='group'  # Balken gruppieren
)

# Balkendiagramm in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=False)  # `use_container_width=False` damit Breite greift
