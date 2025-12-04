# from dash import Dash, html
import pandas as pd
import json
import plotly.express as px
import geopandas as gpd
from geojson_rewind import rewind

# app = Dash(__name__)

df = pd.read_csv('data2.csv', encoding='utf-8')

with open('swiss_geojson.geojson', encoding='utf-8') as file:
   reg_ch = json.load(file)

reg_ch = rewind(reg_ch, rfc7946=False)

geo_df = gpd.GeoDataFrame.from_features(
      reg_ch['features']
).merge(df, on='REGCH_fr').set_index('REGCH_fr')

with open('Swiss_geo_df.csv', 'a', encoding='utf-8') as file:
    file.write(str(geo_df))

# for i in range(0, 7):
#    print(f'{reg_ch["features"][i]["properties"]["REGCH_fr"]} - {df["regch"][i]} - {df["data"][i]}')

fig = px.choropleth(geo_df, geojson=geo_df.geometry, color='data', 
                    locations=geo_df.index,
                    projection="mercator")

fig.update_geos(fitbounds="locations", visible=False) 
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show() 

# if __name__ == "__main__":
#    app.run(debug=True)