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

# Daten abrufen
data = fetch_all_hours_worked_data()

# Überprüfen, ob Daten vorhanden sind
if data:
    # In DataFrame umwandeln
    df = pd.DataFrame(data)

    # Melt für Heatmap
    df_melted = df.melt(id_vars=["Name"], value_vars=[f"Week {i}" for i in range(1, 40)],
                        var_name="Week", value_name="Hours Worked")

    # Pivot-Tabelle erstellen
    heatmap_data = df_melted.pivot(index="Name", columns="Week", values="Hours Worked")

    # Plotly Heatmap erstellen
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlGnBu',
        colorbar=dict(title='Hours Worked')
    ))

    fig.update_layout(
        title="Weekly Hours Worked per Employee",
        xaxis_title="Week",
        yaxis_title="Name"
    )

    # Heatmap anzeigen
    st.plotly_chart(fig)
else:
    st.warning("No data available to display.")
