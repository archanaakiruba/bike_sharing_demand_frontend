from geopandas import GeoDataFrame, points_from_xy
from plotly.graph_objects import Scattermapbox
from shapely import Polygon
from shapely.geometry import Point
from datetime import datetime


import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# Get Default DateTime
def get_default_picker():
    # datetime object containing current date and time
    now = datetime.datetime.now()

    # dd/mm/YY H:M:S
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    next_day = (now + datetime.timedelta(days=1)).strftime("%d")
    current_hour = now.strftime("%H")


    default_picker = {"year": current_year, "month": current_month, "day": next_day, "hour": current_hour}
    return default_picker


default_picker = get_default_picker()
default_year = int(default_picker['year'])
default_month = int(default_picker['month'])
default_day = int(default_picker['day'])

default_time = int(default_picker['hour'])



# >>>>> USER INTERFACE <<<<<
# Header
st.markdown("""### Bike Sharing Demand 😍
##### Predicting the Number of Rentals:
""")


# UI date
picked_date = st.date_input(
    "Pick Date 🗓️ : ",
    datetime.date(default_year, default_month, default_day))
if picked_date >

# UI time
picked_time = st.slider('Pick Time ⌛️ :', 0, 23, default_time, format='%i:00')



# >>>>> API REQUESTS <<<<<

# GET Requests > /polygons
url_poly = 'https://bikesharing-fpjb6aulhq-ew.a.run.app/polygons'
response_poly = requests.get(url_poly).json()


districts = list(response_poly.keys())
district_polys = pd.DataFrame(index=districts)

# Function-converter coords to polygons
def get_polygons(coords):
    polygon = Polygon(coords)
    return polygon


# Mapping coordingates with districts
district_polys['geo_polygon'] = district_polys.index.map(response_poly)

# Convert coordinates to polygons
district_polys['geo_polygon'] = district_polys['geo_polygon'].apply(get_polygons)


# GET Requests > /base_predict
url = 'https://bikesharing-fpjb6aulhq-ew.a.run.app/base_predict'
params = {'date': picked_date}
response = requests.get(url, params=params).json()


# Add number of rents from api (24 predictions / date / district)
district_polys['n_rents'] = district_polys.index.map(response)


# Function get rents per hour column for picked_time
def get_n_rents(picked_time, district_polys):
    district_polys['rents_per_hour'] = district_polys['n_rents'].apply(lambda x: x[picked_time])
    return district_polys

# Applying get rents for picked time
get_n_rents(picked_time, district_polys)


# Initiating GeoDataFrame
gdf = GeoDataFrame(district_polys, crs="EPSG:4326", geometry='geo_polygon')

max_rental_per_day = district_polys['n_rents'].apply(lambda x: max(x)).max()


# >>>>> MAP <<<<<
# Plot map with polygons
fig = px.choropleth_mapbox(gdf,
                           geojson=gdf.geometry,
                           locations=gdf.index,
                           color='rents_per_hour',
                           color_continuous_scale='speed',
                           range_color=(0, max_rental_per_day),
                           mapbox_style="carto-positron",
                           zoom=10,
                           opacity=0.6,
                           center = {"lat": 48.1451, "lon": 11.5820},
                           height=450,
                           labels={'rents_per_hour': '  🚲', 'index': '🏠'}
                           )

# fig.show()
st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")
