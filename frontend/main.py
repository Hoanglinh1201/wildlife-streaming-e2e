import streamlit as st

# --- Streamlit Setup ---
st.set_page_config(
    page_title="Wildlife Tracking E2E Trail Map",
    page_icon="🏞️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Navigation setup

pg = st.navigation(
    pages=[
        st.Page(page="pages/home_page.py", title="𖠿 Home"),
        st.Page(page="pages/summary_page.py", title="➤ Summary"),
        st.Page(page="pages/trailmap_page.py", title="➤ Trail"),
        st.Page(page="pages/event_page.py", title="➤ Logs"),
    ],
    position="top",
)
pg.run()
