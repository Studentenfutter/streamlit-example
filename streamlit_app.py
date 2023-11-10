import streamlit as st
import pandas as pd
import folium
import time
from streamlit_folium import st_folium

# Initialize a Streamlit app
st.set_page_config(
    page_title="Real-Time Flight Dashboard",
    page_icon="✈️",
)

# Set up initial map state
CENTER_START = [50.9375, 6.9603]
ZOOM_START = 5


def initialize_session_state():
    if "center" not in st.session_state:
        st.session_state["center"] = CENTER_START
    if "zoom" not in st.session_state:
        st.session_state["zoom"] = ZOOM_START
    if "markers" not in st.session_state:
        st.session_state["markers"] = []
    if "map_data" not in st.session_state:
        st.session_state["map_data"] = {}
    if "all_drawings" not in st.session_state["map_data"]:
        st.session_state["map_data"]["all_drawings"] = None
    if "upload_file_button" not in st.session_state:
        st.session_state["upload_file_button"] = False
    if 'key' not in st.session_state:
        st.session_state["key"] = "airplane-livemap"
    if 'lat' not in st.session_state:
        st.session_state.lat = 50.9375  # Initial latitude
        st.session_state.lon = 6.9603   # Initial longitude

def reset_session_state():
    # Delete all the items in Session state besides center and zoom
    for key in st.session_state.keys():
        if key in ["center", "zoom", "markers"]:
            continue
        del st.session_state[key]
    initialize_session_state()

def update_lat_lon():
    # Update lat and lon
    st.session_state.lat += 0.01  # Increment latitude
    st.session_state.lon += 0.01  # Increment longitude
    # Update marker
    st.session_state["markers"] = [folium.Marker(location=[st.session_state.lat, st.session_state.lon], popup="Test", icon=folium.Icon(icon='user', prefix='fa', color="lightgreen"))]
    []

initialize_session_state()

st.title("Live Airplane Tracker")

# create columns
col1, col2, col3 = st.columns(3)

# button for new marker
if col1.button("Add Plane"):
    update_lat_lon()

if col2.button("Reset Map", help="ℹ️ Click me to **clear the map and reset**"):
    reset_session_state()
    m = folium.Map(location=st.session_state["center"],
               center=st.session_state["center"]
              )


interval = st.slider("Update Interval (seconds)", min_value=1, max_value=60, value=5, key="one")

# Create a unique key for the map and markers
m = folium.Map(location=st.session_state["center"],
               center=st.session_state["center"],
               tiles="cartodb positron"
              )

fg = folium.FeatureGroup(name="Markers")

for marker in st.session_state["markers"]:
    fg.add_child(marker)

map_data = st_folium(
            m,
            width=800,  # Adjust the width as needed
            height=600,  # Adjust the height as needed
            feature_group_to_add=fg,
        )

st.write("## map")
st.write(interval)
st.write(map_data)
st.write("## session_state")
st.write(st.session_state)



