"""
Presentation Creative Brief page.

A creative-director-style intake that turns a few smart questions into a
detailed creative brief and a set of build-ready artifacts (slide outline,
speaker notes, design direction, content plan, AI visual prompts).

Core logic lives in creative_brief.py; this file is only the Streamlit UI.
"""

import os

import streamlit as st

from main import get_api_key, markdown_to_pdf, PDF_AVAILABLE
import creative_brief as cb

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "brief" not in st.session_state:
    st.session_state.brief = None
if "brief_intake" not in st.session_state:
    st.session_state.brief_intake = None
if "brief_exports" not in st.session_state:
    st.session_state.brief_exports = {}  # label -> generated markdown

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="main-header">📊 Presentation Creative Brief</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">A creative director for your deck — understand the '
    "presentation before you design a single slide</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar: API key + the six needs reference
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = get_api_key()
    if not api_key:
        api_key = st.text_input("Enter your Google Gemini API Key", type="password")
        if api_key:
            os.environ["GENAI_API_KEY"] = api_key
    else:
        st.success("✓ API Key loaded from .env")

    st.divider()
    st.header("🎯 The 6 presentation needs")
    for name, meta in cb.PRESENTATION_NEEDS.items():
        st.markdown(f"**{name}**  \n{meta['summary']}")

    if not PDF_AVAILABLE:
        st.divider()
        st.warning("⚠️ PDF export not available")
        st.caption("Install with: `pip install reportlab markdown2`")

# ---------------------------------------------------------------------------
# Intake form
# ---------------------------------------------------------------------------
st.header("📝 Intake")
st.caption(
    "Answer what you can — the strategist will infer sensible defaults and note "
    "its assumptions for anything you leave blank."
)

with st.form("intake_form"):
    topic = st.text_input(
        "What is the presentation about?",
        placeholder="e.g., Our Q3 product strategy and 2026 roadmap",
    )
    purpose = st.text_area(
        "What is it for — what must it accomplish?",
        placeholder="e.g., Get the leadership team to approve budget for two new hires",
        height=80,
    )

    col1, col2 = st.columns(2)
    with col1:
        audience = st.text_input(
            "Who will see it?",
            placeholder="e.g., Executive leadership team",
        )
        delivery_mode = st.selectbox(
            "Will it be presented live or sent as a document?",
            cb.DELIVERY_MODES,
        )
        knowledge_level = st.selectbox(
            "How much does the audience already know?",
            cb.KNOWLEDGE_LEVELS,
        )
        occasion = st.selectbox(
            "What is the occasion / setting?",
            cb.OCCASIONS,
        )
    with col2:
        desired_outcome = st.text_input(
            "What decision or action should happen afterward?",
            placeholder="e.g., Sign off on the proposed plan",
        )
        content_readiness = st.selectbox(
            "Do you already have content, or need help developing it?",
            cb.CONTENT_READINESS,
        )
        slide_count = st.text_input(
            "How many slides do you need? (optional)",
            placeholder="e.g., 10-12",
        )

    content_nature = st.multiselect(
        "What is the nature of the content?",
        cb.CONTENT_NATURES,
        help="Select all that apply.",
    )
    visual_mood = st.multiselect(
        "How should the deck feel?",
        cb.VISUAL_MOODS,
        help="Select all that apply.",
    )
    brand = st.text_area(
        "Any brand guidelines? (colors, logos, fonts, existing templates)",
        placeholder="e.g., Primary #0B5FFF, secondary #111827, Inter font, logo top-left",
        height=68,
    )
    notes = st.text_area(
        "Anything else the strategist should consider?",
        height=68,
    )

    submitted = st.form_submit_button(
        "🎬 Generate Creative Brief", type="primary", use_container_width=True
    )

# ---------------------------------------------------------------------------
# Handle submission
# ---------------------------------------------------------------------------
if submitted:
    if not api_key:
        st.error("❌ Please provide a Google Gemini API key in the sidebar or .env file")
    elif not (topic or purpose):
        st.error("❌ Please describe at least the topic or the purpose of the presentation.")
    else:
        intake = {
            "topic": topic,
            "purpose": purpose,
            "audience": audience,
            "delivery_mode": delivery_mode,
            "desired_outcome": desired_outcome,
            "knowledge_level": knowledge_level,
            "content_nature": content_nature,
            "visual_mood": visual_mood,
            "content_readiness": content_readiness,
            "brand": brand,
            "slide_count": slide_count,
            "occasion": occasion,
            "notes": notes,
        }
        try:
            with st.spinner("🧠 Thinking like a creative director..."):
                brief = cb.generate_creative_brief(intake, api_key)
            st.session_state.brief = brief
            st.session_state.brief_intake = intake
            st.session_state.brief_exports = {}  # reset stale exports
            st.success("✅ Creative brief generated!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)

# ---------------------------------------------------------------------------
# Display brief + exports
# ---------------------------------------------------------------------------
if st.session_state.brief:
    brief = st.session_state.brief
    intake = st.session_state.brief_intake

    st.divider()
    st.header("📄 Creative Brief")
    st.markdown(brief)

    st.divider()
    st.subheader("📥 Download the brief")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️ Markdown (.md)",
            data=brief,
            file_name="creative_brief.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col2:
        if PDF_AVAILABLE:
            try:
                st.download_button(
                    "⬇️ PDF (.pdf)",
                    data=markdown_to_pdf(brief),
                    file_name="creative_brief.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as pdf_error:
                st.warning(f"⚠️ PDF generation failed: {pdf_error}")
        else:
            st.info("📄 PDF export not available")

    # ---- Additional output options ----
    st.divider()
    st.subheader("🧩 Generate additional outputs")
    st.caption(
        "Build any of these from the brief above. Each is generated on demand."
    )

    labels = list(cb.EXPORT_GENERATORS.keys())
    cols = st.columns(len(labels))
    for col, label in zip(cols, labels):
        with col:
            if st.button(label, use_container_width=True, key=f"gen_{label}"):
                try:
                    with st.spinner(f"Generating {label}..."):
                        generator = cb.EXPORT_GENERATORS[label]
                        st.session_state.brief_exports[label] = generator(
                            brief, intake, api_key
                        )
                except Exception as e:
                    st.error(f"❌ Error generating {label}: {e}")

    # Render any generated exports with their own downloads
    for label, content in st.session_state.brief_exports.items():
        with st.expander(f"📑 {label}", expanded=True):
            st.markdown(content)
            slug = label.lower().replace(" ", "_").replace("/", "_")
            dcol1, dcol2 = st.columns(2)
            with dcol1:
                st.download_button(
                    "⬇️ Markdown (.md)",
                    data=content,
                    file_name=f"{slug}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key=f"dl_md_{label}",
                )
            with dcol2:
                if PDF_AVAILABLE:
                    try:
                        st.download_button(
                            "⬇️ PDF (.pdf)",
                            data=markdown_to_pdf(content),
                            file_name=f"{slug}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key=f"dl_pdf_{label}",
                        )
                    except Exception:
                        st.caption("PDF unavailable for this output")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        A creative director & presentation strategist, powered by Streamlit and Google Gemini AI<br>
        <small>Understand the presentation before you design the slides</small>
    </div>
""",
    unsafe_allow_html=True,
)
