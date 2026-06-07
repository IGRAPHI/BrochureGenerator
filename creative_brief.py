"""
Presentation Creative Brief engine.

This module turns a short intake (purpose, audience, delivery context, etc.)
into a detailed creative brief and a set of downstream artifacts (slide
outline, speaker-support notes, design direction, a PowerPoint-ready content
plan, and AI prompts for generating visuals).

It acts like a creative director and presentation strategist rather than a
slide generator: its first job is to understand what the presentation needs
to accomplish before any slide is designed.

Core AI/PDF helpers are reused from main.py to avoid duplication.
"""

from __future__ import annotations

from typing import Dict, List

from main import configure_genai, get_model, get_api_key, PDF_AVAILABLE  # re-exported


# ---------------------------------------------------------------------------
# Presentation philosophy (shared across every generated artifact)
# ---------------------------------------------------------------------------

PRESENTATION_PHILOSOPHY = """\
Core philosophy you must always apply:
- The strongest decks treat slides as VISUAL SUPPORT for a message, not as a
  script to be read aloud. When a slide carries the full burden of the
  message, attention shifts away from the presenter and impact drops.
- Favor one idea per slide, short headlines that state a point (not a topic),
  and visuals (charts, diagrams, images, icons) over dense paragraphs.
- Detailed prose belongs in speaker notes or a leave-behind appendix, not on
  the slide itself.
- Structure controls how a message unfolds: every deck needs a clear
  beginning (set up the stakes), middle (build the case), and end (land the
  decision or takeaway).
"""


# ---------------------------------------------------------------------------
# The six main presentation needs the app recognizes
# ---------------------------------------------------------------------------

PRESENTATION_NEEDS: Dict[str, Dict[str, str]] = {
    "Communicate information visually": {
        "summary": "Turn data, ideas, or arguments into something an audience "
        "understands quickly, without relying on dense paragraphs.",
    },
    "Structure and pace a message": {
        "summary": "Use slides as the spine of a logical sequence, controlling "
        "how the message unfolds from beginning to end.",
    },
    "Support a speaker": {
        "summary": "Reinforce spoken delivery with visual cues, key phrases, "
        "diagrams, images, or data points, without becoming a script.",
    },
    "Persuade or drive a decision": {
        "summary": "Build a case for a pitch, proposal, donor meeting, "
        "investment request, strategy, or leadership decision.",
    },
    "Simplify complexity": {
        "summary": "Break down technical, policy, financial, scientific, or "
        "organizational topics using diagrams, charts, hierarchy, and visual "
        "storytelling.",
    },
    "Create a shareable record": {
        "summary": "Design decks that live after the meeting as reference "
        "documents, leave-behinds, or internal communication tools.",
    },
}


# ---------------------------------------------------------------------------
# Intake option vocabularies (used to drive the UI and validate input)
# ---------------------------------------------------------------------------

DELIVERY_MODES: List[str] = [
    "Presented live by a speaker",
    "Sent as a standalone document (leave-behind)",
    "Both: presented live, then shared afterward",
]

KNOWLEDGE_LEVELS: List[str] = [
    "Beginners — little prior knowledge",
    "Some familiarity",
    "Highly knowledgeable / expert",
    "Mixed audience",
]

CONTENT_NATURES: List[str] = [
    "Technical",
    "Strategic",
    "Emotional",
    "Financial",
    "Educational",
    "Persuasive",
]

VISUAL_MOODS: List[str] = [
    "Executive",
    "Editorial",
    "Bold",
    "Institutional",
    "Human",
    "Data-driven",
    "Minimal",
    "Highly visual",
]

CONTENT_READINESS: List[str] = [
    "I already have most of the content",
    "I have rough notes / fragments",
    "I need help developing the message from scratch",
]

OCCASIONS: List[str] = [
    "Internal team meeting",
    "Conference / keynote",
    "Sales or business pitch",
    "Donor / fundraising presentation",
    "Investment request",
    "Training / workshop",
    "Report summary",
    "Proposal",
    "Internal update",
    "Other",
]


# ---------------------------------------------------------------------------
# Intake -> prompt helpers
# ---------------------------------------------------------------------------

def _line(label: str, value) -> str:
    """Render one intake field, skipping empties."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        value = ", ".join(str(v) for v in value if v)
    value = str(value).strip()
    if not value:
        return ""
    return f"- {label}: {value}\n"


def format_intake(intake: Dict) -> str:
    """Render the intake dictionary into a readable block for prompting."""
    parts = [
        _line("Topic / what the presentation is about", intake.get("topic")),
        _line("Purpose (what it must accomplish)", intake.get("purpose")),
        _line("Audience", intake.get("audience")),
        _line("How the deck will be delivered", intake.get("delivery_mode")),
        _line("Desired decision or action afterward", intake.get("desired_outcome")),
        _line("Audience's existing knowledge level", intake.get("knowledge_level")),
        _line("Nature of the content", intake.get("content_nature")),
        _line("Desired feel / visual mood", intake.get("visual_mood")),
        _line("Content readiness", intake.get("content_readiness")),
        _line("Brand guidelines (colors, logos, fonts, templates)", intake.get("brand")),
        _line("Approximate number of slides", intake.get("slide_count")),
        _line("Occasion / setting", intake.get("occasion")),
        _line("Anything else to consider", intake.get("notes")),
    ]
    body = "".join(p for p in parts if p)
    return body or "- (No details provided)\n"


def _needs_reference() -> str:
    """A compact reference of the six presentation needs for the model."""
    lines = ["The six main presentation needs you can recognize and combine:"]
    for name, meta in PRESENTATION_NEEDS.items():
        lines.append(f"- {name}: {meta['summary']}")
    return "\n".join(lines)


def _run(system_instruction: str, prompt: str, api_key: str = None) -> str:
    """Configure Gemini and run a single generation, returning text."""
    configure_genai(api_key)
    model = get_model(system_instruction=system_instruction)
    response = model.generate_content(prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("The model returned an empty response.")
    return text.strip()


# ---------------------------------------------------------------------------
# Primary artifact: the creative brief
# ---------------------------------------------------------------------------

BRIEF_SYSTEM_PROMPT = (
    "You are a senior creative director and presentation strategist. You help "
    "people figure out what their presentation truly needs BEFORE they start "
    "designing slides. You are thoughtful, decisive, and practical. You write "
    "clear, well-structured briefs in Markdown.\n\n"
    + PRESENTATION_PHILOSOPHY
)


def generate_creative_brief(intake: Dict, api_key: str = None) -> str:
    """
    Generate a detailed creative brief from the intake answers.

    Args:
        intake: Dictionary of intake answers (see format_intake for keys).
        api_key: Optional Google Gemini API key.

    Returns:
        The creative brief as Markdown.
    """
    prompt = f"""{_needs_reference()}

A user has completed an intake for a presentation they need to create. Here is
what they told you:

{format_intake(intake)}

Produce a detailed creative brief. Infer sensible defaults for anything the
user did not specify, and call out assumptions you made. Use this exact
section structure with Markdown headings:

# Creative Brief: <a short, specific project name>

## Project Overview
A short summary of what the presentation needs to accomplish.

## Presentation Type
Identify the main presentation need(s) from the six categories above (a single
category or a combination). State the primary need and any secondary needs,
and briefly justify the choice.

## Audience
Who the deck is for and what they need to understand or feel. Note their
knowledge level and what matters to them.

## Communication Goal
The core message in one or two sentences, plus the desired outcome (the
decision or action you want afterward).

## Recommended Structure
A logical outline for the deck with a clear beginning, middle, and ending.
Recommend pacing and an appropriate slide count (respect the user's count if
they gave one, otherwise suggest a range and explain why).

## Slide-by-Slide Direction
A numbered slide list. For EACH slide give:
- **Title** (a point-making headline, not just a topic)
- **Purpose** (what this slide accomplishes)
- **Content notes** (what goes on the slide vs. what moves to speaker notes)
- **Visual treatment** (layout, chart, diagram, image, or icon idea)

## Visual Style
Recommended design direction: layout style, image use, icons, charts,
diagrams, typography, color mood, and overall visual tone. Honor any brand
guidelines provided.

## Content Strategy
What should be shortened, emphasized, visualized, moved to speaker notes, or
turned into charts/diagrams. Be specific.

## Design Principles
3-6 principles that keep this specific deck clear, modern, visually engaging,
and easy to follow.

Write for this exact presentation — avoid generic filler.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, api_key)


# ---------------------------------------------------------------------------
# Downstream export artifacts
# ---------------------------------------------------------------------------

def generate_slide_outline(brief: str, intake: Dict, api_key: str = None) -> str:
    """A clean, copy-ready slide outline derived from the brief."""
    prompt = f"""Below is a creative brief for a presentation.

Intake summary:
{format_intake(intake)}

Creative brief:
---
{brief}
---

Produce a clean, copy-ready SLIDE OUTLINE in Markdown. For each slide use:

### Slide N — <headline>
- **Purpose:** ...
- **On-slide content:** short bullets only (the visible slide text)
- **Visual:** the recommended visual element

Keep on-slide text tight (headlines and short bullets), consistent with the
principle that slides are visual support, not a script. Start with a title
slide and end with a closing/call-to-action slide.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, api_key)


def generate_speaker_notes(brief: str, intake: Dict, api_key: str = None) -> str:
    """Speaker-support notes: what to say, not what to read off the slide."""
    prompt = f"""Below is a creative brief for a presentation.

Intake summary:
{format_intake(intake)}

Creative brief:
---
{brief}
---

Write SPEAKER-SUPPORT NOTES in Markdown, organized slide by slide
(### Slide N — <headline>). For each slide provide:
- The key point the speaker should land.
- A natural-language talking-track (2-5 sentences) the speaker can say.
- An optional transition line into the next slide.

The notes carry the detail so the slides can stay visual. Do NOT just repeat
the on-slide bullets — expand on them conversationally.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, api_key)


def generate_design_direction(brief: str, intake: Dict, api_key: str = None) -> str:
    """A focused visual/design direction document."""
    prompt = f"""Below is a creative brief for a presentation.

Intake summary:
{format_intake(intake)}

Creative brief:
---
{brief}
---

Write a focused DESIGN DIRECTION document in Markdown covering:

## Color Palette
Suggest specific colors with hex codes (honor any brand colors provided) and
say where each is used.

## Typography
Recommend heading and body typefaces (or safe system/Office alternatives) and
sizing guidance.

## Layout System
Grid, margins, title placement, and a few reusable slide layout patterns.

## Imagery & Iconography
Photography style, illustration/icon style, and usage rules.

## Data Visualization Style
How charts and diagrams should look and behave.

## Do / Don't
A short list of design do's and don'ts for this deck.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, api_key)


def generate_content_plan(brief: str, intake: Dict, api_key: str = None) -> str:
    """A PowerPoint-ready content plan (exact text blocks per slide)."""
    prompt = f"""Below is a creative brief for a presentation.

Intake summary:
{format_intake(intake)}

Creative brief:
---
{brief}
---

Produce a POWERPOINT-READY CONTENT PLAN in Markdown — the exact text someone
can paste into PowerPoint, slide by slide:

### Slide N
- **Layout:** (e.g., Title, Title + Content, Two Content, Section Header)
- **Title text:** the exact headline
- **Body text:** the exact bullets/short lines for the slide (visual support only)
- **Visual placeholder:** describe the chart/diagram/image to drop in
- **Speaker notes:** the exact text for the notes pane

Be concrete and final — this is the build-ready version.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, api_key)


VISUAL_PROMPTS_SYSTEM = (
    "You are an art director who writes precise prompts for AI image, icon, "
    "diagram, and layout generators. Your prompts are specific about subject, "
    "style, composition, color, and aspect ratio."
)


def generate_visual_prompts(brief: str, intake: Dict, api_key: str = None) -> str:
    """AI prompts for generating visuals, icons, diagrams, or layouts."""
    prompt = f"""Below is a creative brief for a presentation.

Intake summary:
{format_intake(intake)}

Creative brief:
---
{brief}
---

Write a set of AI GENERATION PROMPTS in Markdown the user can paste into image
or diagram tools. Organize as:

## Cover / Hero Image Prompts
## Section Divider Prompts
## Icon Set Prompts
## Diagram / Schematic Prompts
## Background / Texture Prompts

For each, give 1-3 ready-to-copy prompts in fenced code blocks. Reflect the
brief's visual style and any brand colors. Where relevant, note a recommended
aspect ratio (e.g., 16:9) and a negative-prompt hint.
"""
    return _run(VISUAL_PROMPTS_SYSTEM, prompt, api_key)


# Map of export label -> generator function, for convenient UI wiring.
EXPORT_GENERATORS = {
    "Slide outline": generate_slide_outline,
    "Speaker-support notes": generate_speaker_notes,
    "Design direction": generate_design_direction,
    "PowerPoint-ready content plan": generate_content_plan,
    "AI visual prompts": generate_visual_prompts,
}


# ---------------------------------------------------------------------------
# Minimal CLI for quick testing without the Streamlit UI
# ---------------------------------------------------------------------------

def _cli() -> None:
    import sys

    if not get_api_key():
        print("Error: GENAI_API_KEY not found. Add it to your .env file.")
        sys.exit(1)

    print("Presentation Creative Brief — quick intake (press Enter to skip)\n")
    intake = {
        "topic": input("What is the presentation about? "),
        "purpose": input("What is it for / what must it accomplish? "),
        "audience": input("Who will see it? "),
        "delivery_mode": input("Live, document, or both? "),
        "desired_outcome": input("What decision or action should follow? "),
        "occasion": input("Occasion (pitch, conference, training...)? "),
        "slide_count": input("Approximate number of slides? "),
    }

    print("\nGenerating creative brief...\n")
    brief = generate_creative_brief(intake)
    print(brief)


if __name__ == "__main__":
    _cli()
