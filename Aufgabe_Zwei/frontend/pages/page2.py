import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

@st.cache_data
def fetch_all_hours_worked_data() -> dict:
    response = requests.get('http://localhost:8000/all-hours-worked')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data.")
        return {}

# Daten abrufen
data = fetch_all_hours_worked_data()

# In DataFrame umwandeln
df = pd.DataFrame(data)

# Wochen-Spalten identifizieren
week_columns = [col for col in df.columns if col.startswith("Week")]

# Gesamtarbeitszeit pro Person berechnen
df["Total Hours"] = df[week_columns].sum(axis=1)

# Nach der Gesamtarbeitszeit absteigend sortieren
df_sorted = df.sort_values(by="Total Hours", ascending=False)

# Doppelte Namen eindeutig machen
name_counts = {}
def unique_name(name):
    if name in name_counts:
        name_counts[name] += 1
        return f"{name}{name_counts[name]}"
    else:
        name_counts[name] = 0
        return name

df_sorted["Unique Name"] = df_sorted["Name"].apply(unique_name)
names_sorted = df_sorted["Unique Name"].tolist()

# Heatmap-Daten vorbereiten (Transponieren für richtige Ausrichtung)
heatmap_data = df_sorted[week_columns].values  # Reihenfolge bleibt gleich

# Heatmap mit Plotly erstellen
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,          # Arbeitsstunden
    x=week_columns,          # Wochen auf der X-Achse
    y=names_sorted,          # Sortierte eindeutige Namen auf der Y-Achse
    colorscale="Viridis",   # Farbschema
    colorbar=dict(
        title="Arbeitsstunden", 
        tickmode="auto",    # Automatische Tick-Einstellung
        ticks="outside"     # Ticks außerhalb anzeigen
    )
))

# Layout anpassen
fig.update_layout(
    title="Arbeitsstunden pro Woche und Person (sortiert nach Gesamtarbeitszeit)",
    xaxis_title="Woche",
    yaxis_title="Mitarbeiter",
    xaxis_nticks=len(week_columns),
    yaxis=dict(
        automargin=True,
        tickmode="array",
        tickvals=list(range(len(names_sorted))),
        ticktext=names_sorted,
        tickangle=0,
        tickfont=dict(size=10)
    ),
    margin=dict(l=150, r=50, t=50, b=150),
    height=800
)

# Heatmap in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=True)
