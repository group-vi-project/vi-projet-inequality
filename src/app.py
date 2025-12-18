import dash
from dash import html, dcc, Input, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from views.comparisons_view import ComparisonsView
from views.evolution_view import EvolutionView
from views.map_view import MapView

from common.callbacks import get_callbacks

from common.constants import StoreKeys, Series


app = dash.Dash(
        __name__,
        suppress_callback_exceptions=True,
        # needed for callbacks using dynamically added components
        title="Différences salariales femmes vs hommes par région",
    )

VIEWS = [
    MapView(),
    EvolutionView(),
    ComparisonsView()
]


# Main layout
def serve_layout():
    navigation_buttons = [
        dmc.Tooltip(
            dmc.NavLink(
                leftSection=DashIconify(icon=v.icon, height=72),
                href="/"+v.id,
                id=v.id,
                active="exact"
            ),
            label=v.label
        )
        for v in VIEWS
    ]

    return dmc.MantineProvider(
        children=[
            dcc.Location(id="url"),
            dmc.Grid(
                children=[
                    # navigation buttons
                    dmc.GridCol(
                        span=0,
                        style={
                            "borderRight": "1px solid #eee",
                            "height": "100vh",
                            "padding-right": "0"
                        },
                        children=navigation_buttons
                    ),

                    # main content
                    dmc.GridCol(
                        span=10,
                        style={"padding": "1rem 2rem"},
                        children=[
                            html.Div(id="page-content")
                        ],
                    ),
                ],
            ),

            # Initialize storage for the values selected by the user
            # of the common component. It is needed in order to keep the
            # state when navigating from one view (page) to the other
            dcc.Store(id=StoreKeys.SHARED_STATE_STORE, data={
                # set default values
                StoreKeys.SELECTED_SERIES: Series.REGION,
                StoreKeys.SELECTED_REGION: "Suisse",
                StoreKeys.SELECTED_POSITION: (
                    "Position professionnelle - total"
                ),
                StoreKeys.SELECTED_YEAR: 2022,
            })
        ]
    )


app.layout = serve_layout

get_callbacks(app)


# Main render
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page(path):
    # when starting the app, redirect to the first view. Redirecting
    # is needed in order to have the right NavLink activated
    if path == "/" or path is None:
        return dcc.Location(href="/"+VIEWS[0].id, id="redirect")

    for view in VIEWS:
        if path == "/" + view.id:
            # for example MapView.render(self) returns dmc.stack
            # with components.yearSelector()
            return view.render()


if __name__ == "__main__":
    app.run(debug=True)
