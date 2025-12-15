from dash import html, dcc
import dash_mantine_components as dmc

from views.view import View

from common.constants import ContainerIds, Series
import common.components as components

import pandas as pd
import plotly.graph_objects as go

import os

data_path_file = os.path.join(
    os.getcwd(), 'data', '12-22_suisse_sect26_tout_tout.csv'
)

COMPARISON_DATA = pd.read_csv(data_path_file, sep=';')
# columns: "Année";"Grande région";"Division économique";
# "Position professionnelle";"Sexe";"Médiane";"P10";"P25";"P75";"P90"


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
        mask = COMPARISON_DATA["Année"] == year

        if series == Series.POSITION:
            mask = mask & (
                COMPARISON_DATA["Position professionnelle"] == position
            )
            title = (
                f"Comparaison des salaires {year} de la position "
                f"professionnelle : {position}"
            )
            series_name = "Grande région"
        else:
            mask = mask & (COMPARISON_DATA["Grande région"] == region)
            title = f"Comparaison des salaires {year} de la région : {region}"
            series_name = "Position professionnelle"

        # columns: "Année";"Grande région";"Division économique";
        # "Position professionnelle";"Sexe";"Médiane";"P10";"P25";"P75";"P90"
        full_df = COMPARISON_DATA[mask]

        def getValues(df, column):
            return df[column].tolist()

        color = {
            "Hommes": "darkblue",
            "Femmes": "tomato"
        }

        fig = go.Figure()
        for gender in ["Hommes", "Femmes"]:
            df = full_df[full_df["Sexe"] == gender]

            fig.add_trace(go.Box(
                x=getValues(df, series_name),
                lowerfence=getValues(df, "P10"),
                q1=getValues(df, "P25"),
                median=getValues(df, "Médiane"),
                q3=getValues(df, "P75"),
                upperfence=getValues(df, "P90"),
                name=gender,
                marker_color=color[gender],
                line_color=color[gender],
                showlegend=True,
                hoverinfo="y",
            ))
        # TODO ajotuer séparation entre Suisse et autres régions /
        # entre Toutes positions prof et les autres

        fig.update_layout(
            boxmode='group',
            title=title
        )
        fig.update_yaxes(title="Salaire en CHF")
        graph = dcc.Graph(figure=fig)

        return html.Div(children=[
            graph,
            ])
