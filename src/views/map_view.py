from dash import html
import dash_mantine_components as dmc
import geopandas as gpd
import pandas as pd
from views.view import View
from common.constants import ContainerIds
import common.components as components
import os

geofile_path = os.path.join(
    os.getcwd(), '..',
    '2025_GEOM_TK', '03_ANAL',
    'Gesamtfläche_gf', 'K4_greg20001205_gf',
    'K4greg20001205gf_ch2007Poly.shp'
)
data_path_file = os.path.join(
    os.getcwd(), '..', 'data',
    'inequality_by_region_position_year.csv'
)

dfinq = pd.read_csv(data_path_file)
gdf_base = gpd.read_file(geofile_path)


class MapView(View):

    id = "map"
    label = "Ecarts salariaux par région"
    icon = "tabler:compass"

    def render(self):
        return dmc.Stack(
            children=[
                html.H3(self.label),
                components.positionSelector(),
                # components.dataContainer(id=ContainerIds.MAP_CONTAINER),
                html.Div(id=ContainerIds.MAP_CONTAINER),

                components.yearSelector()
            ],
        )

    def renderMap(self, year, position):
        try:
            dfinq_filtered = dfinq.loc[
                (dfinq["Year"] == year) & (dfinq["Position"] == position)
            ]
            gdf = gdf_base.merge(dfinq_filtered[['Region', 'Inequality']],
                                 left_on='name', right_on='Region', how='left')
            gdf = gdf.drop(columns=['id', 'name'])
            m = gdf.explore(column='Inequality',
                            cmap='Reds',
                            legend_kwds={'label': 'Inequality level'})
            m.save('map.html')
            with open('map.html', 'r') as f:
                map_html = f.read()
            return html.Iframe(
                srcDoc=map_html,
                style={
                    'width': '90%',
                    'height': '70vh',
                    'border': 'none'
                }
            )
        except FileNotFoundError:
            return html.Div(
                "Cmap.html not found Please generate the map first."
            )
