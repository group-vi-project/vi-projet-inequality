from dash import html, dcc, Input, Output
import dash_mantine_components as dmc

from views.view import View

from common.constants import ComponentIds, ContainerIds
import common.components as components

class MapView(View):

    id = "map"
    label = "Ecarts salariaux par région"
    icon = "tabler:compass"


    def render(self):
        return dmc.Stack(
            children=[
                html.H3(self.label),

                components.dataContainer(id=ContainerIds.MAP_CONTAINER),

                components.yearSelector()
            ],
        )
    

    def renderMap(self, year):
        # TODO replace by actual map
        return html.Div(f"Carte des écarts salariaux de l'année {year}")