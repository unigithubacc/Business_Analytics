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

# Durchschnitt der Arbeitsstunden pro Projekt berechnen
df_avg = df.groupby("Projekt")[weeks].mean().reset_index()

# Anzahl der Personen pro Projekt berechnen
projekt_counts = df["Projekt"].value_counts().to_dict()

# Farben definieren
colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3"]

# Liniendiagramm erstellen
fig = go.Figure()

# Für jedes Projekt eine Linie hinzufügen
for i, projekt in enumerate(df_avg["Projekt"].unique()):
    anzahl_personen = projekt_counts.get(projekt, 0)
    fig.add_trace(go.Scatter(
        x=weeks,
        y=df_avg[df_avg["Projekt"] == projekt][weeks].values.flatten(),
        mode='lines+markers',
        name=f"{projekt} ({anzahl_personen} Personen)",  # Anzahl der Personen in der Legende
        line=dict(color=colors[i % len(colors)])  # Farben zuweisen
    ))

# Layout anpassen
fig.update_layout(
    title="Durchschnittliche Arbeitsstunden pro Woche nach Projekt",
    xaxis_title="Woche",
    yaxis_title="Arbeitsstunden",
    xaxis=dict(tickmode='linear'),
    legend_title="Projekt (Anzahl Personen)",
    height=600
)

# Liniendiagramm in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=True)