"""
Streamlit web interface for AI-powered company brochure generation.
"""

import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils import create_brochure

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Company Brochure Generator", page_icon="📄", layout="wide"
)

# Custom CSS
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

# Header
st.markdown(
    '<div class="main-header">📄 AI Company Brochure Generator</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Generate professional company brochures from any website using AI</div>',
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # API Key input
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter your Google Gemini API Key", type="password")
        if api_key:
            os.environ["GENAI_API_KEY"] = api_key
    else:
        st.success("✓ API Key loaded from .env")

    st.divider()

    st.header("ℹ️ About")
    st.write("""
    This tool uses Google's Gemini AI to:
    1. Fetch and parse website content
    2. Extract relevant pages (About, Products, etc.)
    3. Generate a professional brochure
    """)

    st.divider()

    st.header("💡 Tips")
    st.write("""
    - Use full URLs (e.g., https://example.com)
    - Works best with company/corporate websites
    - Generation may take 30-60 seconds
    """)

# Main content
st.header("🌐 Enter Website URL")

col1, col2 = st.columns([3, 1])

with col1:
    website_url = st.text_input(
        "Company Website",
        placeholder="https://www.example.com",
        label_visibility="collapsed",
    )

with col2:
    generate_button = st.button(
        "🚀 Generate Brochure", type="primary", use_container_width=True
    )

# Generate brochure
if generate_button:
    if not api_key:
        st.error(
            "❌ Please provide a Google Gemini API key in the sidebar or .env file"
        )
    elif not website_url:
        st.error("❌ Please enter a website URL")
    else:
        # Ensure URL has protocol
        if not website_url.startswith(("http://", "https://")):
            website_url = "https://" + website_url

        try:
            # Configure Gemini
            genai.configure(api_key=api_key)

            # System prompt
            system_prompt = """You are a professional marketing copywriter that creates detailed, 
            engaging company brochures based on website content. Your brochures are well-structured, 
            informative, and highlight the company's key strengths and offerings."""

            # Initialize model
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp", system_instruction=system_prompt
            )

            # Progress indicators
            with st.spinner(f"🔍 Analyzing {website_url}..."):
                st.info("📥 Fetching website content...")

                # Generate brochure
                brochure = create_brochure(website_url, model)

                st.success("✅ Brochure generated successfully!")

            # Display brochure
            st.divider()
            st.header("📄 Generated Brochure")

            # Tabs for different views
            tab1, tab2 = st.tabs(["📖 Formatted View", "📝 Raw Markdown"])

            with tab1:
                st.markdown(brochure)

            with tab2:
                st.code(brochure, language="markdown")

            # Download button
            st.divider()
            st.download_button(
                label="⬇️ Download Brochure (Markdown)",
                data=brochure,
                file_name="company_brochure.md",
                mime="text/markdown",
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Made with ❤️ using Streamlit and Google Gemini AI<br>
        <small>Educational project for demonstrating AI-powered content generation</small>
    </div>
""",
    unsafe_allow_html=True,
)
