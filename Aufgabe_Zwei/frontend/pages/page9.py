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

# Filter für Geschäftsführung und Heads setzen
df_filtered = df[(df['Abteilung'] == 'Geschäftsführung') | (df['Position'] == 'Head')]

# Anzahl der Personen pro Standort ermitteln
location_counts = df_filtered['Standort'].value_counts().to_dict()

# Anzahl der Heads und Geschäftsführung pro Standort ermitteln
heads_counts = df_filtered[df_filtered['Position'] == 'Head']['Standort'].value_counts().to_dict()
gf_counts = df_filtered[df_filtered['Abteilung'] == 'Geschäftsführung']['Standort'].value_counts().to_dict()

# Labels mit detaillierten Informationen erstellen
labels = []
values = []
for location, count in location_counts.items():
    heads = heads_counts.get(location, 0)
    gf = gf_counts.get(location, 0)
    labels.append(f"{location}: {count}\n(Heads: {heads}, GF: {gf})")
    values.append(count)

# Kreisdiagramm erstellen
fig = go.Figure()
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.3,  # Für ein Donut-Diagramm
    marker=dict(colors=['#66a61e', '#e7298a']),
    textinfo='label+percent',  # Zeigt Labels und Anzahl an
))

# Layout anpassen
fig.update_layout(
    title="Anzahl der Geschäftsführung und Heads nach Standort"
)

# Diagramm in Streamlit anzeigen
st.plotly_chart(fig, use_container_width=True)
