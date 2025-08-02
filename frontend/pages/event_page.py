"""
Fetching last X events from database
"""

import pandas as pd
import streamlit as st
from utils.db import query_clickhouse

# --- Streamlit Page ---
st.set_page_config(
    page_title="Logs",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REFRESH_INTERVAL = 120  # seconds

# --- State --
if "event_types" not in st.session_state:
    st.session_state.event_types = ["spawn", "move", "remove"]

if "tracker_id" not in st.session_state:
    st.session_state.tracker_id = None

if "limit" not in st.session_state:
    st.session_state.limit = 50

# --- Helper function ---

EVENT_DISPLAY_CONFIG = {
    "event_type": st.column_config.TextColumn(
        "Type", help="Type/category of the event"
    ),
    "event_at": st.column_config.DatetimeColumn(
        "Timestamp", format="YYYY-MM-DD HH:mm:ss", help="When the event occurred"
    ),
    "tracker_id": st.column_config.TextColumn(
        "🐾 Tracker ID", help="Identifier for the tracking device"
    ),
    "new_location": st.column_config.ListColumn(
        "📍To",
        help="New location coordinates (latitude, longitude)",
    ),
    "previous_location": st.column_config.ListColumn(
        "📍From",
        help="Previous location coordinates (latitude, longitude)",
    ),
    "distance_km": st.column_config.NumberColumn(
        "Distance (km)",
        help="Distance traveled during the event",
        format="%.2f",
    ),
    "speed_kmh": st.column_config.NumberColumn(
        "Speed (km/h)",
        help="Speed during the event",
        format="%.2f",
    ),
}

COLUMN_ORDER = [
    "event_at",
    "tracker_id",
    "event_type",
    "previous_location",
    "new_location",
    "distance_km",
    "speed_kmh",
]

EXTRACT_SQL = """
    SELECT
        event_type,
        event_at,
        tracker_id,
        tuple(lat,lon) AS new_location,
        tuple(prev_lat, prev_lon) AS previous_location,
        distance_km,
        speed_kmh
    FROM foundation.f_movement
    WHERE 1=1
    {tracker_id_filter}
    {event_type_filter}
    ORDER BY event_at DESC
    LIMIT {limit}

"""


@st.cache_data(ttl=120)
def fetch_events(
    limit: int = 50, tracker_id: str | None = None, event_types: list[str] | None = None
) -> pd.DataFrame:
    """
    Display the events DataFrame in Streamlit.

    :param events_df: DataFrame containing event data.
    """
    if event_types is None:
        event_types = ["spawn", "move", "remove"]

    event_type_filter = ",".join(f"'{et}'" for et in event_types)
    tracker_id_filter = f"AND tracker_id = '{tracker_id}'" if tracker_id else ""
    event_type_filter = (
        f"AND event_type IN ({event_type_filter})" if event_types else ""
    )

    event_df = query_clickhouse(
        EXTRACT_SQL,
        {
            "limit": limit,
            "tracker_id_filter": tracker_id_filter,
            "event_type_filter": event_type_filter,
        },
    )
    return event_df


# --- Main Page Content ---
st.markdown(
    """
    <div style="padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem;">
        <h1 style="margin: 0;">🐾 Tracking Logs 🐾</h1>
        <p style="color: #555;">Fetch and explore the most recent tracking events from the database.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# Filters
with st.container():
    st.subheader("Event Filters")
    st.markdown("Use the options below to filter and customize the event display.")

    cols = st.columns(3)
    limit = cols[0].number_input(
        "Number of events to display",
        min_value=1,
        max_value=1000,
        value=50,
        step=1,
        help="Specify how many recent events to display",
    )

    event_types = cols[1].multiselect(
        "Event Type",
        options=["spawn", "move", "remove"],
        default=["spawn", "move", "remove"],
        help="Filter events by type",
    )

    tracker_id = cols[2].text_input(
        "Tracker ID",
        value=None,
        placeholder="Enter Tracker ID to filter",
        help="Filter events by specific tracker ID",
    )

# Update session state
st.session_state.limit = limit
st.session_state.event_types = event_types
st.session_state.tracker_id = tracker_id

# Display the DataFrame with custom configuration
event_df = fetch_events(
    limit=st.session_state.limit,
    tracker_id=st.session_state.tracker_id,
    event_types=st.session_state.event_types,
)
height = min(500, 50 * len(event_df))  # Dynamic height based on number of rows
st.caption(f"Displaying the last {len(event_df)} events for the selected filters.")
table_button_cols = st.columns([1, 10])
reload_button = table_button_cols[0].button(
    "Reload Events",
    type="primary",
    use_container_width=True,
    help="Fetch the latest events based on the selected filters",
)
st.dataframe(
    event_df,
    column_config=EVENT_DISPLAY_CONFIG,
    column_order=COLUMN_ORDER,
    use_container_width=True,
    hide_index=False,
    height=height,
)

if reload_button:
    st.rerun()
