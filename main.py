"""
Main entry point for AI-powered company brochure generation.
CLI interface for generating brochures from company websites.
Also provides core functions used by the Streamlit app.
"""

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from utils import create_brochure
from io import BytesIO
import re

# Load environment variables
load_dotenv()

# Gemini model used across the project (shared constant).
MODEL_NAME = "gemini-2.0-flash-exp"

# System prompt for brochure generation (shared constant)
SYSTEM_PROMPT = """You are a professional marketing copywriter that creates detailed,
engaging company brochures based on website content. Your brochures are well-structured,
informative, and highlight the company's key strengths and offerings."""

# Check if ReportLab is available
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
    from reportlab.lib.colors import HexColor
    import markdown2

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def get_api_key() -> str:
    """
    Get API key from environment variables.

    Returns:
        str: API key if found, None otherwise
    """
    return os.getenv("GENAI_API_KEY")


def configure_genai(api_key: str = None) -> None:
    """
    Configure Google Gemini AI with API key.

    Args:
        api_key (str, optional): API key. If None, gets from environment.
    """
    if api_key is None:
        api_key = get_api_key()

    if not api_key:
        raise ValueError("GENAI_API_KEY not found. Please provide API key.")

    genai.configure(api_key=api_key)


def get_model(system_instruction: str = SYSTEM_PROMPT):
    """
    Get configured Gemini model for brochure generation.

    Args:
        system_instruction (str): System prompt for the model

    Returns:
        GenerativeModel: Configured Gemini model
    """
    return genai.GenerativeModel(
        model_name=MODEL_NAME, system_instruction=system_instruction
    )


def normalize_url(url: str) -> str:
    """
    Ensure URL has proper protocol.

    Args:
        url (str): URL to normalize

    Returns:
        str: URL with protocol
    """
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def generate_brochure(website_url: str, api_key: str = None) -> str:
    """
    Generate company brochure from website URL.
    This is the main function used by both CLI and Streamlit app.

    Args:
        website_url (str): Company website URL
        api_key (str, optional): Google Gemini API key

    Returns:
        str: Generated brochure in markdown format

    Raises:
        ValueError: If API key not found
        Exception: If brochure generation fails
    """
    # Configure API
    configure_genai(api_key)

    # Normalize URL
    website_url = normalize_url(website_url)

    # Get model
    model = get_model()

    # Generate brochure
    brochure = create_brochure(website_url, model)

    return brochure


def markdown_to_pdf(markdown_text: str) -> BytesIO:
    """
    Convert markdown text to PDF using ReportLab.

    Args:
        markdown_text (str): Markdown formatted text

    Returns:
        BytesIO: PDF file as bytes

    Raises:
        ImportError: If reportlab or markdown2 is not installed
        Exception: If PDF generation fails
    """
    if not PDF_AVAILABLE:
        raise ImportError(
            "PDF libraries not installed. Run: pip install reportlab markdown2"
        )

    # Create PDF buffer
    pdf_buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    # Container for the 'Flowable' objects
    story = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=HexColor("#2c3e50"),
        spaceAfter=30,
        spaceBefore=20,
        alignment=TA_LEFT,
    )

    heading1_style = ParagraphStyle(
        "CustomHeading1",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=HexColor("#34495e"),
        spaceAfter=12,
        spaceBefore=12,
        borderColor=HexColor("#95a5a6"),
        borderWidth=1,
        borderPadding=5,
    )

    heading2_style = ParagraphStyle(
        "CustomHeading2",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=HexColor("#555555"),
        spaceAfter=10,
        spaceBefore=10,
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16,
    )

    # Process markdown line by line
    lines = markdown_text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            story.append(Spacer(1, 0.1 * inch))
            i += 1
            continue

        # Handle headers
        if line.startswith("# "):
            text = line[2:].strip()
            # Remove markdown links
            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
            story.append(Paragraph(text, title_style))
            story.append(Spacer(1, 0.2 * inch))

        elif line.startswith("## "):
            text = line[3:].strip()
            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
            story.append(Paragraph(text, heading1_style))
            story.append(Spacer(1, 0.15 * inch))

        elif line.startswith("### "):
            text = line[4:].strip()
            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
            story.append(Paragraph(text, heading2_style))
            story.append(Spacer(1, 0.1 * inch))

        # Handle bullet points
        elif line.startswith("* ") or line.startswith("- "):
            text = line[2:].strip()
            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
            # Make bold text
            text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
            text = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', text)
            story.append(Paragraph(f"• {text}", body_style))

        # Handle regular paragraphs
        else:
            text = line
            # Remove markdown links but keep text
            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
            # Make bold text
            text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
            # Make italic text
            text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
            # Handle inline code
            text = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', text)

            if text:
                story.append(Paragraph(text, body_style))
                story.append(Spacer(1, 0.05 * inch))

        i += 1

    # Build PDF
    try:
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")


def main():
    """Main CLI function for brochure generation."""

    # Get API key from environment
    api_key = get_api_key()
    if not api_key:
        print("Error: GENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key:")
        print("GENAI_API_KEY=your_api_key_here")
        sys.exit(1)

    # Get website URL from command line or user input
    if len(sys.argv) > 1:
        website_url = sys.argv[1]
    else:
        website_url = input("Enter company website URL: ").strip()

    if not website_url:
        print("Error: No URL provided")
        sys.exit(1)

    try:
        # Generate brochure
        print(f"\n{'=' * 60}")
        print(f"Generating brochure for: {website_url}")
        print(f"{'=' * 60}\n")

        brochure = generate_brochure(website_url, api_key)

        # Print brochure
        print("\n" + "=" * 60)
        print("GENERATED BROCHURE")
        print("=" * 60 + "\n")
        print(brochure)

        # Optionally save to file
        save = input("\n\nSave brochure to file? (y/n): ").strip().lower()
        if save == "y":
            filename = (
                input("Enter filename (default: brochure.md): ").strip()
                or "brochure.md"
            )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(brochure)
            print(f"✓ Brochure saved to {filename}")

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
