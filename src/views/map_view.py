from dash import html, dcc, Input, Output
import dash_mantine_components as dmc
import geopandas as gpd
import pandas as pd

from views.view import View

from common.constants import ComponentIds, ContainerIds
import common.components as components
import geopandas as gpd
geofile_path = "2025_GEOM_TK/03_ANAL/Gesamtfläche_gf/K4_greg20001205_gf/K4greg20001205gf_ch2007Poly.shp"
dfinq = pd.read_csv('data/inequality_by_region_position_year.csv')
dfinq_filtered = dfinq.loc[(dfinq["Year"] == 2022) & (dfinq["Position"] == "Sans fonction de cadre")]
gdf = gpd.read_file(geofile_path)
# print(gdf.columns)
# print(dfinq_filtered.columns)
# print(gdf['name'].head())
# print(dfinq_filtered['Region'].head())
gdf = gdf.merge(dfinq_filtered[['Region', 'Inequality']], left_on='name', right_on='Region', how='left')
gdf = gdf.drop(columns=['id', 'name'])
m = gdf.explore(column='Inequality',
                cmpa='Reds',
                legend=True,
                legend_kwds={'lable': 'Inequality level'})
m.save("map.html")

class MapView(View):

    id = "map"
    label = "Ecarts salariaux par région"
    icon = "tabler:compass"


    def render(self):
        return dmc.Stack(
            children=[
                html.H3(self.label),

                # components.dataContainer(id=ContainerIds.MAP_CONTAINER),
                html.Div(id=ContainerIds.MAP_CONTAINER),

                components.yearSelector()
            ],
        )
    

    def renderMap(self, year):
        # TODO replace by actual map
        try: 
            with open("map.html", "r") as f:
                map_html = f.read()
            return html.Iframe(
                srcDoc=map_html,
                style={
                    'width': '100%',
                    'height': '80vh',
                    'border': 'none'
                }
            )
        except FileNotFoundError:
            
            return html.Div("Cmap.html not found Please generate the map first.")