from geopandas import GeoDataFrame
from shapely import Polygon

import datetime
import geopandas
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# >>>>> USER INTERFACE <<<<<
# Header
st.markdown("""# Predicting the Number of Rentals
## Choose the day and time below""")

# UI date
picked_date = st.date_input(
    "🗓️ Select day: ",
    datetime.date(2025, 7, 6))

# UI time
picked_time = st.slider('🚲 Select time:', 0, 23, 12)



# >>>>> API REQUESTS <<<<<

# GET Requests > /polygons
url = 'http://localhost:8000/polygons'
response = requests.get(url).json()

districts = list(response.keys())
index_values = districts
district_polys = pd.DataFrame(index=index_values)

# Function-converter coords to polygons
def get_polygons(coords):
    polygon = Polygon(coords)
    return polygon


# Mapping coordingates with districts
district_polys['geo_polygon'] = district_polys.index.map(response)

# Convert coordinates to polygons
district_polys['geo_polygon'] = district_polys['geo_polygon'].apply(get_polygons)



# GET Requests > /base_predict
url = 'http://127.0.0.1:8000/base_predict'
params = {'date': picked_date}
response = requests.get(url, params=params).json()

# Add number of rents from api
district_polys['n_rents'] = district_polys.index.map(response)

# Function get rents per hour column
def get_n_rents(picked_time, district_polys):
    district_polys['rents_per_hour'] = district_polys['n_rents'].apply(lambda x: x[picked_time])
    return district_polys


get_n_rents(picked_time, district_polys)


# Initiating GeoDataFrame
gdf = GeoDataFrame(district_polys, crs="EPSG:4326", geometry='geo_polygon')


# >>>>> MAP <<<<<
# Plot map with polygons
fig = px.choropleth_mapbox(gdf,
                           geojson=gdf.geometry,
                           locations=gdf.index,
                           color='rents_per_hour',
                           color_continuous_scale='RdBu',
                           range_color=(0, 100),
                           mapbox_style="open-street-map", # carto-positron
                           zoom=10,
                           opacity=0.5,
                           center = {"lat": 48.1351, "lon": 11.5820})

# fig.show()
st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")
