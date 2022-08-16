import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Page configuration and title
st.set_page_config(page_title='Map Testing', layout='wide', page_icon="🌍")
# st.markdown("<h1 style='text-align: center; color: #666666;'>Map Testing.</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([1,10])

# Type of graph
plot = col1.radio(
     "Graph:",
     ("Population", "Rent House", "Buy House"))

# geojson load
# Preparamos el GeoJSON
provincias = json.load(open("./data/raw sources/provincias-espanolas.geojson", "r"))
provincias_id = {}
for feature in provincias["features"]:
    feature["id"] = feature["properties"]["codigo"]
    provincias_id[feature["properties"]["provincia"]] = feature["id"]
provincias_id['Baleares'] = provincias_id.pop('Illes Balears')
provincias_id['Vizcaya'] = provincias_id.pop('Bizkaia')
provincias_id['Alicante/Alacant'] = provincias_id.pop('Alacant')
provincias_id['Castellón/Castelló'] = provincias_id.pop('Castelló')
provincias_id['Álava'] = provincias_id.pop('Araba')
provincias_id['Guipúzcoa'] = provincias_id.pop('Gipuzcoa')

if plot == "Population":
    # Dataset load
    df = pd.read_pickle("data/pop_df.pkl")
    fig = px.density_mapbox(df, lat="lat", lon="lng", z="population_log"
                        ,hover_name='city'
                        ,center=dict(lat=39.3, lon=-4.2)
                        ,hover_data= ['population']
                        ,zoom=5
                        ,radius=df["population_log"]*4
                        ,opacity=0.5
                        ,mapbox_style='open-street-map'
                        ,height=875
                        ,title="<b>Spanish population by city</b>"
                        )
    fig.update_layout(title={'font': {'size': 50}})

elif plot == "Rent House":
    df = pd.read_pickle("data/rent_df.pkl")
    fig = px.choropleth(df,locations="id", color="Rent 100m2 house",
                        geojson=provincias,
                        hover_name="Localización",
                        height=800
                        ,title="<b>Rent by province in Spain</b>"
                        )             
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title={'font': {'size': 50}})

else:
    df = pd.read_pickle("data/buy_df.pkl")
    fig = px.choropleth(df,locations="id", color="Buy 100m2 house",
                        geojson=provincias,
                        hover_name="Localización",
                        height=800
                        ,title="<b>House price by province in Spain</b>"
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title={'font': {'size': 50}})

col2.plotly_chart(fig, use_container_width=True)
