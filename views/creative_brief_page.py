"""
Presentation Strategy Studio page.

A creative-director-style intake that turns a few smart questions into a
detailed creative brief and a set of build-ready artifacts (slide outline,
speaker notes, design direction, content plan, AI visual prompts).

The AI provider is pluggable — Claude (default), Gemini (optional), or Demo
Mode (no key). Core logic lives in creative_brief.py / providers.py; this file
is only the Streamlit UI.
"""

import streamlit as st

import providers
import creative_brief as cb
from pdf_export import markdown_to_pdf, PDF_AVAILABLE

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "brief" not in st.session_state:
    st.session_state.brief = None
if "brief_intake" not in st.session_state:
    st.session_state.brief_intake = None
if "brief_exports" not in st.session_state:
    st.session_state.brief_exports = {}  # label -> generated markdown


def _load_sample():
    """Populate the intake form with the demo sample (form-widget keys)."""
    s = cb.SAMPLE_INTAKE
    mapping = {
        "cb_topic": "topic", "cb_purpose": "purpose", "cb_audience": "audience",
        "cb_mode": "mode", "cb_delivery": "delivery_mode", "cb_outcome": "desired_outcome",
        "cb_knowledge": "knowledge_level", "cb_occasion": "occasion",
        "cb_readiness": "content_readiness", "cb_slides": "slide_count",
        "cb_content_nature": "content_nature", "cb_visual_mood": "visual_mood",
        "cb_brand_colors": "brand_colors", "cb_brand_fonts": "brand_fonts",
        "cb_brand_logo": "brand_logo", "cb_brand_tone": "brand_tone",
        "cb_brand_guidelines": "brand_guidelines", "cb_notes": "notes",
    }
    for widget_key, intake_key in mapping.items():
        st.session_state[widget_key] = s.get(intake_key, "")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    f'<div class="main-header">📊 {cb.APP_NAME}</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">A creative director for your deck — understand the '
    "presentation before you design a single slide</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar: provider selection + the six needs reference
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🤖 AI provider")

    default_name = providers.resolve_provider_name()
    options = ["Claude (recommended)", "Gemini (optional)", "Demo (no key)"]
    default_index = {"claude": 0, "gemini": 1, "demo": 2}.get(default_name, 0)
    provider_choice = st.radio(
        "Model provider", options, index=default_index, label_visibility="collapsed"
    )

    key = None
    if provider_choice.startswith("Claude"):
        selected_name = providers.CLAUDE
        if providers.anthropic_key():
            st.success("✓ Anthropic API key loaded")
        else:
            key = st.text_input("Anthropic API key", type="password") or None
            if not key:
                st.info("No key yet → runs in **Demo Mode**.")
    elif provider_choice.startswith("Gemini"):
        selected_name = providers.GEMINI
        if providers.gemini_key():
            st.success("✓ Gemini API key loaded")
        else:
            key = st.text_input("Gemini API key", type="password") or None
            if not key:
                st.info("No key yet → runs in **Demo Mode**.")
    else:
        selected_name = providers.DEMO

    active_provider = providers.get_provider(preferred=selected_name, api_key=key)

    if active_provider.is_mock:
        st.warning(f"🟡 **Demo Mode** — {active_provider.reason}. Output is illustrative.")
    elif active_provider.name == providers.CLAUDE:
        st.caption(f"🟢 Claude mode · `{active_provider.model}`")
    else:
        st.caption(f"🔵 Gemini mode · `{active_provider.model}`")

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
top1, top2 = st.columns([3, 1])
with top1:
    st.caption(
        "Answer what you can — the strategist infers sensible defaults and notes "
        "its assumptions for anything you leave blank."
    )
with top2:
    st.button("✨ Load sample", on_click=_load_sample, use_container_width=True,
              help="Fill the form with a worked example so you can try it instantly.")

with st.form("intake_form"):
    st.text_input("What is the presentation about?", key="cb_topic",
                  placeholder="e.g., Our Q3 product strategy and 2026 roadmap")
    st.text_area("What is it for — what must it accomplish?", key="cb_purpose",
                 placeholder="e.g., Get leadership to approve budget for two new hires",
                 height=80)

    st.selectbox(
        "Presentation mode (this strongly shapes the whole brief)",
        cb.PRESENTATION_MODE_NAMES, key="cb_mode",
        help="; ".join(f"{m}: {meta['summary']}" for m, meta in cb.PRESENTATION_MODES.items()),
    )

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Who will see it?", key="cb_audience",
                      placeholder="e.g., Executive leadership team")
        st.selectbox("Live or document?", cb.DELIVERY_MODES, key="cb_delivery")
        st.selectbox("How much does the audience already know?",
                     cb.KNOWLEDGE_LEVELS, key="cb_knowledge")
        st.selectbox("Occasion / setting", cb.OCCASIONS, key="cb_occasion")
    with col2:
        st.text_input("What decision or action should happen afterward?",
                      key="cb_outcome", placeholder="e.g., Sign off on the proposed plan")
        st.selectbox("Do you have content, or need help developing it?",
                     cb.CONTENT_READINESS, key="cb_readiness")
        st.text_input("How many slides? (optional)", key="cb_slides",
                      placeholder="e.g., 10-12")

    st.multiselect("Nature of the content", cb.CONTENT_NATURES, key="cb_content_nature")
    st.multiselect("How should the deck feel?", cb.VISUAL_MOODS, key="cb_visual_mood")

    # ---- Brand input ----
    st.markdown("**🎨 Brand input** (optional — paste anything you have)")
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        st.text_input("Brand colors", key="cb_brand_colors",
                      placeholder="e.g., #0B5FFF primary, #111827 ink, #F8FAFC bg")
        st.text_input("Fonts / typography", key="cb_brand_fonts",
                      placeholder="e.g., Headings: Space Grotesk; Body: Inter")
    with bcol2:
        st.text_input("Logo notes", key="cb_brand_logo",
                      placeholder="e.g., Wordmark top-left, keep clear space")
        st.text_input("Tone of voice", key="cb_brand_tone",
                      placeholder="e.g., Confident, warm, credible")
    st.text_area("Other brand guidelines (or paste references)", key="cb_brand_guidelines",
                 height=68)

    st.text_area("Anything else the strategist should consider?", key="cb_notes", height=68)

    submitted = st.form_submit_button(
        "🎬 Generate Creative Brief", type="primary", use_container_width=True
    )

# ---------------------------------------------------------------------------
# Handle submission
# ---------------------------------------------------------------------------
if submitted:
    intake = {
        "topic": st.session_state.get("cb_topic", ""),
        "purpose": st.session_state.get("cb_purpose", ""),
        "audience": st.session_state.get("cb_audience", ""),
        "mode": st.session_state.get("cb_mode", ""),
        "delivery_mode": st.session_state.get("cb_delivery", ""),
        "desired_outcome": st.session_state.get("cb_outcome", ""),
        "knowledge_level": st.session_state.get("cb_knowledge", ""),
        "content_nature": st.session_state.get("cb_content_nature", []),
        "visual_mood": st.session_state.get("cb_visual_mood", []),
        "content_readiness": st.session_state.get("cb_readiness", ""),
        "brand_colors": st.session_state.get("cb_brand_colors", ""),
        "brand_fonts": st.session_state.get("cb_brand_fonts", ""),
        "brand_logo": st.session_state.get("cb_brand_logo", ""),
        "brand_tone": st.session_state.get("cb_brand_tone", ""),
        "brand_guidelines": st.session_state.get("cb_brand_guidelines", ""),
        "slide_count": st.session_state.get("cb_slides", ""),
        "occasion": st.session_state.get("cb_occasion", ""),
        "notes": st.session_state.get("cb_notes", ""),
    }
    if not (intake["topic"] or intake["purpose"]):
        st.error("❌ Please describe at least the topic or the purpose of the presentation.")
    else:
        try:
            spinner = "🧠 Thinking like a creative director..." if not active_provider.is_mock \
                else "🧩 Building a Demo-Mode sample..."
            with st.spinner(spinner):
                brief = cb.generate_creative_brief(intake, active_provider)
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
            "⬇️ Markdown (.md)", data=brief, file_name="creative_brief.md",
            mime="text/markdown", use_container_width=True,
        )
    with col2:
        if PDF_AVAILABLE:
            try:
                st.download_button(
                    "⬇️ PDF (.pdf)", data=markdown_to_pdf(brief),
                    file_name="creative_brief.pdf", mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as pdf_error:
                st.warning(f"⚠️ PDF generation failed: {pdf_error}")
        else:
            st.info("📄 PDF export not available")

    # ---- Additional output options ----
    st.divider()
    st.subheader("🧩 Generate additional outputs")
    st.caption("Build any of these from the brief above. Each is generated on demand.")

    labels = list(cb.EXPORT_GENERATORS.keys())
    cols = st.columns(len(labels))
    for col, label in zip(cols, labels):
        with col:
            if st.button(label, use_container_width=True, key=f"gen_{label}"):
                try:
                    with st.spinner(f"Generating {label}..."):
                        generator = cb.EXPORT_GENERATORS[label]
                        st.session_state.brief_exports[label] = generator(
                            brief, intake, active_provider
                        )
                except Exception as e:
                    st.error(f"❌ Error generating {label}: {e}")

    for label, content in st.session_state.brief_exports.items():
        with st.expander(f"📑 {label}", expanded=True):
            st.markdown(content)
            slug = label.lower().replace(" ", "_").replace("/", "_")
            dcol1, dcol2 = st.columns(2)
            with dcol1:
                st.download_button(
                    "⬇️ Markdown (.md)", data=content, file_name=f"{slug}.md",
                    mime="text/markdown", use_container_width=True, key=f"dl_md_{label}",
                )
            with dcol2:
                if PDF_AVAILABLE:
                    try:
                        st.download_button(
                            "⬇️ PDF (.pdf)", data=markdown_to_pdf(content),
                            file_name=f"{slug}.pdf", mime="application/pdf",
                            use_container_width=True, key=f"dl_pdf_{label}",
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
        A creative director & presentation strategist · Claude-first, Gemini optional, Demo Mode always-on<br>
        <small>Understand the presentation before you design the slides</small>
    </div>
""",
    unsafe_allow_html=True,
)
