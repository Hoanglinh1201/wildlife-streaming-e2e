# --- map.py ---

import hashlib
from datetime import datetime

import pandas as pd
import streamlit as st
from pydeck import Deck, Layer, ViewState
from tooltip import MAP_TOOLTIPS

ICON_SIZE = 75


def color_from_id(id_str: str) -> list[int]:
    hash_val = int(hashlib.md5(id_str.encode()).hexdigest(), 16)
    return [(hash_val >> shift) & 0xFF for shift in (0, 8, 16)]


def rgb_to_hex(color: list[int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*color)


def render_wildlife_map(
    tracking_metadata: pd.DataFrame,
    coordinate_data: pd.DataFrame,
    zoom: int = 10,
    pitch: int = 0,
) -> Deck:
    """Render a map using PyDeck with wolf locations."""
    if tracking_metadata.empty:
        st.error("No data available to display on the map.")
        return None

    tracking_metadata["icon_adjust"] = tracking_metadata.apply(
        lambda row: {
            "url": row["icon"],
            "width": ICON_SIZE,
            "height": ICON_SIZE,
            "anchorY": ICON_SIZE,
        },
        axis=1,
    )

    # Last lat lon per collar_id
    latest_coords_df = (
        coordinate_data.sort_values(
            by=["animal_id", "timestamp"], ascending=[True, False]
        )
        .groupby("animal_id", as_index=False)
        .first()
    )
    # Enhance woft_metadata with last known coordinates
    merged_df = tracking_metadata.merge(
        latest_coords_df,
        how="left",
        on="animal_id",
    )

    merged_df[["lon", "lat"]] = merged_df["coordinate"].apply(
        lambda x: pd.Series(x[:2])
    )

    merged_df["trail_color"] = merged_df["animal_id"].apply(
        lambda x: rgb_to_hex(color_from_id(x))
    )
    merged_df = merged_df.drop(columns=["coordinate", "animal_id"])
    merged_df["age"] = merged_df["age"].apply(lambda x: f"{x:.1f}")

    icon_layer = Layer(
        "IconLayer",
        data=merged_df,
        get_icon="icon_adjust",
        get_size=5,
        get_position=["lon", "lat"],
        size_scale=15,
        pickable=True,
    )

    trail_df = coordinate_data.groupby("animal_id", as_index=False).agg(
        {"coordinate": list, "timestamp": list}
    )
    trail_df["color"] = coordinate_data["animal_id"].apply(lambda x: color_from_id(x))
    trail_layer = Layer(
        "TripsLayer",
        data=trail_df,
        get_path="coordinate",
        get_timestamps="timestamp",
        get_color="color",
        current_time=int(datetime.now().timestamp()),
        trail_length=500,
        opacity=0.6,
        rounded=True,
        width_scale=1,
        width_min_pixels=2,
        width_max_pixels=10,
    )

    # Set the view state of the map
    view_state = ViewState(
        latitude=merged_df["lat"].mean(),
        longitude=merged_df["lon"].mean(),
        zoom=zoom,
        pitch=pitch,
    )

    # Create the deck
    return Deck(
        layers=[icon_layer, trail_layer],
        initial_view_state=view_state,
        tooltip=MAP_TOOLTIPS,
        map_style="light",
        height=2000,
    )
