# Presentation Strategy Studio 📊

A creative director and presentation strategist for your deck. Instead of
jumping straight to slides, it runs a short intake to understand what the
presentation needs to accomplish — and what *kind* of deck it is — then
generates a detailed, mode-adaptive creative brief and a set of build-ready
artifacts.

## Why it exists

The strongest PowerPoint decks treat slides as **visual support for a message,
not a script to be read aloud**. When a slide carries the full burden of the
message, attention shifts away from the presenter and impact drops. This tool
bakes that philosophy into every output: one idea per slide, point-making
headlines, visuals over paragraphs, and detail pushed into speaker notes.

## AI providers (Claude-first)

Generation runs through a pluggable provider layer (`providers.py`):

- **Claude** — the default and preferred provider (`ANTHROPIC_API_KEY`, default
  model `claude-opus-4-8`, uses streaming + adaptive thinking).
- **Gemini** — optional alternative (`GEMINI_API_KEY`).
- **Demo Mode** — no key required; produces clearly-labeled, intake-aware sample
  output so the whole flow (including PDF export) works offline.

Pick the provider in the sidebar or via `AI_PROVIDER` / keys in `.env`. See the
main README for the full configuration table.

## Presentation modes

The intake includes a **presentation mode** that strongly shapes structure,
tone, pacing, and visual direction so the brief is never generic:

| Mode | Maps to need |
| --- | --- |
| Live speaker support | Support a speaker |
| Executive decision deck | Persuade or drive a decision |
| Donor / proposal deck | Persuade or drive a decision |
| Training or workshop deck | Simplify complexity |
| Conference presentation | Communicate information visually |
| Leave-behind / shareable document | Create a shareable record |
| Technical explanation deck | Simplify complexity |
| Visual report summary | Communicate information visually |

These sit on top of the six core presentation needs (communicate visually,
structure & pace, support a speaker, persuade/decide, simplify complexity,
create a shareable record). A brief can map to a single need or a combination.

## How it works

1. **Intake.** Answer a short set of smart questions: what it's for, audience,
   presentation mode, live vs. document, the decision you want afterward, how
   much the audience knows, content nature, desired feel, slide count, occasion,
   and a **brand input** block (colors, fonts, logo notes, tone of voice, and
   any pasted guidelines). Anything you skip is filled with sensible defaults
   (and the assumptions are noted). A **Load sample** button fills the form with
   a worked example so you can try it instantly.

2. **Creative brief.** Produced with these sections:
   - Project Overview
   - Presentation Type (mode + primary/secondary needs)
   - Audience
   - Communication Goal
   - Recommended Structure (beginning / middle / end + pacing)
   - **Slide-by-Slide Direction** — for every slide: title, purpose, main
     message, suggested layout, visual treatment, chart/diagram/image
     recommendation, and what belongs in speaker notes (not on the slide)
   - Visual Style
   - Content Strategy
   - Design Principles
   - **Presentation Quality Check** — verdicts + fixes for: too text-heavy?
     supporting vs. replacing the speaker? clear at a glance? logical flow?
     complex ideas simplified visually? clear ending/action?

3. **Additional outputs.** Generate any of these on demand from the brief:
   - **Slide outline** — clean, copy-ready slide list.
   - **Speaker-support notes** — what to *say*, not what to read.
   - **Design direction** — palette, typography, layout, imagery, chart style.
   - **PowerPoint-ready content plan** — exact title/body/notes text per slide.
   - **AI visual prompts** — ready-to-paste prompts for images, icons, diagrams.

Every output can be downloaded as Markdown or PDF.

## Running it

```bash
streamlit run app.py
```

Use the sidebar to switch between **Presentation Strategy Studio** (default) and
**Company Brochure Generator**, and to choose the AI provider / paste a key.

## Code map

| File | Responsibility |
| --- | --- |
| `creative_brief.py` | Core engine: needs, modes, intake formatting, all generators, and Demo-Mode builders (no Streamlit). |
| `providers.py` | Pluggable AI providers — Claude (default), Gemini (optional), Demo/Mock. |
| `pdf_export.py` | Shared Markdown→PDF renderer (headings, lists, tables, code, quotes). No AI deps. |
| `views/creative_brief_page.py` | Streamlit UI: provider selector, intake form, brief display, exports. |
| `views/brochure_page.py` | Streamlit UI for the brochure generator. |
| `app.py` | Multipage entry point (`st.navigation`) and shared styling. |

## Quick CLI test

```bash
python creative_brief.py            # interactive intake
python creative_brief.py --sample   # use the built-in sample intake
```

With no API key set, this prints a Demo-Mode brief; with `ANTHROPIC_API_KEY`
(or `GEMINI_API_KEY` + `AI_PROVIDER=gemini`) it generates live.
