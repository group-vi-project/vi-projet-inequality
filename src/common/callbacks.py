from dash import html, dcc, Input, Output, State

from common.constants import ComponentIds, ContainerIds, StoreKeys, Series
import common.components as components

from views.comparisons_view import ComparisonsView
from views.evolution_view import EvolutionView
from views.map_view import MapView


def get_callbacks(app):

    # used to update the store, called whenever the user changed the state of a component
    # that handles a value shared among different views
    @app.callback(
        Output(StoreKeys.SHARED_STATE_STORE, "data"),
        Input(ComponentIds.SERIES_SELECTOR, "value", allow_optional=True),
        Input(ComponentIds.POSITION_SELECTOR, "value", allow_optional=True),
        Input(ComponentIds.REGION_SELECTOR, "value", allow_optional=True),
        Input(ComponentIds.YEAR_SELECTOR, "value", allow_optional=True),
        State(StoreKeys.SHARED_STATE_STORE, "data"),
        prevent_initial_call=True
    )
    def update_store(selected_series, selected_position, selected_region, selected_year, state):
        if selected_series is not None:
            state[StoreKeys.SELECTED_SERIES] = selected_series
        if selected_position is not None:
            state[StoreKeys.SELECTED_POSITION] = selected_position
        if selected_region is not None:
            state[StoreKeys.SELECTED_REGION] = selected_region
        if selected_year is not None:
            state[StoreKeys.SELECTED_YEAR] = selected_year
        return state
    

    # retrieve the storage value in order to update the the series selector
    @app.callback(
        Output(ComponentIds.SERIES_SELECTOR, "value"),
        Input("url", "pathname"), # execute this callback whenever the url changes
        State(StoreKeys.SHARED_STATE_STORE, "data")
    )
    def sync_series_selector(_path, state):
        return state[StoreKeys.SELECTED_SERIES]


    # retrieve the storage value in order to update the the professional position selector
    @app.callback(
        Output(ComponentIds.POSITION_SELECTOR, "value"),
        Input("url", "pathname"), # execute this callback whenever the url changes
        State(StoreKeys.SHARED_STATE_STORE, "data")
    )
    def sync_position_selector(_path, state):
        return state[StoreKeys.SELECTED_POSITION]


    # retrieve the storage value in order to update the the region selector
    @app.callback(
        Output(ComponentIds.REGION_SELECTOR, "value"),
        Input("url", "pathname"), # execute this callback whenever the url changes
        State(StoreKeys.SHARED_STATE_STORE, "data")
    )
    def sync_region_selector(_path, state):
        return state[StoreKeys.SELECTED_REGION]

    # retrieve the storage value in order to update the the year selector
    @app.callback(
        Output(ComponentIds.YEAR_SELECTOR, "value"),
        Input("url", "pathname"), # execute this callback whenever the url changes
        State(StoreKeys.SHARED_STATE_STORE, "data")
    )
    def sync_year_selector(_path, state):
        return state[StoreKeys.SELECTED_YEAR]


    # show the region or position selector, depending on the value of the series selector
    @app.callback(
        Output(ContainerIds.REGION_OR_POSITION_CONTAINER, "children"),
        Input(ComponentIds.SERIES_SELECTOR, "value")
    )
    def render_region_or_position(selected_series):
        if selected_series == Series.POSITION:
            return components.positionSelector()
        return components.regionSelector()


    # show the map
    # @app.callback(
    #     Output(ContainerIds.MAP_CONTAINER, "children"),
    #     Input(ComponentIds.YEAR_SELECTOR, "value"),
    # )
    # def render_map(year):
    #     return MapView().renderMap(year)
    
    # update map
    @app.callback(
        Output(ContainerIds.MAP_CONTAINER, "children"),
        Input(StoreKeys.SHARED_STATE_STORE, "data")
    )
    def update_map(shared_state):
        year = shared_state.get(StoreKeys.SELECTED_YEAR, 2022)
        return MapView().renderMap(year)
    

    # show the evolution
    @app.callback(
        Output(ContainerIds.EVOLUTION_CONTAINER, "children"),
        Input(ComponentIds.SERIES_SELECTOR, "value"),
        Input(ComponentIds.REGION_SELECTOR, "value", allow_optional=True), # either position or region
        Input(ComponentIds.POSITION_SELECTOR, "value", allow_optional=True), # either position or region
    )
    def render_evolution(series, region, position):
        return EvolutionView().renderEvolution(series, region, position)
    

    # show the comparison
    @app.callback(
        Output(ContainerIds.COMPARISON_CONTAINER, "children"),
        Input(ComponentIds.SERIES_SELECTOR, "value"),
        Input(ComponentIds.REGION_SELECTOR, "value", allow_optional=True), # either position or region
        Input(ComponentIds.POSITION_SELECTOR, "value", allow_optional=True), # either position or region
        Input(ComponentIds.YEAR_SELECTOR, "value"),
    )
    def render_comparison(series, region, position, year):
        return ComparisonsView().renderComparison(series, region, position, year)
