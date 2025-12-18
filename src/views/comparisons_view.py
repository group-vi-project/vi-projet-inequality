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
                hoverinfo="y",  # pas possible de cacher les libellés min/max, cf. notamment https://community.plotly.com/t/customizing-traces-of-boxplot/82464
            ))

        # line separating the global value "Suisse" / "Position professionnelle - Total" and the following
        fig.add_vline(
            x=0.5,  # between first serie (x=0) and second (x=1)
            line_width=1,
            line_color="lightgrey",
            line_dash="dot"
        )

        fig.update_layout(
            boxmode='group',
            title=title,
            margin=dict(l=40, r=20, t=30, b=40),  # narrow margins
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)")
        fig.update_yaxes(
            title="Salaire en CHF",
            rangemode="tozero",  # display the 0 value
            hoverformat=",.0f",  # see https://github.com/d3/d3-format/tree/v1.4.5#d3-format
            ticks="outside",
            tickcolor="rgba(0,0,0,0.6)",
            )
        graph = dcc.Graph(
            figure=fig,
            config=dict(locale="fr"),
            style={"height": "500px"}
            )

        return html.Div(children=[
            graph,
            components.sourceInfo("Source : OFS. Salaires du secteur Fabrication de produits informatiques, électroniques et optiques/horlogerie"),
        ])
