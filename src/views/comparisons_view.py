from dash import html, dcc, Input, Output
import dash_mantine_components as dmc

from views.view import View

from common.constants import ComponentIds, ContainerIds, Series
import common.components as components


class ComparisonsView(View):

    id = "comparisons"
    label = "Comparaison des salaires"
    icon = "tabler:scale"


    def render(self):
        return dmc.Stack(
            children=[
                html.H3(self.label),

                components.seriesSelector(),

                html.Div(id=ContainerIds.REGION_OR_POSITION_CONTAINER),
                
                components.dataContainer(id=ContainerIds.COMPARISON_CONTAINER),

                components.yearSelector(),
            ],
        )
    
    
    def renderComparison(self, series, region, position, year):
        # TODO replace by actual graph
        title = ""
        if series == Series.POSITION:
            title = f"Comparaison des salaires {year} de la position professionnelle : {position}"
        else:
            title = f"Comparaison des salaires {year} de la région : {region}"
        return html.Div(title)
    