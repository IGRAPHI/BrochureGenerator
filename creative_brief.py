"""
Core logic for the Presentation Creative Brief generator.

This module turns a short intake (answers to a handful of strategic questions)
into a detailed creative brief for a PowerPoint/slide deck. It deliberately does
NOT generate slides immediately. Its first job is to act like a creative director
and presentation strategist: understand the goal, audience, and context, then
produce a brief that tells the user what their presentation needs before they
begin designing it.

It reuses the Google Gemini configuration helpers from ``main.py`` so the
brochure app and this app share a single, consistent AI setup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import google.generativeai as genai

# Reuse the shared Gemini configuration + PDF helpers from the brochure app
# so there is a single source of truth for API setup and export.
from main import configure_genai, get_api_key, MODEL_NAME  # noqa: F401

# ---------------------------------------------------------------------------
# Domain knowledge: the strategist's mental model
# ---------------------------------------------------------------------------

# The six core presentation needs the app must recognize. Each entry is a short
# label plus the working definition used to brief the model and to explain the
# recommendation back to the user.
PRESENTATION_NEEDS = {
    "Communicate information visually": (
        "Turning data, ideas, or arguments into something an audience can "
        "understand quickly, without relying on dense paragraphs."
    ),
    "Structure and pace a message": (
        "Using slides as the spine of a logical sequence, helping control how "
        "the message unfolds from beginning to end."
    ),
    "Support a speaker": (
        "Creating slides that reinforce spoken delivery with visual cues, key "
        "phrases, diagrams, images, or data points, without becoming a script."
    ),
    "Persuade or drive a decision": (
        "Building a case for a pitch, proposal, donor meeting, investment "
        "request, strategy, or leadership decision."
    ),
    "Simplify complexity": (
        "Breaking down technical, policy, financial, scientific, or "
        "organizational topics using diagrams, charts, hierarchy, and visual "
        "storytelling."
    ),
    "Create a shareable record": (
        "Designing decks that can live after the meeting as reference "
        "documents, leave-behinds, or internal communication tools."
    ),
}

# Option sets surfaced in the intake UI. Keeping them here means the UI and the
# prompt always agree on the available choices.
DELIVERY_MODES = [
    "Presented live by a speaker",
    "Sent as a standalone document (leave-behind)",
    "Both — presented live, then shared afterward",
]

AUDIENCE_KNOWLEDGE = [
    "Knows very little — start from the basics",
    "Some familiarity — knows the context",
    "Expert — deep in the subject",
    "Mixed audience — a range of expertise",
]

CONTENT_NATURES = [
    "Technical",
    "Strategic",
    "Emotional",
    "Financial",
    "Educational",
    "Persuasive",
]

VISUAL_MOODS = [
    "Executive",
    "Editorial",
    "Bold",
    "Institutional",
    "Human",
    "Data-driven",
    "Minimal",
    "Highly visual",
]

CONTENT_READINESS = [
    "I already have most of the content",
    "I have rough notes / fragments",
    "I need help developing the message from scratch",
]

OCCASIONS = [
    "Team / client meeting",
    "Conference talk",
    "Sales or investor pitch",
    "Donor / fundraising presentation",
    "Training or workshop",
    "Report summary",
    "Proposal",
    "Internal update",
]

# The deliverables the app can export. Each maps to a focused generation prompt
# (see ``OUTPUT_PROMPTS``) so the user can request just the piece they need.
OUTPUT_OPTIONS = [
    "Creative brief",
    "Slide outline",
    "Speaker-support notes",
    "Design direction",
    "PowerPoint-ready content plan",
    "AI prompts for visuals",
]


@dataclass
class BriefIntake:
    """Structured answers collected during the intake conversation.

    Every field is optional at the type level so the UI can submit a partial
    intake; the prompt builder gracefully omits anything left blank and tells
    the strategist to infer sensible defaults.
    """

    topic: str = ""
    purpose: str = ""
    audience: str = ""
    delivery_mode: str = ""
    desired_action: str = ""
    audience_knowledge: str = ""
    content_nature: List[str] = field(default_factory=list)
    visual_mood: List[str] = field(default_factory=list)
    content_readiness: str = ""
    brand_guidelines: str = ""
    slide_count: str = ""
    occasion: str = ""
    extra_notes: str = ""


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

STRATEGIST_SYSTEM_PROMPT = """You are a senior creative director and \
presentation strategist. You help people build powerful slide decks by first \
understanding what the presentation truly needs — its goal, audience, context, \
and visual direction — before any slide is designed.

Operating principles you always follow:
- The strongest decks treat slides as VISUAL SUPPORT for a spoken or written \
message, never as a script to be read aloud. When a slide carries the full \
burden of the message, attention shifts away from the presenter and impact \
drops. Push content that belongs in the speaker's mouth into speaker notes.
- You think in terms of these six core presentation needs, and you name the one \
(or combination) that fits best:
  1. Communicate information visually
  2. Structure and pace a message
  3. Support a speaker
  4. Persuade or drive a decision
  5. Simplify complexity
  6. Create a shareable record
- You are opinionated and specific. You make real recommendations (structure, \
slide counts, chart types, layout style) rather than listing generic options.
- You write clean, well-structured Markdown with clear headings and tight, \
scannable bullets. No fluff, no filler.
- When information is missing, you infer reasonable defaults from the context \
and state the assumption briefly rather than asking the user to come back."""


def _format_list(values: List[str]) -> str:
    """Render a list of selected options as a comma-separated string."""
    return ", ".join(v for v in values if v) if values else "(not specified)"


def _val(value: str) -> str:
    """Return a value or a clear placeholder when it is blank."""
    return value.strip() if value and value.strip() else "(not specified)"


def build_intake_summary(intake: BriefIntake) -> str:
    """Render the intake answers as a labelled block for the model.

    Args:
        intake: The collected intake answers.

    Returns:
        A human-readable, labelled summary of everything the user told us.
    """
    return f"""INTAKE ANSWERS
- Topic / subject of the presentation: {_val(intake.topic)}
- What the presentation is for (purpose): {_val(intake.purpose)}
- Who will see it (audience): {_val(intake.audience)}
- How it will be delivered: {_val(intake.delivery_mode)}
- Decision or action wanted afterward: {_val(intake.desired_action)}
- How much the audience already knows: {_val(intake.audience_knowledge)}
- Nature of the content: {_format_list(intake.content_nature)}
- Desired visual mood: {_format_list(intake.visual_mood)}
- Content readiness: {_val(intake.content_readiness)}
- Brand guidelines (colors, logos, fonts, templates): {_val(intake.brand_guidelines)}
- Target number of slides: {_val(intake.slide_count)}
- Occasion / setting: {_val(intake.occasion)}
- Anything else: {_val(intake.extra_notes)}"""


# The master brief is the headline deliverable. The section list mirrors the
# format the product promises to the user.
BRIEF_PROMPT_TEMPLATE = """Using the intake below, produce a detailed CREATIVE \
BRIEF for this presentation. Do not design the slides yet beyond the \
slide-by-slide direction — focus on strategy and direction.

{intake_summary}

Write the brief in Markdown with exactly these sections, in this order:

# Creative Brief: <a short, specific title for this presentation>

## Project Overview
A short summary of what the presentation needs to accomplish.

## Presentation Type
Name the main presentation need (or combination) from the six core needs, and \
explain in one or two sentences why it fits. Also state plainly whether the \
deck is meant to support a live speaker, persuade a decision-maker, explain \
complex information, or work as a leave-behind document.

## Audience
Who the deck is for, what they already know, and what they need to understand \
or feel by the end.

## Communication Goal
The single core message and the desired outcome / action.

## Recommended Structure
A logical outline with a clear beginning, middle, and ending, plus a note on \
pacing (where to slow down, where to move fast). Recommend a target slide count.

## Slide-by-Slide Direction
A numbered slide list. For EACH slide give:
- **Title** — the working slide title
- **Purpose** — the one job this slide does
- **Content notes** — what goes on the slide (kept lean) vs. what should move \
to speaker notes
- **Visual treatment** — layout, and any chart, diagram, image, or icon

## Visual Style
Recommended design direction: layout style, image use, icons, charts, \
diagrams, typography, color mood, and overall visual tone. Honor any brand \
guidelines provided.

## Data Visualization Needs
Where data appears, recommend the specific chart/diagram type and what it must \
make obvious. If there is no data, say so and suggest what could strengthen the \
argument.

## Content Strategy
What to shorten, emphasize, visualize, move to speaker notes, or turn into \
charts/diagrams. Be specific.

## Tone of Voice & Level of Detail
The voice the deck should use and how dense each slide should be.

## Design Principles
A short checklist of principles to keep the deck clear, modern, visually \
engaging, and easy to follow.

Be concrete and decisive throughout."""


# Focused follow-on deliverables. Each is generated from the same intake plus
# the already-produced master brief so the outputs stay consistent.
OUTPUT_PROMPTS = {
    "Slide outline": """From the brief and intake below, output ONLY a clean \
slide outline as a numbered Markdown list. Each line: the slide number, the \
slide title, and a 4-8 word description of its single purpose. No other prose.

{context}""",
    "Speaker-support notes": """From the brief and intake below, write \
SPEAKER-SUPPORT NOTES, organized slide by slide. For each slide give 2-4 \
talking-point bullets the presenter would SAY out loud — the narrative that the \
slide visually supports. These are spoken cues, not a word-for-word script, and \
they must contain the message detail that should stay OFF the slide.

{context}""",
    "Design direction": """From the brief and intake below, write a focused \
DESIGN DIRECTION document: color palette (with suggested hex values that honor \
any brand guidance), typography pairing, layout/grid style, iconography and \
imagery style, chart styling, and 5-7 do/don't rules. Markdown only.

{context}""",
    "PowerPoint-ready content plan": """From the brief and intake below, \
produce a POWERPOINT-READY CONTENT PLAN. For every slide output a block with: \
Slide number and layout type (e.g. Title, Section, Two-content, Chart, Quote, \
Closing); the exact on-slide headline; the exact on-slide body text or bullets \
(lean — what the audience reads); the speaker notes (what the presenter says); \
and a visual asset note (chart/diagram/image/icon). Make it ready to type \
straight into PowerPoint.

{context}""",
    "AI prompts for visuals": """From the brief and intake below, write a set \
of ready-to-use AI GENERATION PROMPTS for the deck's visuals — images, icons, \
diagrams, and background/layout art — matched to the recommended visual style. \
Group them by slide or by asset type. Each prompt should be specific enough to \
paste directly into an image or diagram generator.

{context}""",
}


# ---------------------------------------------------------------------------
# Model helpers
# ---------------------------------------------------------------------------

def _strategist_model() -> "genai.GenerativeModel":
    """Return the Gemini model configured as the presentation strategist."""
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=STRATEGIST_SYSTEM_PROMPT,
    )


def generate_creative_brief(intake: BriefIntake, api_key: str | None = None) -> str:
    """Generate the master creative brief from the intake answers.

    Args:
        intake: The collected intake answers.
        api_key: Optional Gemini API key. Falls back to the environment.

    Returns:
        The creative brief as Markdown.

    Raises:
        ValueError: If no API key is available.
    """
    configure_genai(api_key)
    model = _strategist_model()

    prompt = BRIEF_PROMPT_TEMPLATE.format(
        intake_summary=build_intake_summary(intake)
    )
    response = model.generate_content(prompt)
    return getattr(response, "text", str(response))


def generate_output(
    option: str,
    intake: BriefIntake,
    brief: str,
    api_key: str | None = None,
) -> str:
    """Generate a focused follow-on deliverable for the deck.

    Args:
        option: One of ``OUTPUT_PROMPTS`` keys (e.g. "Slide outline").
        intake: The collected intake answers.
        brief: The already-generated master creative brief, for consistency.
        api_key: Optional Gemini API key. Falls back to the environment.

    Returns:
        The requested deliverable as Markdown.

    Raises:
        ValueError: If the option is unknown or no API key is available.
    """
    if option == "Creative brief":
        # The master brief is generated separately; return it as-is.
        return brief

    if option not in OUTPUT_PROMPTS:
        raise ValueError(f"Unknown output option: {option!r}")

    configure_genai(api_key)
    model = _strategist_model()

    context = (
        f"{build_intake_summary(intake)}\n\n"
        f"CREATIVE BRIEF ALREADY PRODUCED:\n{brief}"
    )
    prompt = OUTPUT_PROMPTS[option].format(context=context)
    response = model.generate_content(prompt)
    return getattr(response, "text", str(response))
