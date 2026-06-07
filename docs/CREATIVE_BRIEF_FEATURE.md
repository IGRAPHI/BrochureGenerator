# Presentation Creative Brief 📊

A creative director and presentation strategist for your deck. Instead of
jumping straight to slides, it runs a short intake to understand what the
presentation needs to accomplish, then generates a detailed creative brief and
a set of build-ready artifacts.

## Why it exists

The strongest PowerPoint decks treat slides as **visual support for a message,
not a script to be read aloud**. When a slide carries the full burden of the
message, attention shifts away from the presenter and impact drops. This tool
bakes that philosophy into every output: one idea per slide, point-making
headlines, visuals over paragraphs, and detail pushed into speaker notes.

## The six presentation needs it recognizes

1. **Communicate information visually** — turn data/ideas into something the
   audience grasps quickly.
2. **Structure and pace a message** — use slides as the spine of a logical
   sequence.
3. **Support a speaker** — reinforce spoken delivery without becoming a script.
4. **Persuade or drive a decision** — build a case for a pitch, proposal,
   donor meeting, investment request, or leadership decision.
5. **Simplify complexity** — break down technical/policy/financial/scientific
   topics with diagrams, charts, and hierarchy.
6. **Create a shareable record** — decks that live on as leave-behinds and
   reference documents.

A brief can map to a single need or a combination.

## How it works

1. **Intake.** Answer a short set of smart questions: what the presentation is
   for, who the audience is, live vs. document, the decision you want
   afterward, how much the audience already knows, the nature of the content,
   the desired feel, brand guidelines, slide count, and the occasion. Anything
   you skip is filled in with sensible defaults (and the assumptions are noted).

2. **Creative brief.** The strategist produces a brief with these sections:
   - **Project Overview**
   - **Presentation Type** (primary + secondary needs)
   - **Audience**
   - **Communication Goal**
   - **Recommended Structure** (beginning / middle / end + pacing)
   - **Slide-by-Slide Direction** (title, purpose, content notes, visual treatment)
   - **Visual Style**
   - **Content Strategy**
   - **Design Principles**

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

Use the sidebar to switch between **Presentation Creative Brief** (default) and
**Company Brochure Generator**. A Google Gemini API key is required — set
`GENAI_API_KEY` in a `.env` file or paste it into the sidebar.

## Code map

| File | Responsibility |
| --- | --- |
| `creative_brief.py` | Core engine: presentation needs, intake formatting, and all generation functions (no Streamlit). |
| `views/creative_brief_page.py` | Streamlit UI for the intake form, brief display, and exports. |
| `views/brochure_page.py` | Streamlit UI for the brochure generator. |
| `app.py` | Multipage entry point (`st.navigation`) and shared styling. |

The engine reuses the Gemini configuration and `markdown_to_pdf` helper from
`main.py`, so both tools share one AI/PDF setup.

## Quick CLI test

You can exercise the engine without the UI:

```bash
python creative_brief.py
```

This runs a minimal intake in the terminal and prints the generated brief.
