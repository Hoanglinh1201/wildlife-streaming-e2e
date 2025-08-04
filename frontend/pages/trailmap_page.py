import pandas as pd
import streamlit as st
from pydeck import Deck, Layer, ViewState
from utils.db import query_clickhouse

# --- Streamlit Page ---
st.set_page_config(
    page_title="Trail",
    page_icon="🗺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REFRESH_INTERVAL = 120  # seconds
ICON_SIZE = 75

MAP_TOOLTIPS = {
    "html": "<b>Time:</b> {event_str}<br/>"
    "<b>Lat :</b> {lat_str}<br/>"
    "<b>Lon :</b> {lon_str}<br/>"
    "<b>Dist:</b> {dist_str}<br/>"
    "<b>Speed:</b> {speed_str}",
    "style": {
        "backgroundColor": "transparent",
        "color": "#2c3e50",
        "fontSize": "12px",
        "padding": "5px",
    },
}


@st.cache_data(ttl=REFRESH_INTERVAL)
def fetch_animal_list() -> pd.DataFrame:
    """
    Fetch the latest summary data from the database.
    """
    extract_sql = "SELECT * FROM mart.f_animal_summary"
    df = query_clickhouse(extract_sql)
    return df


def fetch_trail_data(tracker_id: str) -> pd.DataFrame:
    """
    Fetch the trail data for a specific animal ID.
    """
    extract_sql = f"""
        SELECT tracker_id,event_id,event_type,lat,lon,event_at, distance_km, speed_kmh
        FROM foundation.f_movement
        WHERE tracker_id = '{tracker_id}'
        ORDER BY event_at
    """
    return query_clickhouse(extract_sql)


def get_animal_label(row: pd.Series) -> str:
    return f"{row['animal_name']} ({row['animal_type']} / {row['species']} / {row['gender']})"


def get_label_mapping(df: pd.DataFrame) -> dict[str, str]:
    return {row["tracker_id"]: get_animal_label(row) for _, row in df.iterrows()}


def create_trail_map(
    animal_icon: str,
    trail_df: pd.DataFrame,
    trail_event_to_display: int = 30,
    zoom: int = 6,
    pitch: int = 40,
) -> Deck:
    # Prepare the trail data
    fig_prep_df = trail_df.copy().tail(trail_event_to_display)
    max_timestamp = fig_prep_df["event_at"].max().timestamp()
    min_timestamp = fig_prep_df["event_at"].min().timestamp()
    latest_lat = fig_prep_df["lat"].iloc[-1]
    latest_lon = fig_prep_df["lon"].iloc[-1]
    trail_length_calculated = max_timestamp - min_timestamp

    fig_prep_df["coordinates"] = fig_prep_df.apply(
        lambda row: [row["lon"], row["lat"]],
        axis=1,
    )
    fig_prep_df["timestamp"] = fig_prep_df["event_at"].apply(
        lambda x: pd.to_datetime(x).timestamp()
        - pd.to_datetime(min_timestamp).timestamp()
    )

    fig_prep_df["event_str"] = pd.to_datetime(fig_prep_df["event_at"]).dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    fig_prep_df["lat_str"] = fig_prep_df["lat"].map(lambda x: f"{x:.5f}")
    fig_prep_df["lon_str"] = fig_prep_df["lon"].map(lambda x: f"{x:.5f}")
    fig_prep_df["dist_str"] = fig_prep_df["distance_km"].map(lambda d: f"{d:.2f} km")
    fig_prep_df["speed_str"] = fig_prep_df["speed_kmh"].map(lambda s: f"{s:.2f} km/h")

    # Make into 1 line per animal
    fig_df = (
        fig_prep_df.groupby(["tracker_id"])
        .agg({"coordinates": list, "timestamp": list})
        .reset_index()
    )

    fig_df.drop(columns=["tracker_id"], inplace=True)

    trail_layer = Layer(
        "TripsLayer",
        fig_df,
        get_path="coordinates",
        get_timestamps="timestamp",
        get_color=[253, 128, 93],
        opacity=0.8,
        width_min_pixels=5,
        rounded=True,
        current_time=max_timestamp,
        trail_length=trail_length_calculated,
        animation_speed=1,
    )

    icon_layer = Layer(
        "IconLayer",
        data=[
            {
                "coordinates": [latest_lon, latest_lat],
                "icon_adjust": {
                    "url": animal_icon,
                    "width": ICON_SIZE,
                    "height": ICON_SIZE,
                    "anchorY": ICON_SIZE,
                },
            }
        ],
        get_icon="icon_adjust",
        get_size=5,
        get_position="coordinates",
        size_scale=15,
    )

    # 4) Scatterplot layer for each movement point
    points_layer = Layer(
        "ScatterplotLayer",
        data=fig_prep_df,
        get_position=["lon", "lat"],
        get_fill_color=[253, 128, 93],
        get_radius=3,  # in meters
        pickable=True,  # enable hover
        auto_highlight=True,  # highlight on hover
        highlight_color=[255, 255, 0, 200],
    )

    # Set the view state of the map
    view_state = ViewState(
        latitude=latest_lat,
        longitude=latest_lon,
        zoom=zoom,
        pitch=pitch,
    )

    # Create the deck
    return Deck(
        layers=[icon_layer, trail_layer, points_layer],
        initial_view_state=view_state,
        tooltip=MAP_TOOLTIPS,
        map_style="light",
        height=2000,
    )


# --- Main Page Content ---
st.markdown(
    """
    <div style="padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem;">
        <h1 style="margin: 0;">🐾 Trail Deepdive 🐾</h1>
        <p style="color: #555;">Visualizes previous tracked location as trail on map</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

map_df = fetch_animal_list()
label_df = get_label_mapping(map_df)

# Sidebar Div
left_col, between_col, right_col = st.columns(
    [2, 6, 4], gap="small", vertical_alignment="top"
)
with left_col:
    st.subheader("Filters", divider=True)

    selected_id = st.selectbox(
        "Select Animal",
        options=list(label_df.keys()),
        format_func=lambda x: label_df[x],
        help="Select an animal to view its trail",
    )

    trail_event_to_display = st.slider(
        "Trail Events to Display",
        min_value=10,
        max_value=100,
        value=30,
        step=5,
        help="Adjust the number of trail events to display on the map",
    )

    selected_zoom = st.slider(
        "Map Zoom Level",
        min_value=1,
        max_value=30,
        value=15,
        step=1,
        help="Adjust the zoom level of the map",
    )

    selected_pitch = st.slider(
        "Map Pitch",
        min_value=0,
        max_value=100,
        value=60,
        step=1,
        help="Adjust the pitch angle of the map",
    )

# Map and Charts Section
with between_col:
    st.subheader("Trail map", divider=True)
    st.caption("Map showing the distribution of animals based on selected filters")
    selected_animal = map_df[map_df["tracker_id"] == selected_id]
    animal_icon = selected_animal["animal_icon"].values[0]
    trail_data = fetch_trail_data(selected_id)
    st.pydeck_chart(
        create_trail_map(
            animal_icon,
            trail_data,
            trail_event_to_display=trail_event_to_display,
            zoom=selected_zoom,
            pitch=selected_pitch,
        ),
        use_container_width=True,
        height=550,
    )

with right_col:
    st.subheader("Movement Logs", divider=True)
    st.caption("Detailed movement logs for the selected animal")
    st.dataframe(
        trail_data,
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config={
            "event_type": st.column_config.TextColumn("Event"),
            "lat": st.column_config.NumberColumn("Latitude", format="%.5f"),
            "lon": st.column_config.NumberColumn("Longitude", format="%.5f"),
            "event_at": st.column_config.DatetimeColumn("Event Time"),
            "distance_km": st.column_config.NumberColumn(
                "Distance (km)", format="%.2f"
            ),
            "speed_kmh": st.column_config.NumberColumn("Speed (km/h)", format="%.2f"),
        },
        column_order=[
            "event_at",
            "event_type",
            "lat",
            "lon",
            "distance_km",
            "speed_kmh",
        ],
    )
