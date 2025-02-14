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
    xaxis=dict(
        tickmode="array",
        tickvals=list(range(len(week_columns))),
        ticktext=week_columns,
        tickangle=45,  # Optional: Drehen Sie die Beschriftungen für bessere Lesbarkeit
        tickfont=dict(size=10)
    ),
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

# Funktion zum Hinzufügen eines roten Rahmens um eine spezifische Zelle
def add_red_border(fig, x_coord, y_coord):
    fig.add_shape(
        type="rect",
        x0=x_coord - 0.5, y0=y_coord - 0.5,
        x1=x_coord + 0.5, y1=y_coord + 0.5,
        line=dict(color="red", width=2),
        fillcolor="rgba(0,0,0,0)",
        layer="above"
    )

# Koordinaten für die spezifischen Zellen finden
first_week_index = week_columns.index("Week 1")
last_week_index = week_columns.index("Week 40")

abdurrahim_index = names_sorted.index("Abdurrahim")
anil_index = names_sorted.index("Anil")
abdulhalim_index = names_sorted.index("Abdulhalim")
khyalla_index = names_sorted.index("Khyalla")

# Rote Rahmen hinzufügen
add_red_border(fig, last_week_index, abdurrahim_index)
add_red_border(fig, last_week_index, anil_index)
add_red_border(fig, last_week_index, abdulhalim_index)
add_red_border(fig, first_week_index, khyalla_index)

# Heatmap in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=True)