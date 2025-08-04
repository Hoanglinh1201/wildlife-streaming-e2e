import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Wildlife Tracker",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<h1 style='text-align: center; color: black; margin-top: -2rem;'>
    Welcome to the Wildlife Tracking E2E Trail Map
</h1>
<p style='text-align: center; color: black; font-size:18px;'>
    An interactive app to visualize and explore animal movements, summaries, and events.
</p>
""",
    unsafe_allow_html=True,
)


st.divider()

# Feature cards in columns
_, col1, col2, _ = st.columns([2, 2, 6, 2], gap=None, vertical_alignment="center")

with col1:
    st.markdown("### [📌 Summary Page](/summary_page)")
    st.caption("Overview of all tracked animals and their key statistics.")
    st.markdown("### [📌 Trail Map Page](/trailmap_page)")
    st.caption("Follow historical movement paths of tracked wildlife.")
    st.markdown("### [📌 Event Page](/event_page)")
    st.caption("Stay updated on the latest wildlife tracking events.")

with col2:
    st.image("frontend/images/banner.png", use_container_width=True)
