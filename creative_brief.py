"""
Presentation Strategy Studio — brief engine.

Turns a short intake (purpose, audience, presentation mode, brand, etc.) into a
detailed, mode-adaptive creative brief plus a set of downstream artifacts
(slide outline, speaker-support notes, design direction, a PowerPoint-ready
content plan, and AI prompts for generating visuals).

It acts like a professional creative director and presentation strategist
rather than a slide generator: its first job is to understand what the
presentation needs to accomplish — and what *kind* of deck it is — before any
slide is designed.

The AI provider is pluggable (Claude by default, Gemini optional, Demo/Mock
when no key is available) via providers.py. PDF export lives in pdf_export.py.
"""

from __future__ import annotations

from typing import Dict, List

import providers
from providers import get_provider
from pdf_export import markdown_to_pdf, PDF_AVAILABLE  # re-exported for the UI

# Public product name (kept in one place so the UI and docs stay consistent).
APP_NAME = "Presentation Strategy Studio"


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
# Presentation modes — each strongly shapes structure, tone, and design so the
# brief is never generic. "needs" ties the mode back to the six core needs;
# "directives" are injected verbatim into the prompt.
# ---------------------------------------------------------------------------

PRESENTATION_MODES: Dict[str, Dict[str, str]] = {
    "Live speaker support": {
        "summary": "Minimal slides that back a speaker in the room.",
        "needs": "Support a speaker",
        "directives": (
            "This deck SUPPORTS A LIVE SPEAKER. Slides must be glanceable from "
            "the back of a room: one idea per slide, very few words, large "
            "visuals or a single key number/phrase. Never write full "
            "sentences on slides. The speaker carries the narrative; push all "
            "explanation, transitions, and detail into the speaker notes. "
            "Optimize for the speaker not losing the audience to the screen."
        ),
    },
    "Executive decision deck": {
        "summary": "Drive a fast, confident decision from busy leaders.",
        "needs": "Persuade or drive a decision",
        "directives": (
            "This is an EXECUTIVE DECISION DECK. Lead with the bottom line up "
            "front (BLUF): the recommendation/ask on or near slide 1, then an "
            "executive summary. Be crisp, data-backed, and decision-oriented. "
            "Present clear options with a recommendation, anticipate the top "
            "objections, and quantify impact. Keep the main line short; move "
            "supporting detail to an appendix. Tone: confident, concise, "
            "credible. Minimize cognitive load for time-pressed executives."
        ),
    },
    "Donor / proposal deck": {
        "summary": "Win support and funding with story plus credibility.",
        "needs": "Persuade or drive a decision",
        "directives": (
            "This is a DONOR / PROPOSAL DECK. Open with an emotional, human "
            "hook and a vivid sense of the problem/need. Balance emotion with "
            "evidence: show your solution, proof of impact, and credibility. "
            "Make the ask explicit (amount, use of funds, what it unlocks) and "
            "paint the vision of what success looks like. End with a strong, "
            "specific call to action."
        ),
    },
    "Training or workshop deck": {
        "summary": "Teach a skill or concept that sticks.",
        "needs": "Simplify complexity",
        "directives": (
            "This is a TRAINING / WORKSHOP DECK. Start with clear learning "
            "objectives. Chunk content into digestible modules with examples, "
            "checkpoints, and exercises. Use progressive disclosure and "
            "frequent recaps/summaries. Some on-slide reference content is "
            "acceptable here because the deck doubles as a learning aid, but "
            "still favor visuals and worked examples over walls of text. End "
            "each module and the deck with concrete takeaways."
        ),
    },
    "Conference presentation": {
        "summary": "A memorable talk for a large audience.",
        "needs": "Communicate information visually",
        "directives": (
            "This is a CONFERENCE PRESENTATION for a large audience and a big "
            "screen. Build a strong narrative arc with a memorable opening "
            "hook and a quotable closing. One bold message per slide, large "
            "imagery, almost no body text. Optimize for memorability and "
            "shareability (a slide someone would photograph)."
        ),
    },
    "Leave-behind / shareable document": {
        "summary": "A deck that stands alone after the meeting.",
        "needs": "Create a shareable record",
        "directives": (
            "This is a LEAVE-BEHIND / SHAREABLE DOCUMENT read without a "
            "presenter. Each slide must stand alone: provide enough on-slide "
            "context, self-explanatory charts with captions, clear section "
            "headers, and a summary/contents for navigation. A slightly higher "
            "text density is acceptable since there is no speaker — but keep it "
            "skimmable and structured, not a wall of prose."
        ),
    },
    "Technical explanation deck": {
        "summary": "Make a complex system or process clear.",
        "needs": "Simplify complexity",
        "directives": (
            "This is a TECHNICAL EXPLANATION DECK. Define terms, reduce or "
            "explain jargon, and lean heavily on diagrams, schematics, "
            "flowcharts, and before/after comparisons. Layer detail "
            "progressively (overview first, depth later) and use analogies to "
            "anchor hard concepts. Move deep technical detail to an appendix."
        ),
    },
    "Visual report summary": {
        "summary": "Turn data and results into a scannable story.",
        "needs": "Communicate information visually",
        "directives": (
            "This is a VISUAL REPORT SUMMARY. Be data-forward: dashboards, "
            "KPIs, trends, and comparisons. Every chart's TITLE must state the "
            "insight (the takeaway), not just the metric. Keep prose minimal "
            "and the whole thing scannable; lead each section with the "
            "headline finding."
        ),
    },
}


# ---------------------------------------------------------------------------
# Intake option vocabularies (used to drive the UI and validate input)
# ---------------------------------------------------------------------------

PRESENTATION_MODE_NAMES: List[str] = list(PRESENTATION_MODES.keys())

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
# Sample / demo intake (lets users test the app without filling every field)
# ---------------------------------------------------------------------------

SAMPLE_INTAKE: Dict = {
    "topic": "Series A funding pitch for NorthWind Robotics — autonomous warehouse robots",
    "purpose": "Convince venture investors to lead a $12M Series A round",
    "audience": "Partners at growth-stage venture capital funds",
    "mode": "Executive decision deck",
    "delivery_mode": "Both: presented live, then shared afterward",
    "desired_outcome": "Secure a term sheet or a partner-level follow-up meeting",
    "knowledge_level": "Some familiarity",
    "content_nature": ["Strategic", "Financial", "Persuasive"],
    "visual_mood": ["Executive", "Bold", "Data-driven"],
    "content_readiness": "I have rough notes / fragments",
    "brand_colors": "#0B3D91 deep blue, #FF6B35 orange accent, #111827 near-black, #F8FAFC light bg",
    "brand_fonts": "Headings: Space Grotesk; Body: Inter",
    "brand_logo": "Wordmark logo top-left with clear space; white logo on dark, dark logo on light",
    "brand_tone": "Confident, ambitious, and credible — not hypey",
    "brand_guidelines": "",
    "slide_count": "12-14",
    "occasion": "Investment request",
    "notes": "Strong traction (3x YoY revenue) and a defensible tech moat. Expect "
    "objections on market timing and unit economics — address both head-on.",
}


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
        _line("Presentation mode", intake.get("mode")),
        _line("Audience", intake.get("audience")),
        _line("How the deck will be delivered", intake.get("delivery_mode")),
        _line("Desired decision or action afterward", intake.get("desired_outcome")),
        _line("Audience's existing knowledge level", intake.get("knowledge_level")),
        _line("Nature of the content", intake.get("content_nature")),
        _line("Desired feel / visual mood", intake.get("visual_mood")),
        _line("Content readiness", intake.get("content_readiness")),
        _line("Brand — colors", intake.get("brand_colors")),
        _line("Brand — fonts/typography", intake.get("brand_fonts")),
        _line("Brand — logo notes", intake.get("brand_logo")),
        _line("Brand — tone of voice", intake.get("brand_tone")),
        _line("Brand — additional guidelines", intake.get("brand_guidelines")),
        # Back-compat with the original single "brand" field.
        _line("Brand guidelines", intake.get("brand")),
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


def _mode_meta(intake: Dict) -> Dict[str, str]:
    return PRESENTATION_MODES.get((intake.get("mode") or "").strip(), {})


def _mode_directives(intake: Dict) -> str:
    """Return the strong, mode-specific guidance block for the chosen mode."""
    meta = _mode_meta(intake)
    if not meta:
        return (
            "No specific presentation mode was selected. Infer the most likely "
            "mode from the intake and state which one you assumed."
        )
    return (
        f"SELECTED PRESENTATION MODE: {intake.get('mode')}\n"
        f"Primary presentation need: {meta['needs']}\n"
        f"Mode directives (follow these strongly):\n{meta['directives']}"
    )


def _resolve_provider(provider):
    """Accept a provider instance, a provider-name string, or None (env-driven)."""
    if provider is None:
        return get_provider()
    if isinstance(provider, str):
        return get_provider(preferred=provider)
    return provider


def _run(system_instruction: str, prompt: str, provider) -> str:
    """Run a single generation through the active provider."""
    return _resolve_provider(provider).generate(system_instruction, prompt).strip()


# ---------------------------------------------------------------------------
# Primary artifact: the creative brief
# ---------------------------------------------------------------------------

BRIEF_SYSTEM_PROMPT = (
    "You are a senior creative director and presentation strategist who has "
    "shaped decks for executives, investors, conferences, and major proposals. "
    "You help people figure out what their presentation truly needs BEFORE "
    "they start designing slides. You are opinionated, specific, and practical, "
    "and you adapt your recommendations strongly to the kind of deck being "
    "built. You write clear, well-structured briefs in Markdown.\n\n"
    + PRESENTATION_PHILOSOPHY
)


def generate_creative_brief(intake: Dict, provider=None) -> str:
    """
    Generate a detailed, mode-adaptive creative brief from the intake answers.

    Args:
        intake: Dictionary of intake answers (see format_intake for keys).
        provider: A provider instance, a provider-name string, or None
            (resolved from the environment). Demo Mode returns sample output.

    Returns:
        The creative brief as Markdown.
    """
    prov = _resolve_provider(provider)
    if prov.is_mock:
        return _demo_creative_brief(intake)

    prompt = f"""{_needs_reference()}

{_mode_directives(intake)}

A user completed an intake for a presentation they need to create. Here is what
they told you:

{format_intake(intake)}

Produce a detailed creative brief that is SPECIFIC to this deck and its mode —
no generic, interchangeable advice. Strongly adapt the structure, tone, pacing,
and visual direction to whether this deck is persuasive, informative,
technical, executive, speaker-supported, or a leave-behind. Infer sensible
defaults for anything unspecified and explicitly note assumptions you make.

Use this exact section structure with Markdown headings:

# Creative Brief: <a short, specific project name>

## Project Overview
What the presentation needs to accomplish, in a few sentences.

## Presentation Type
State the chosen presentation mode and the primary + any secondary needs from
the six categories, and briefly justify the choice. Explain how this mode
shapes the rest of the brief.

## Audience
Who the deck is for, their knowledge level, what they care about, and what they
need to understand or feel.

## Communication Goal
The core message in one or two sentences, plus the desired outcome (the
decision or action you want afterward).

## Recommended Structure
A logical outline with a clear beginning, middle, and ending, plus pacing and a
recommended slide count (respect the user's count if given, otherwise suggest a
range and justify it). Tailor the arc to the presentation mode.

## Slide-by-Slide Direction
A numbered slide list. For EVERY slide, include ALL of these labeled fields:
- **Slide title:** a point-making headline (not just a topic)
- **Slide purpose:** what this slide accomplishes in the flow
- **Main message:** the single takeaway the audience should leave with
- **Suggested layout:** e.g., Title, Title + Content, Two Content, Section
  Header, Full-bleed image, Big number, Comparison, Quote
- **Visual treatment:** the visual approach for the slide
- **Chart / diagram / image recommendation:** the specific visual to use (and
  what data or concept it should show)
- **Speaker notes (not on slide):** what should be SAID rather than shown — the
  detail that belongs in notes instead of on the slide

## Visual Style
Layout system, image use, icons, charts, diagrams, typography, color mood, and
overall visual tone. Honor every brand input provided (colors, fonts, logo,
tone); if brand details are missing, recommend a fitting palette and type
pairing and say so.

## Content Strategy
What to shorten, emphasize, visualize, move to speaker notes, or turn into
charts/diagrams. Be specific to this content.

## Design Principles
3-6 principles that keep THIS specific deck clear, modern, engaging, and easy
to follow.

## Presentation Quality Check
Evaluate the deck you just outlined against each question below. For each, give
a verdict (✅ strong / ⚠️ watch out) and a one-line, specific recommendation:
- **Too text-heavy?** Is any slide carrying too many words?
- **Supporting vs. replacing the speaker?** Do slides back the speaker rather
  than become the script? (For leave-behinds, judge stand-alone clarity instead.)
- **Clear at a glance?** Can each slide's point be grasped in a few seconds?
- **Logical flow?** Does the sequence build coherently from start to finish?
- **Complex ideas simplified visually?** Are hard concepts shown, not just told?
- **Clear ending / action?** Is the closing takeaway or call to action obvious?

Write for this exact presentation — avoid filler.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, prov)


# ---------------------------------------------------------------------------
# Downstream export artifacts
# ---------------------------------------------------------------------------

def _artifact_context(brief: str, intake: Dict) -> str:
    """Shared context block prepended to every downstream artifact prompt."""
    return f"""{_mode_directives(intake)}

Intake summary:
{format_intake(intake)}

Creative brief:
---
{brief}
---
"""


def generate_slide_outline(brief: str, intake: Dict, provider=None) -> str:
    """A clean, copy-ready slide outline derived from the brief."""
    prov = _resolve_provider(provider)
    if prov.is_mock:
        return _demo_slide_outline(intake)
    prompt = f"""{_artifact_context(brief, intake)}

Produce a clean, copy-ready SLIDE OUTLINE in Markdown. For each slide use:

### Slide N — <headline>
- **Purpose:** ...
- **Main message:** ...
- **On-slide content:** short bullets only (the visible slide text)
- **Visual:** the recommended visual element

Keep on-slide text tight (headlines and short bullets), consistent with the
mode directives and the principle that slides are visual support, not a script.
Start with a title slide and end with a closing/call-to-action slide.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, prov)


def generate_speaker_notes(brief: str, intake: Dict, provider=None) -> str:
    """Speaker-support notes: what to say, not what to read off the slide."""
    prov = _resolve_provider(provider)
    if prov.is_mock:
        return _demo_speaker_notes(intake)
    prompt = f"""{_artifact_context(brief, intake)}

Write SPEAKER-SUPPORT NOTES in Markdown, organized slide by slide
(### Slide N — <headline>). For each slide provide:
- The key point the speaker should land.
- A natural-language talking-track (2-5 sentences) the speaker can say.
- An optional transition line into the next slide.

The notes carry the detail so the slides can stay visual. Do NOT just repeat
the on-slide bullets — expand on them conversationally.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, prov)


def generate_design_direction(brief: str, intake: Dict, provider=None) -> str:
    """A focused visual/design direction document."""
    prov = _resolve_provider(provider)
    if prov.is_mock:
        return _demo_design_direction(intake)
    prompt = f"""{_artifact_context(brief, intake)}

Write a focused DESIGN DIRECTION document in Markdown covering:

## Color Palette
Suggest specific colors with hex codes (honor any brand colors provided) and
say where each is used.

## Typography
Recommend heading and body typefaces (honor brand fonts if provided, else
suggest a pairing with safe Office fallbacks) and sizing guidance.

## Layout System
Grid, margins, title placement, and a few reusable slide layout patterns.

## Imagery & Iconography
Photography style, illustration/icon style, and usage rules.

## Data Visualization Style
How charts and diagrams should look and behave.

## Do / Don't
A short list of design do's and don'ts for this deck.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, prov)


def generate_content_plan(brief: str, intake: Dict, provider=None) -> str:
    """A PowerPoint-ready content plan (exact text blocks per slide)."""
    prov = _resolve_provider(provider)
    if prov.is_mock:
        return _demo_content_plan(intake)
    prompt = f"""{_artifact_context(brief, intake)}

Produce a POWERPOINT-READY CONTENT PLAN in Markdown — the exact text someone
can paste into PowerPoint, slide by slide:

### Slide N
- **Layout:** (e.g., Title, Title + Content, Two Content, Section Header)
- **Title text:** the exact headline
- **Body text:** the exact bullets/short lines for the slide (visual support only)
- **Visual placeholder:** describe the chart/diagram/image to drop in
- **Speaker notes:** the exact text for the notes pane

Be concrete and final — this is the build-ready version, consistent with the
mode directives.
"""
    return _run(BRIEF_SYSTEM_PROMPT, prompt, prov)


VISUAL_PROMPTS_SYSTEM = (
    "You are an art director who writes precise prompts for AI image, icon, "
    "diagram, and layout generators. Your prompts are specific about subject, "
    "style, composition, color, and aspect ratio."
)


def generate_visual_prompts(brief: str, intake: Dict, provider=None) -> str:
    """AI prompts for generating visuals, icons, diagrams, or layouts."""
    prov = _resolve_provider(provider)
    if prov.is_mock:
        return _demo_visual_prompts(intake)
    prompt = f"""{_artifact_context(brief, intake)}

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
    return _run(VISUAL_PROMPTS_SYSTEM, prompt, prov)


# Map of export label -> generator function, for convenient UI wiring.
EXPORT_GENERATORS = {
    "Slide outline": generate_slide_outline,
    "Speaker-support notes": generate_speaker_notes,
    "Design direction": generate_design_direction,
    "PowerPoint-ready content plan": generate_content_plan,
    "AI visual prompts": generate_visual_prompts,
}


# ---------------------------------------------------------------------------
# Demo Mode builders — intake-aware sample output, no API key required.
# These prove the structure/format and let the whole pipeline (incl. PDF) run
# offline. They are clearly labeled as demo output.
# ---------------------------------------------------------------------------

def _demo_topic(intake: Dict) -> str:
    return (intake.get("topic") or intake.get("purpose") or "Your presentation").strip()


def _demo_audience(intake: Dict) -> str:
    return (intake.get("audience") or "your target audience").strip()


def _demo_mode(intake: Dict) -> str:
    return (intake.get("mode") or "Executive decision deck").strip()


def _demo_banner() -> str:
    return (
        "> 🟡 **Demo Mode** — this is illustrative sample output generated "
        "without an AI model. Add an `ANTHROPIC_API_KEY` (Claude) or "
        "`GEMINI_API_KEY` (Gemini) for live, fully tailored results.\n"
    )


def _demo_creative_brief(intake: Dict) -> str:
    topic = _demo_topic(intake)
    audience = _demo_audience(intake)
    mode = _demo_mode(intake)
    meta = _mode_meta(intake)
    primary_need = meta.get("needs", "Persuade or drive a decision")
    outcome = intake.get("desired_outcome") or "the decision or action you want next"
    count = intake.get("slide_count") or "10–12"
    moods = ", ".join(intake.get("visual_mood") or ["Executive", "Bold"])
    colors = intake.get("brand_colors") or "a confident primary + a single accent (none provided — suggested)"
    fonts = intake.get("brand_fonts") or "a clean geometric sans for headings + a readable sans for body (none provided — suggested)"

    return f"""{_demo_banner()}
# Creative Brief: {topic}

## Project Overview
This deck needs to {intake.get('purpose') or 'move ' + audience + ' to act'}.
Framed as a **{mode}**, its job is to land one clear message and drive
**{outcome}** — not to document everything you know.

## Presentation Type
- **Mode:** {mode}
- **Primary need:** {primary_need}
- **Secondary needs:** {', '.join([n for n in ['Communicate information visually', 'Structure and pace a message'] if n != primary_need][:1])}

This mode means: {meta.get('directives', 'adapt structure and tone to the audience and goal.')}

## Audience
**{audience}.** Knowledge level: {intake.get('knowledge_level') or 'some familiarity'}.
They are time-constrained and decision-oriented — they need the point fast and
the evidence on demand.

## Communication Goal
**Core message:** A single, defensible claim that earns {outcome}.
**Desired outcome:** {outcome}.

## Recommended Structure
A clear beginning → middle → end across **{count} slides**:
1. **Open** — set the stakes and state the ask.
2. **Build** — the case in 3 moves (problem → solution → proof).
3. **Close** — the decision and the specific next step.

## Slide-by-Slide Direction
{_demo_slide_block(intake)}

## Visual Style
- **Mood:** {moods}.
- **Color:** {colors}.
- **Typography:** {fonts}.
- One idea per slide, generous whitespace, big numbers, and charts whose titles
  state the takeaway. Honor logo placement: {intake.get('brand_logo') or 'top-left, with clear space.'}

## Content Strategy
- **Shorten:** any slide over ~20 words — move the detail to speaker notes.
- **Visualize:** turn comparisons into charts and processes into diagrams.
- **Emphasize:** the ask and the single proof point that de-risks it.
- **Move to notes:** caveats, methodology, and backup numbers (appendix).

## Design Principles
1. One message per slide; the headline states the point.
2. Slides support the speaker — they are not the script.
3. Show, don't tell: a chart beats a paragraph.
4. Consistent grid, type scale, and accent color throughout.
5. End every section with the takeaway.

## Presentation Quality Check
- **Too text-heavy?** ✅ strong — drafted at headline + ≤4 bullets per slide. Keep it there.
- **Supporting vs. replacing the speaker?** ✅ strong — detail lives in the notes.
- **Clear at a glance?** ✅ strong — each headline is a complete point.
- **Logical flow?** ✅ strong — stakes → case → decision.
- **Complex ideas simplified visually?** ⚠️ watch out — confirm each data slide has a real chart, not a table dump.
- **Clear ending / action?** ✅ strong — closes on **{outcome}**.
"""


def _demo_slide_block(intake: Dict) -> str:
    topic = _demo_topic(intake)
    outcome = intake.get("desired_outcome") or "the next step"
    slides = [
        ("Title — the one-line promise",
         "Set the frame and state the ask in a sentence.",
         f"What {topic} delivers, and what you're asking for.",
         "Title", "Full-bleed image + logo + one-line headline",
         "Cover image; no bullets."),
        ("The stakes: why now",
         "Make the problem urgent and relatable.",
         "This problem is costing the audience something today.",
         "Big number", "One large statistic with a short caption",
         "A single arresting metric."),
        ("Our answer in one picture",
         "Show the solution at a glance.",
         "Here is the solution, simply.",
         "Title + Content", "Simple concept diagram (3 boxes + arrows)",
         "A schematic, not text."),
        ("Proof it works",
         "De-risk the claim with evidence.",
         "The results back up the claim.",
         "Two Content", "Trend chart whose title states the result",
         "One chart with an insight headline."),
        (f"The ask: {outcome}",
         "Make the decision and next step unmistakable.",
         f"Here's exactly what we're asking for: {outcome}.",
         "Section Header", "Bold statement slide + single CTA",
         "The specific ask and timeline."),
    ]
    out = []
    for i, (title, purpose, message, layout, visual, notes) in enumerate(slides, 1):
        out.append(
            f"{i}. **Slide title:** {title}\n"
            f"   - **Slide purpose:** {purpose}\n"
            f"   - **Main message:** {message}\n"
            f"   - **Suggested layout:** {layout}\n"
            f"   - **Visual treatment:** {visual}\n"
            f"   - **Chart / diagram / image recommendation:** {visual}\n"
            f"   - **Speaker notes (not on slide):** {notes}"
        )
    return "\n".join(out)


def _demo_slide_outline(intake: Dict) -> str:
    topic = _demo_topic(intake)
    outcome = intake.get("desired_outcome") or "the next step"
    rows = [
        ("Title", "Set the frame and ask", f"{topic} — the one-line promise", "Full-bleed cover + logo"),
        ("Why now", "Create urgency", "One big stakes number", "Big-number layout"),
        ("Our answer", "Show the solution", "The solution in one diagram", "3-box concept diagram"),
        ("Proof", "De-risk the claim", "Results back the claim", "Trend chart, insight title"),
        ("The ask", "Drive the decision", f"Exactly: {outcome}", "Bold CTA slide"),
    ]
    out = [_demo_banner(), "# Slide Outline\n"]
    for i, (head, purpose, msg, visual) in enumerate(rows, 1):
        out.append(
            f"### Slide {i} — {head}\n"
            f"- **Purpose:** {purpose}\n"
            f"- **Main message:** {msg}\n"
            f"- **On-slide content:** {head} · one short line\n"
            f"- **Visual:** {visual}\n"
        )
    return "\n".join(out)


def _demo_speaker_notes(intake: Dict) -> str:
    topic = _demo_topic(intake)
    outcome = intake.get("desired_outcome") or "the next step"
    return f"""{_demo_banner()}
# Speaker-Support Notes

### Slide 1 — Title
- **Key point:** Frame the whole talk in one sentence.
- **Talking track:** "In the next few minutes I'll show you {topic.lower()} —
  and what I'm asking you to decide by the end."
- **Transition:** "First, why this matters right now."

### Slide 2 — Why now
- **Key point:** Make the problem urgent.
- **Talking track:** "This number is the cost of the status quo. It's growing,
  and waiting makes it worse."
- **Transition:** "Here's our answer."

### Slide 3 — Our answer
- **Key point:** Explain the solution simply.
- **Talking track:** "It works in three steps — input, transformation, result.
  That's the whole idea."
- **Transition:** "And it's not theoretical."

### Slide 4 — Proof
- **Key point:** Evidence de-risks the decision.
- **Talking track:** "Here's what happened when we ran it: the trend speaks for
  itself."
- **Transition:** "So here's what I'm asking."

### Slide 5 — The ask
- **Key point:** Make the decision easy.
- **Talking track:** "Concretely, we're asking for {outcome}. Here's the
  timeline and what it unlocks."
"""


def _demo_design_direction(intake: Dict) -> str:
    colors = intake.get("brand_colors") or "#1A2A4F primary, #FF6B35 accent, #F8FAFC background"
    fonts = intake.get("brand_fonts") or "Headings: Space Grotesk; Body: Inter (fallbacks: Calibri/Arial)"
    return f"""{_demo_banner()}
# Design Direction

## Color Palette
{colors}
- Primary: titles, key shapes. Accent: a single highlight per slide. Background: light, generous whitespace.

## Typography
{fonts}
- Titles ~36–44pt, body ~18–24pt, captions ~12–14pt. Tight, consistent scale.

## Layout System
- 12-column grid, wide margins, title locked top-left, logo with clear space.
- Reusable patterns: Big Number, Two-Content compare, Full-bleed image, Section Header.

## Imagery & Iconography
- Photography: authentic, human, well-lit; avoid generic stock.
- Icons: single-weight line icons in the primary color.

## Data Visualization Style
- One idea per chart; the **title states the insight**. Accent color highlights the key series; everything else muted.

## Do / Don't
- ✅ Headlines that make a point · ✅ one chart per slide · ✅ lots of whitespace.
- ❌ Paragraphs on slides · ❌ 3-D charts · ❌ more than two type sizes per slide.
"""


def _demo_content_plan(intake: Dict) -> str:
    topic = _demo_topic(intake)
    outcome = intake.get("desired_outcome") or "the next step"
    return f"""{_demo_banner()}
# PowerPoint-Ready Content Plan

### Slide 1
- **Layout:** Title
- **Title text:** {topic}
- **Body text:** (none — cover slide)
- **Visual placeholder:** Full-bleed hero image + logo top-left
- **Speaker notes:** Frame the talk and preview the ask.

### Slide 2
- **Layout:** Big Number
- **Title text:** The cost of waiting
- **Body text:** One large metric · one short caption
- **Visual placeholder:** Oversized statistic
- **Speaker notes:** Make the problem urgent and concrete.

### Slide 3
- **Layout:** Title + Content
- **Title text:** Our answer, in one picture
- **Body text:** Input → Transformation → Result
- **Visual placeholder:** 3-box concept diagram with arrows
- **Speaker notes:** Explain the solution simply.

### Slide 4
- **Layout:** Two Content
- **Title text:** It works — here's the proof
- **Body text:** Before vs. after · one supporting stat
- **Visual placeholder:** Trend chart with an insight title
- **Speaker notes:** Evidence de-risks the decision.

### Slide 5
- **Layout:** Section Header
- **Title text:** The ask: {outcome}
- **Body text:** What we're asking · timeline · what it unlocks
- **Visual placeholder:** Bold CTA panel in the accent color
- **Speaker notes:** Make the decision easy and specific.
"""


def _demo_visual_prompts(intake: Dict) -> str:
    topic = _demo_topic(intake)
    colors = intake.get("brand_colors") or "deep navy and a warm orange accent"
    return f"""{_demo_banner()}
# AI Visual Prompts

## Cover / Hero Image Prompts
```
Editorial hero image for "{topic}", cinematic lighting, {colors},
clean negative space on the left for a title, 16:9. Negative prompt: text, watermark, clutter.
```

## Section Divider Prompts
```
Minimal section divider, large numeral, {colors}, lots of whitespace, 16:9.
```

## Icon Set Prompts
```
Set of 6 single-weight line icons (problem, solution, growth, team, money, timeline),
consistent stroke, primary color, transparent background.
```

## Diagram / Schematic Prompts
```
Clean 3-step concept diagram: input -> transformation -> result, rounded boxes + arrows,
{colors}, flat design, 16:9.
```

## Background / Texture Prompts
```
Subtle abstract gradient background, {colors}, very low contrast so text stays legible, 16:9.
```
"""


# ---------------------------------------------------------------------------
# Minimal CLI for quick testing without the Streamlit UI
# ---------------------------------------------------------------------------

def _cli() -> None:
    import sys

    use_sample = "--sample" in sys.argv
    prov = get_provider()
    print(f"[{APP_NAME}] provider: {prov.label}"
          f"{' (Demo Mode — ' + prov.reason + ')' if prov.is_mock else ''}\n")

    if "--check" in sys.argv:
        ok, msg = providers.health_check(prov)  # redacted, never prints the key
        print(("OK: " if ok else "FAIL: ") + msg)
        sys.exit(0 if ok else 1)

    if use_sample:
        intake = dict(SAMPLE_INTAKE)
        print(f"Using sample intake: {intake['topic']}\n")
    else:
        print("Quick intake (press Enter to skip)\n")
        intake = {
            "topic": input("What is the presentation about? "),
            "purpose": input("What is it for / what must it accomplish? "),
            "audience": input("Who will see it? "),
            "mode": input(f"Mode {PRESENTATION_MODE_NAMES}: "),
            "desired_outcome": input("What decision or action should follow? "),
            "occasion": input("Occasion (pitch, conference, training...)? "),
            "slide_count": input("Approximate number of slides? "),
        }

    print("\nGenerating creative brief...\n")
    print(generate_creative_brief(intake, prov))


if __name__ == "__main__":
    _cli()
