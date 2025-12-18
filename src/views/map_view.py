from dash import html
import dash_mantine_components as dmc
import geopandas as gpd
import pandas as pd
from views.view import View
from common.constants import ContainerIds
import common.components as components
import os
import folium
import branca
import branca.colormap as cm

gpd.explore._MAP_KWARGS += ["dragging", "scrollWheelZoom"]

geofile_path = os.path.join(
    os.getcwd(),
    '2025_GEOM_TK', '03_ANAL',
    'Gesamtfläche_gf', 'K4_greg20001205_gf',
    'K4greg20001205gf_ch2007Poly.shp'
)
data_path_file = os.path.join(
    os.getcwd(), 'data',
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
    

    def color(self, value, cmap):
        if value is None:
            return "#dadada"  # grey
        return cmap(value)


    def renderMap(self, year, position):
        min_value = -25.0 # dfinq["Inequality"].min()
        max_value = 50.0 # dfinq["Inequality"].max()

        dfinq_filtered = dfinq.loc[
            (dfinq["Year"] == year) & (dfinq["Position"] == position)
        ]
        gdf = gdf_base.merge(dfinq_filtered[['Region', 'Inequality']],
                                left_on='name', right_on='Region', how='left')
        gdf = gdf.drop(columns=['id', 'name'])

        white_tile = branca.utilities.image_to_url([[1, 1], [1, 1]])
        zoom_value = 8
        m = folium.Map(
            tiles=white_tile,
            attr="Ecarts salariaux",
            zoom_control=False,
            scrollWheelZoom=False,
            dragging=False,
            location=(46.8, 8.2),
            zoom_start=zoom_value,
            min_zoom=zoom_value,
            max_zoom=zoom_value,  # avoid zooming with double click. Only works when tiles != None (bizarre...)
        )

        cmap = cm.LinearColormap(
            ["blueviolet", "white", "yellow", "orange", "red", "darkred"],
            index=[min_value, 0, max_value/4.0, max_value/2.0, 3*max_value/4.0, max_value],
            vmin=min_value,
            vmax=max_value,
            caption="Ecart (%)",
            tick_labels=[min_value, 0, max_value/2.0, max_value],)

        folium.GeoJson(
            gdf,
            style_function=lambda feature: {
                "fillColor": self.color(feature["properties"]["Inequality"], cmap),
                "color": "black",
                "weight": 0.5,
                "fillOpacity": 1,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["Region", "Inequality"],
                aliases=["Région", "Ecart (%)"],
            ),
            name="inequality",
        ).add_to(m)

        # add legend:
        cmap.add_to(m)

        return html.Iframe(
            srcDoc=m.get_root().render(),
            style={
                    'width': '100%',
                    'height': '70vh',
                    'border': 'none'
                },
        )
