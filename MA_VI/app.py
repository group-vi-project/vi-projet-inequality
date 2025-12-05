# from dash import Dash, html
import pandas as pd
import json
import plotly.express as px
import geopandas as gpd
from geojson_rewind import rewind
import numpy as np

# app = Dash(__name__)

try:
    df = pd.read_csv('data.csv', sep=';', encoding='latin-1')
except Exception as e:
    print(f"Erreur lors du chargement du fichier: {e}")
    # Si le chargement échoue, nous arrêtons ici.
    raise

df = df[df['Sexe'] != 'Sexe - total']
all_Regions = df['Grande région'].unique()
allowed_regions = [region for region in all_Regions if region != 'Suisse']

df_for_each_region = {}

for region in allowed_regions:
    # Filtrer le DataFrame principal pour la région actuelle et créer une copie propre (.copy())
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
    print(f"✅ Moyenne calculée pour la région {region}. Taille du DataFrame: {df_mean.shape}")

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

with open('swiss_geojson.geojson', encoding='utf-8') as file:
   reg_ch = json.load(file)

reg_ch = rewind(reg_ch, rfc7946=False)

geo_df = gpd.GeoDataFrame.from_features(
      reg_ch['features']
      
).merge(df_to_print[2016], on='REGCH_fr').set_index('REGCH_fr')


with open('Swiss_geo_df.csv', 'a', encoding='utf-8') as file:
    file.write(str(geo_df))

# for i in range(0, 7):
#    print(f'{reg_ch["features"][i]["properties"]["Grande région"]} - {df["regch"][i]} - {df["data"][i]}')

fig = px.choropleth(geo_df, geojson=geo_df.geometry, color='Pay_Gap_Mean', 
                    locations=geo_df.index,
                    color_continuous_scale="Viridis",
                    range_color=(0, geo_df['Pay_Gap_Mean'].max()),
                    projection="mercator")

fig.update_geos(fitbounds="locations", visible=False) 
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show() 

# if __name__ == "__main__":
#    app.run(debug=True)