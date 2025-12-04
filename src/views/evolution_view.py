from dash import html, dcc, Input, Output
import dash_mantine_components as dmc

from views.view import View

from common.constants import ComponentIds, ContainerIds, Series
import common.components as components


class EvolutionView(View):

    id = "evolution"
    label = "Evolution des écarts salariaux"
    icon = "tabler:timeline"


    def render(self):
        return dmc.Stack(
            children=[
                html.H3(self.label),

                components.seriesSelector(),

                html.Div(id=ContainerIds.REGION_OR_POSITION_CONTAINER),

                components.dataContainer(id=ContainerIds.EVOLUTION_CONTAINER),
            ],
        )
    
    
    def renderEvolution(self, series, region, position):
        # TODO replace by actual graph
        title = ""
        if series == Series.POSITION:
            title = f"Evolution des écarts salariaux de la position professionnelle : {position}"
        else:
            title = f"Evolution des écarts salariaux de la région : {region}"
        return html.Div(title)
    
    