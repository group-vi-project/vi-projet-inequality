from dash import html, dcc, Input, Output
import dash_mantine_components as dmc
import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gpd
import json
from geojson_rewind import rewind
import os

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
        data_path_file = os.path.join(os.getcwd(), 'data', '12-22_suisse_info_tout_tout.csv')
        try:
            df = pd.read_csv(data_path_file, sep=';', encoding='latin-1')
        except Exception as e:
            print(f"Erreur lors du chargement du fichier: {e}")
            # Si le chargement échoue, nous arrêtons ici.
            raise

        df = df[df['Sexe'] != 'Sexe - total']
        all_Regions = df['Grande région'].unique()
        allowed_regions = [region for region in all_Regions if region != 'Suisse']

        df_for_each_region = {}

        for region in allowed_regions:
            # Filtrer le DataFrame principal pour la région actuelle et créer une copie propre
            df_for_each_region[region] = df[df['Grande région'] == region].copy()

        df_pay_gap_by_region = {}

        cols_to_keep = [ 'Année', 'Grande région', 'Division économique',  'Position professionnelle']

        for region, df_region in df_for_each_region.items():
            df_cleaned = df_region.replace(['..', ':', ';;', ''], np.nan)
            df_cleaned['Médiane'] = pd.to_numeric(df_cleaned['Médiane'], errors='coerce')
            df_pivot = df_cleaned.pivot_table(
                index=cols_to_keep,
                columns='Sexe',
                values='Médiane',
                aggfunc='first'
            ).reset_index()
            df_pivot.rename(columns={'Hommes': 'Mediane_Homme', 'Femmes': 'Mediane_Femme'}, inplace=True)
            df_pivot['Pay_Gap'] = df_pivot['Mediane_Homme'] - df_pivot['Mediane_Femme']
            final_cols = cols_to_keep + ['Mediane_Homme', 'Mediane_Femme', 'Pay_Gap']
            df_final = df_pivot[final_cols].copy()
            df_pay_gap_by_region[region] = df_final

        dfs_pay_gap_mean_by_region_year = []

        print("Calcul de la moyenne de l'écart salarial (Médiane H-F) par Année et Région...")
        for region, df_region in df_pay_gap_by_region.items():
            df_mean = df_region.groupby(['Année', 'Grande région'])['Pay_Gap'].mean().round(2).reset_index()
            df_mean.rename(columns={'Pay_Gap': 'Pay_Gap_Mean'}, inplace=True)
            dfs_pay_gap_mean_by_region_year.append(df_mean)

        df_pay_gap = pd.concat(dfs_pay_gap_mean_by_region_year, ignore_index=True)

        df_by_year = {}

        annees_uniques = df_pay_gap['Année'].unique()

        for annee in annees_uniques:
            df_annee = df_pay_gap[df_pay_gap['Année'] == annee].copy()
            df_by_year[annee] = df_annee

        df_to_print = {}
        for annee, df_annee in df_by_year.items():
            df_annee.rename(columns={'Grande région': 'REGCH_fr'}, inplace=True) 
            region_pay_gap = df_annee[['REGCH_fr', 'Pay_Gap_Mean']].copy()
            df_to_print[annee] = region_pay_gap.set_index('REGCH_fr')['Pay_Gap_Mean']

        swiss_geo_path_file = os.path.join(os.getcwd(), 'data', 'swiss_geojson.geojson')
        with open(swiss_geo_path_file, encoding='utf-8') as file:
            reg_ch = json.load(file)

        reg_ch = rewind(reg_ch, rfc7946=False)

        geo_df = gpd.GeoDataFrame.from_features(
            reg_ch['features']
            
        ).merge(df_to_print[2016], on='REGCH_fr').set_index('REGCH_fr')

        fig = px.choropleth(geo_df, geojson=geo_df.geometry, color='Pay_Gap_Mean', 
                            locations=geo_df.index,
                            color_continuous_scale="Viridis",
                            range_color=(0, geo_df['Pay_Gap_Mean'].max()),
                            projection="mercator")

        fig.update_geos(fitbounds="locations", visible=False) 
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        # fig.show() 
        # TODO replace by actual map

        # print(os.getcwd())
        # swiss_geo_path_file = os.path.join(os.getcwd(), 'data', 'swiss_geojson.geojson')
        # with open(swiss_geo_path_file, encoding='utf-8') as file:
        #     reg_ch = json.load(file)

        # print(reg_ch)
        return html.Div(f"Carte des écarts salariaux de l'année {year}")