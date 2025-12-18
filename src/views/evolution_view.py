from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px

from views.view import View

from common.constants import ContainerIds, Series
import common.components as components
import pandas as pd
import os

data_path_file = os.path.join(
    os.getcwd(), 'data',
    'inequality_by_region_position_year.csv'
)
DATA = pd.read_csv(data_path_file)
# columns: Year,Region,Position,Inequality


class EvolutionView(View):

    id = "evolution"
    label = "Evolution des écarts salariaux"
    icon = "tabler:timeline"

    def render(self):
        return dmc.Stack(
            children=[
                html.H3(self.label),

                components.seriesSelector(),    # selects REGION or POSITION

                html.Div(id=ContainerIds.REGION_OR_POSITION_CONTAINER),

                components.dataContainer(id=ContainerIds.EVOLUTION_CONTAINER),
            ],
        )

    def renderEvolution(self, series, region, position):
        df = DATA.copy()
        title = ""
        if series == Series.POSITION:
            df = df[df["Position"] == position]
            title = (
                "Evolution des écarts salariaux de la "
                f"position professionnelle : {position}"
            )
            line_field = "Region"   # show a line for every region
        else:
            df = df[df["Region"] == region]
            title = f"Evolution des écarts salariaux de la région : {region}"
            line_field = "Position"
        # Plot
        fig = px.line(
            df,
            x="Year",
            y="Inequality",
            color=line_field,
            line_dash=line_field,
            symbol=line_field,
            markers=True,
            labels={
                "Inequality": "Écart salarial (%)",
                "Year": "Année",
                line_field: line_field,
            },
            title=title,
        )
        fig.update_traces(marker=dict(size=10),
                          hovertemplate="Écart salarial: %{y:.2f}%<br>"
                        )
        fig.update_yaxes(
            ticks="outside",
            tickcolor="rgba(0,0,0,0.6)",
            )
        fig.update_xaxes(
            ticks="outside",
            tickcolor="rgba(0,0,0,0.6)",
            )
        fig.update_layout(margin=dict(t=60, r=20, l=20, b=40),
                          paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)")
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=0.5,          # thin lines
            gridcolor="rgba(0,0,0,0.2)"  # light color (adjust as you like)
        )
        return html.Div(children=[
            dcc.Graph(figure=fig),
            components.sourceInfo(),
        ])
