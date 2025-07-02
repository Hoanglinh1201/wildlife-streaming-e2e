from datetime import datetime, timedelta

import pandas as pd
import requests
import streamlit as st
from map import render_wildlife_map

# --- Streamlit Setup ---
st.set_page_config(
    page_title="Streaming Wildlife E2E",
    page_icon="🏞️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🏞️ Yok Don Nationa Park - 🐾 Live Wildlife Tracking")
st.caption("This is a demo dashboard for streaming wildlife tracking data.")

# -------------------------------
# 🧠 Session State Initialization
# -------------------------------
if "tracking_metadata" not in st.session_state:
    st.session_state.tracking_metadata = None

if "coordinates" not in st.session_state:
    st.session_state.coordinates = []

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()


# --- API Request Functions ---
def request_tracking_metadata() -> requests.Response | None:
    url = "http://localhost:9000/tracking_metadata"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None


def request_coordinates() -> requests.Response | None:
    url = "http://localhost:9000/coordinates"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        st.error(f"Error fetching coordinates: {response.status_code}")
        return None


# --- UI Button to Load Wolves ---
if st.button("Initialize Map"):
    tracking_response = request_tracking_metadata()
    if tracking_response:
        st.session_state.tracking_metadata = pd.DataFrame(tracking_response.json())

# -------------------------------
# 🔁 Auto Update Coordinates
# -------------------------------
if st.session_state.tracking_metadata is not None:
    now = datetime.now()
    if now - st.session_state.last_update > timedelta(seconds=15):
        tracking_response = request_tracking_metadata()
        if tracking_response:
            st.session_state.tracking_metadata = pd.DataFrame(tracking_response.json())

        coord_response = request_coordinates()
        if coord_response:
            new_coords = coord_response.json()
            st.session_state.coordinates.extend(new_coords)
            st.session_state.last_update = now
            st.rerun()

if st.session_state.coordinates:  # -------------------------------
    # 🗺️ Render Map + Data Tables
    # -------------------------------
    coordinate_df = pd.DataFrame(st.session_state.coordinates)
    tracking_df = st.session_state.tracking_metadata

    deck = render_wildlife_map(tracking_df, coordinate_df, zoom=10, pitch=0)
    st.pydeck_chart(deck, use_container_width=True, height=600)

    with st.expander("Show Raw Data", expanded=False, icon="📊"):
        st.subheader("Tracking Metadata")
        st.dataframe(tracking_df, use_container_width=True)

        st.subheader("Coordinates")
        st.dataframe(coordinate_df, use_container_width=True)
