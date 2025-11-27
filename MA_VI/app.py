from dash import Dash, html
import pandas as pd
import json
import plotly.express as px

app = Dash(__name__)

with open('swiss_geojson.json') as file:
   reg_ch = json.load(file)

df = pd.read_csv('data2.csv') 

fig = px.choropleth(df, geojson=reg_ch, locations='regch',
                    color='data',
                    featureidkey='properties.region',
                    projection="mercator")

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


fig.show() 
if __name__ == "__main__":
   app.run(debug=True)