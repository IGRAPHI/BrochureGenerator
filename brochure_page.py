"""
Company Brochure Generator page.

Streamlit page that generates a professional company brochure from a website
URL. Core functionality is imported from main.py to avoid duplication.
(This was previously the standalone app.py; it is now one page of a
multipage app — st.set_page_config lives in the entrypoint.)
"""

import os

import streamlit as st

from main import get_api_key, generate_brochure, markdown_to_pdf, PDF_AVAILABLE

# Initialize session state for storing brochure
if "brochure" not in st.session_state:
    st.session_state.brochure = None
if "last_url" not in st.session_state:
    st.session_state.last_url = None

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
    api_key = get_api_key()
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

    if not PDF_AVAILABLE:
        st.divider()
        st.warning("⚠️ PDF export not available")
        st.caption("Install with: `pip install reportlab markdown2`")

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

# Check if URL changed - if so, clear previous brochure
if website_url and website_url != st.session_state.last_url:
    if st.session_state.last_url is not None:  # Only clear if there was a previous URL
        st.session_state.brochure = None
    st.session_state.last_url = website_url

# Generate brochure
if generate_button:
    if not api_key:
        st.error(
            "❌ Please provide a Google Gemini API key in the sidebar or .env file"
        )
    elif not website_url:
        st.error("❌ Please enter a website URL")
    else:
        try:
            # Progress indicators
            with st.spinner(f"🔍 Analyzing {website_url}..."):
                st.info("📥 Fetching website content...")

                # Generate brochure using main.py function
                brochure = generate_brochure(website_url, api_key)

                # Store in session state
                st.session_state.brochure = brochure
                st.session_state.last_url = website_url

                st.success("✅ Brochure generated successfully!")

        except Exception as e:
            import providers
            st.error(f"❌ Error: {providers.redact(str(e))}")

# Display brochure if it exists in session state
if st.session_state.brochure:
    brochure = st.session_state.brochure

    # Display brochure
    st.divider()
    st.header("📄 Generated Brochure")

    # Display formatted markdown - simple clean rendering
    st.markdown(brochure)

    # Download options
    st.divider()
    st.subheader("📥 Download Options")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="⬇️ Download as Markdown (.md)",
            data=brochure,
            file_name="company_brochure.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col2:
        # Generate PDF only if library is available
        if PDF_AVAILABLE:
            try:
                pdf_buffer = markdown_to_pdf(brochure)
                st.download_button(
                    label="⬇️ Download as PDF (.pdf)",
                    data=pdf_buffer,
                    file_name="company_brochure.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as pdf_error:
                st.warning(f"⚠️ PDF generation failed: {pdf_error}")
                st.info(
                    "💡 Tip: You can download Markdown and convert it using online tools"
                )
        else:
            st.info("📄 PDF export not available")
            st.caption("Install with: `pip install reportlab markdown2`")

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
