from streamlit_folium import st_folium

import datetime
import folium
import numpy as np
import requests
import streamlit as st



# >>>>> USER INTERFACE <<<<<

# Header
st.markdown("""# Number of bikes rented
## Choose the day and time below""")

# UI date
picked_date = st.date_input(
    "🗓️ Select day: ",
    datetime.date(2019, 7, 6))

# UI time
picked_time = st.slider('🚲 Select time:', 0, 24, 12)



# >>>>> API REQUEST <<<<<

# Datetime combined
# rented_dt = datetime.combine(picked_date, picked_time)

# GET request
# url = 'some_api_url'
# params =    {
#                 # 'rented_dt': rented_dt
#             }

# response = requests.get(url, params=params).json()




# >>>>> MAP <<<<<
map = folium.Map(location=[48.14, 11.58], zoom_start=11.5)

cluster_centers = np.array([[48.12512424, 11.57744165],
                            [48.16817174, 11.54119953],
                            [48.17803669, 11.62262054],
                            [48.12167802, 11.45414658],
                            [48.17990781, 11.57788319],
                            [48.12273717, 11.7195075 ],
                            [48.25386796, 11.64324707],
                            [48.14587391, 11.51193132],
                            [48.14910962, 11.56111138],
                            [48.13088106, 11.61293088],
                            [47.90527218, 11.30435671],
                            [48.06649158, 11.62329064],
                            [48.09626698, 11.54173558],
                            [48.12785765, 11.54511078],
                            [48.15229305, 11.58422161]])

clusters = folium.map.FeatureGroup()


for lat, lon in zip(cluster_centers[:,0], cluster_centers[:,1]):
    clusters.add_child(
        folium.features.CircleMarker(
            [lat, lon],
            radius=7, # define how big you want the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

map.add_child(clusters)
st_data = st_folium(map, width=725)
