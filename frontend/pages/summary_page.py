"""
Fetching last X events from database
"""

import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.graph_objects import Figure
from pydeck import Deck, Layer, ViewState
from utils.db import query_clickhouse

# --- Streamlit Page ---
st.set_page_config(
    page_title="Summary",
    page_icon="🗺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REFRESH_INTERVAL = 120  # seconds
ICON_SIZE = 75


@st.cache_data(ttl=REFRESH_INTERVAL)
def fetch_summary() -> pd.DataFrame:
    """
    Fetch the latest summary data from the database.
    """
    extract_sql = "SELECT * FROM mart.f_animal_summary WHERE tracker_status = 'active'"
    df = query_clickhouse(extract_sql)
    return df


# -- HELPER FUNCTIONS ---
MAP_TOOLTIPS = {
    "html": """
        <div style='padding:12px; width:320px; background:#fefefe; border-radius:10px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.2); font-family:Arial, sans-serif;
                    font-size:14px; line-height:1.5; color:#2c3e50;'>
            <div style='font-weight:bold; font-size:22px; text-align:center; margin-bottom:8px;'>
                🐾 {animal_name} ({gender})
            </div>
            <div><strong>Species:</strong> {species}</div>
            <div><strong>Type:</strong> {animal_type}</div>
            <div><strong>Age:</strong> {age} yrs</div>
            <div><strong>Born:</strong> {born_at}</div>
            <div><strong>Size:</strong> {length_cm} cm, {weight_kg} kg</div>
            <hr style="margin:10px 0;">
            <div style="font-size:13px;">
                <strong>Type:</strong> {tracker_type}<br>
                <strong>Battery:</strong> {battery_level}%<br>
                <strong>Status:</strong> {tracker_status}<br>
                <strong>Latitude:</strong> {lat}<br>
                <strong>Longitude:</strong> {lon}<br>
            </div>
        </div>
    """,
    "style": {"backgroundColor": "transparent", "color": "#2c3e50"},
}


def create_treemap_chart(df: pd.DataFrame) -> Figure:
    """
    Create a sunburst chart to visualize animal types
    """
    treemap_df = df.copy()
    treemap_df["count"] = 1

    # Create the sunburst chart
    fig = px.treemap(
        treemap_df,
        path=[px.Constant("all"), "animal_type", "species"],
        values="count",
        color_discrete_sequence=["#FFB3A7", "#A8E6A1", "#A1B8F1"],
    )

    # Beautify the traces
    fig.update_traces(
        textinfo="label+percent entry",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percentEntry:.0%}<extra></extra>",
        marker=dict(line=dict(color="white", width=1)),
    )

    # Update layout aesthetics
    fig.update_layout(
        font=dict(size=12, color="#333"),
        paper_bgcolor="white",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=0, l=0, r=0, b=0),
        height=200,
    )
    return fig


def create_summary_pydeck_map(df: pd.DataFrame, zoom: int = 10, pitch: int = 0) -> Deck:
    deck_df = df.copy()

    deck_df["born_at"] = pd.to_datetime(deck_df["born_at"]).dt.strftime("%Y-%m-%d")

    deck_df["icon_adjust"] = deck_df.apply(
        lambda row: {
            "url": row["animal_icon"],
            "width": ICON_SIZE,
            "height": ICON_SIZE,
            "anchorY": ICON_SIZE,
        },
        axis=1,
    )

    icon_layer = Layer(
        "IconLayer",
        data=deck_df,
        get_icon="icon_adjust",
        get_size=5,
        get_position=["lon", "lat"],
        size_scale=15,
        pickable=True,
    )

    # Set the view state of the map
    view_state = ViewState(
        latitude=deck_df["lat"].mean(),
        longitude=deck_df["lon"].mean(),
        zoom=zoom,
        pitch=pitch,
    )

    # Create the deck
    return Deck(
        layers=[icon_layer],
        initial_view_state=view_state,
        tooltip=MAP_TOOLTIPS,
        map_style="light",
        height=2000,
    )


# --- Main Page Content ---
map_df = fetch_summary()
animal_types = map_df["animal_type"].unique().tolist()
animal_genders = map_df["gender"].unique().tolist()
animal_species = map_df["species"].unique().tolist()

# Sidebar Div
left_col, right_col = st.columns([2, 8], gap="large")
with left_col:
    st.subheader("Filters", divider=True)
    left_filters_col, right_filters_col = st.columns(2)

    selected_type: list[str] = st.multiselect(
        "Animal Type",
        options=animal_types,
        default=[],
        help="Show all animal types",
        placeholder="Show all types",
    )

    selected_gender: list[str] = st.multiselect(
        "Animal Gender",
        options=animal_genders,
        default=[],
        help="Show all genders",
    )

    selected_species: list[str] = st.multiselect(
        "Animal Species",
        options=animal_species,
        default=[],
        help="Filter by animal species",
        placeholder="Show all species",
    )

    with right_filters_col:
        selected_zoom = st.slider(
            "Map Zoom Level",
            min_value=1,
            max_value=20,
            value=8,
            step=1,
            help="Adjust the zoom level of the map",
        )

    with left_filters_col:
        selected_pitch = st.slider(
            "Map Pitch",
            min_value=0,
            max_value=60,
            value=40,
            step=1,
            help="Adjust the pitch angle of the map",
        )

    selected_species = (
        selected_species or animal_species
    )  # Default to all if none selected
    selected_gender = (
        selected_gender or animal_genders
    )  # Default to all if none selected
    selected_type = selected_type or animal_types  # Default to all if none selected

    filtered_df = map_df[
        (map_df["animal_type"].isin(selected_type))
        & (map_df["gender"].isin(selected_gender))
        & (map_df["species"].isin(selected_species))
    ]

    st.subheader("Summary", divider=True)
    st.caption("Total active trackers and their distribution across animal types")

    left_metric_col, right_metric_col = st.columns(2)
    with left_metric_col:
        st.metric(
            "Total Trackers",
            value=len(map_df["tracker_id"]),
            help="Total number of active trackers",
        )
        st.metric(
            "GPS",
            value=map_df[map_df["tracker_type"] == "gps"].shape[0],
            help="Total number of active GPS trackers",
        )

    with right_metric_col:
        st.metric(
            "Rfid",
            value=map_df[map_df["tracker_type"] == "rfid"].shape[0],
            help="Total number of active RFID trackers",
        )

        st.metric(
            "Collars",
            value=map_df[map_df["tracker_type"] == "collar"].shape[0],
            help="Total number of active Collar trackers",
        )

# Map and Charts Section
with right_col:
    if filtered_df.empty:
        st.warning("No animals found with the selected filters.")
    else:
        st.subheader("Map")
        st.caption("Map showing the distribution of animals based on selected filters")

        st.pydeck_chart(
            create_summary_pydeck_map(
                filtered_df,
                zoom=selected_zoom,
                pitch=selected_pitch,
            ),
            use_container_width=True,
            height=350,
        )

        st.write("##### Distribution")
        st.plotly_chart(
            create_treemap_chart(filtered_df),
            use_container_width=True,
        )
