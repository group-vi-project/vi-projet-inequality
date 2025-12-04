# app.py
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd
import random
import folium
import mapclassify

geofile_path = "2025_GEOM_TK/03_ANAL/Gesamtfläche_gf/K4_greg20001205_gf/K4greg20001205gf_ch2007Poly.shp"

gdf = gpd.read_file(geofile_path)
# gdf["id"] = gdf["name"]
# # create a geojson mapping
# geojson = gdf.set_index('id').__geo_interface__  # adjust name column
m = gdf.explore('id')
# prepare data

app = Dash(__name__)
app.layout = html.Div([
    html.H4('Salary Inequality Map of Switzerland'),
    html.P("Select your options:"),
    html.Iframe(srcDoc = open('map.html', 'r').read(),
                         style={
        'width': '100%',
        'height': '100vh',
        'border': 'none'
    })
])

app.run(debug=True)
