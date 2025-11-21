# app.py
from dash import Dash, dcc, html
import plotly.express as px
import geopandas as gpd

geofile_path = "2025_GEOM_TK/03_ANAL/Gesamtfläche_gf/K4_greg20001205_gf/K4greg20001205gf_ch2007Poly.shp"

regions = gpd.read_file(geofile_path)
# create a geojson mapping
geojson = regions.set_index('name').__geo_interface__  # adjust name column

# For px.choropleth_mapbox we need locations matched to index keys:
regions['id'] = regions['name']  # ensure a string id
fig = px.choropleth_mapbox(
    regions,
    geojson=regions.__geo_interface__,
    locations='id',
    color=None,                # no color yet, just boundaries
    hover_name='name',
    mapbox_style="carto-positron",
    center={"lat": 46.8, "lon": 8.3},
    zoom=6
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app = Dash(__name__)
app.layout = html.Div([dcc.Graph(id='map', figure=fig)])

if __name__ == '__main__':
    app.run(debug=True)
