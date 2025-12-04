from dash import html, dcc, Input, Output
import dash_mantine_components as dmc
import geopandas as gpd

from views.view import View

from common.constants import ComponentIds, ContainerIds
import common.components as components
import geopandas as gpd
geofile_path = "2025_GEOM_TK/03_ANAL/Gesamtfläche_gf/K4_greg20001205_gf/K4greg20001205gf_ch2007Poly.shp"
gdf = gpd.read_file(geofile_path)
m = gdf.explore('id')
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