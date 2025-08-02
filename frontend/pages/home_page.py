import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Wildlife Tracker",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hero section
st.markdown(
    """
<div style='background-image: url(https://example.com/banner.jpg);
            background-size: cover;
            padding: 3rem;
            border-radius: .75rem;'>
    <h1 style='color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.6);'>
    Welcome to the Wildlife Tracking E2E Trail Map
    </h1>
    <p style='color: white; font-size:18px;'>
    An interactive app to visualize and explore animal movements, summaries, and events.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# Feature cards in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 📌 Trail Map")
    st.write("Follow historical movement paths of tracked wildlife.")
with col2:
    st.markdown("### 📌 Summary Page")
    st.write("Overview of all tracked animals and their key statistics.")
with col3:
    st.markdown("### 📌 Events Page")
    st.write("Stay updated on the latest wildlife tracking events.")
