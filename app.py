"""
Entry point for the AI Presentation & Brochure Studio (Streamlit).

This is a multipage app:
- 📊 Presentation Creative Brief — a creative-director-style intake that turns a
  few smart questions into a detailed creative brief and build-ready outputs.
- 📄 Company Brochure Generator — generate a brochure from any website URL.

Run with:  streamlit run app.py
"""

import streamlit as st

# Page config (set once, here in the entrypoint, for the whole app)
st.set_page_config(
    page_title="AI Presentation & Brochure Studio",
    page_icon="🎯",
    layout="wide",
)

# Shared styling used by the individual pages
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Multipage navigation. The creative brief is the default landing page.
creative_brief_page = st.Page(
    "views/creative_brief_page.py",
    title="Presentation Creative Brief",
    icon="📊",
    default=True,
)
brochure_page = st.Page(
    "views/brochure_page.py",
    title="Company Brochure Generator",
    icon="📄",
)

navigation = st.navigation([creative_brief_page, brochure_page])
navigation.run()
