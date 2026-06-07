"""
Markdown -> PDF export.

A self-contained, dependency-light PDF renderer (ReportLab) with no AI-provider
dependencies, so it can be shared by every tool in the app and used in Demo
Mode without any API key. Renders a practical subset of Markdown well enough to
produce clean, professional documents: headings, bold/italic/inline-code,
links, bullet and numbered lists, block quotes, horizontal rules, fenced code
blocks, and pipe tables.
"""

from __future__ import annotations

import re
from io import BytesIO

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Preformatted,
        Table,
        TableStyle,
        HRFlowable,
    )
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor

    PDF_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only without reportlab
    PDF_AVAILABLE = False


# ---------------------------------------------------------------------------
# Inline markdown -> ReportLab mini-HTML
# ---------------------------------------------------------------------------

_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_BOLD_US_RE = re.compile(r"__([^_]+)__")
_ITALIC_RE = re.compile(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)")
_CODE_RE = re.compile(r"`([^`]+)`")


def _inline(text: str) -> str:
    """Convert inline markdown to ReportLab markup, escaping XML specials first."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = _LINK_RE.sub(r"\1", text)  # keep link text, drop the URL
    text = _BOLD_RE.sub(r"<b>\1</b>", text)
    text = _BOLD_US_RE.sub(r"<b>\1</b>", text)
    text = _ITALIC_RE.sub(r"<i>\1</i>", text)
    text = _CODE_RE.sub(r'<font face="Courier">\1</font>', text)
    return text


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "CB_Title", parent=base["Heading1"], fontSize=23,
            textColor=HexColor("#1A2A4F"), spaceAfter=16, spaceBefore=6, leading=27,
        ),
        "h1": ParagraphStyle(
            "CB_H1", parent=base["Heading1"], fontSize=16,
            textColor=HexColor("#1A2A4F"), spaceAfter=8, spaceBefore=16, leading=20,
        ),
        "h2": ParagraphStyle(
            "CB_H2", parent=base["Heading2"], fontSize=13,
            textColor=HexColor("#374151"), spaceAfter=6, spaceBefore=10, leading=17,
        ),
        "h3": ParagraphStyle(
            "CB_H3", parent=base["Heading3"], fontSize=11.5,
            textColor=HexColor("#4B5563"), spaceAfter=5, spaceBefore=8, leading=15,
        ),
        "body": ParagraphStyle(
            "CB_Body", parent=base["BodyText"], fontSize=10.5,
            alignment=TA_JUSTIFY, spaceAfter=7, leading=15,
        ),
        "bullet": ParagraphStyle(
            "CB_Bullet", parent=base["BodyText"], fontSize=10.5,
            alignment=TA_LEFT, leftIndent=16, spaceAfter=3, leading=14,
            bulletIndent=4,
        ),
        "quote": ParagraphStyle(
            "CB_Quote", parent=base["BodyText"], fontSize=10.5,
            leftIndent=16, textColor=HexColor("#6B7280"), spaceAfter=7,
            leading=15, borderColor=HexColor("#D1D5DB"),
        ),
        "code": ParagraphStyle(
            "CB_Code", parent=base["Code"], fontSize=8.5,
            textColor=HexColor("#111827"), backColor=HexColor("#F3F4F6"),
            leading=11, leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=8,
            borderPadding=6,
        ),
    }


def _is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.count("|") >= 2


def _is_table_divider(line: str) -> bool:
    s = line.strip().strip("|")
    cells = [c.strip() for c in s.split("|")]
    return bool(cells) and all(set(c) <= set("-: ") and "-" in c for c in cells)


def _split_row(line: str):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def markdown_to_pdf(markdown_text: str) -> BytesIO:
    """
    Convert Markdown text to a clean, professional PDF.

    Args:
        markdown_text: Markdown-formatted text.

    Returns:
        BytesIO positioned at 0, containing the PDF bytes.

    Raises:
        ImportError: If reportlab is not installed.
    """
    if not PDF_AVAILABLE:
        raise ImportError("PDF libraries not installed. Run: pip install reportlab markdown2")

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, rightMargin=64, leftMargin=64, topMargin=64, bottomMargin=64,
        title="Presentation Strategy Studio",
    )
    s = _styles()
    story = []

    lines = markdown_text.split("\n")
    i = 0
    n = len(lines)

    while i < n:
        raw = lines[i]
        line = raw.strip()

        # Fenced code block
        if line.startswith("```"):
            i += 1
            code_lines = []
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            code = "\n".join(code_lines) if code_lines else " "
            story.append(Preformatted(code, s["code"]))
            continue

        # Pipe table
        if _is_table_row(raw) and i + 1 < n and _is_table_divider(lines[i + 1]):
            header = _split_row(raw)
            i += 2  # skip header + divider
            rows = []
            while i < n and _is_table_row(lines[i]):
                rows.append(_split_row(lines[i]))
                i += 1
            data = [[Paragraph(_inline(c), s["body"]) for c in header]]
            for r in rows:
                # pad/truncate to header width
                r = (r + [""] * len(header))[: len(header)]
                data.append([Paragraph(_inline(c), s["body"]) for c in r])
            table = Table(data, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1A2A4F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D1D5DB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#F3F4F6")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(Spacer(1, 0.05 * inch))
            story.append(table)
            story.append(Spacer(1, 0.1 * inch))
            continue

        if not line:
            story.append(Spacer(1, 0.06 * inch))
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"(\*\s*){3,}|(-\s*){3,}|(_\s*){3,}", line):
            story.append(Spacer(1, 0.04 * inch))
            story.append(HRFlowable(width="100%", thickness=0.6, color=HexColor("#D1D5DB")))
            story.append(Spacer(1, 0.06 * inch))
            i += 1
            continue

        # Headings
        if line.startswith("#### "):
            story.append(Paragraph(_inline(line[5:].strip()), s["h3"]))
        elif line.startswith("### "):
            story.append(Paragraph(_inline(line[4:].strip()), s["h3"]))
        elif line.startswith("## "):
            story.append(Paragraph(_inline(line[3:].strip()), s["h1"]))
        elif line.startswith("# "):
            story.append(Paragraph(_inline(line[2:].strip()), s["title"]))
            story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#1A2A4F")))
            story.append(Spacer(1, 0.08 * inch))

        # Block quote
        elif line.startswith(">"):
            story.append(Paragraph(_inline(line.lstrip(">").strip()), s["quote"]))

        # Numbered list
        elif re.match(r"^\d+\.\s+", line):
            num, _, rest = line.partition(". ")
            story.append(Paragraph(f"{num}. {_inline(rest.strip())}", s["bullet"]))

        # Bullet list (supports a couple of indent levels)
        elif re.match(r"^[\*\-\+]\s+", line) or re.match(r"^\s+[\*\-\+]\s+", raw):
            indent = len(raw) - len(raw.lstrip())
            text = re.sub(r"^[\*\-\+]\s+", "", line)
            marker = "◦" if indent >= 2 else "•"
            para = ParagraphStyle(
                f"bl{indent}", parent=s["bullet"], leftIndent=16 + min(indent, 6) * 4
            )
            story.append(Paragraph(f"{marker} {_inline(text)}", para))

        # Plain paragraph
        else:
            story.append(Paragraph(_inline(line), s["body"]))

        i += 1

    if not story:
        story.append(Paragraph(" ", s["body"]))

    doc.build(story)
    buf.seek(0)
    return buf
