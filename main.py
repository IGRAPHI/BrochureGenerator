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
import markdown

# Load environment variables
load_dotenv()

# System prompt for brochure generation (shared constant)
SYSTEM_PROMPT = """You are a professional marketing copywriter that creates detailed, 
engaging company brochures based on website content. Your brochures are well-structured, 
informative, and highlight the company's key strengths and offerings."""

# Check if xhtml2pdf is available
try:
    from xhtml2pdf import pisa
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
        model_name="gemini-2.0-flash-exp", system_instruction=system_instruction
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
    Convert markdown text to PDF.

    Args:
        markdown_text (str): Markdown formatted text

    Returns:
        BytesIO: PDF file as bytes

    Raises:
        ImportError: If xhtml2pdf is not installed
        Exception: If PDF generation fails
    """
    if not PDF_AVAILABLE:
        raise ImportError("xhtml2pdf is not installed. Run: pip install xhtml2pdf")

    # Convert markdown to HTML
    html = markdown.markdown(
        markdown_text, extensions=["extra", "codehilite", "tables", "toc"]
    )

    # Add CSS styling for better PDF appearance
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: Arial, Helvetica, sans-serif;
                line-height: 1.6;
                color: #333;
                font-size: 11pt;
            }}
            h1 {{
                color: #2c3e50;
                font-size: 24pt;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                margin-top: 20px;
            }}
            h2 {{
                color: #34495e;
                font-size: 18pt;
                margin-top: 18px;
                border-bottom: 2px solid #95a5a6;
                padding-bottom: 5px;
            }}
            h3 {{
                color: #555;
                font-size: 14pt;
                margin-top: 15px;
            }}
            p {{
                margin: 10px 0;
                text-align: justify;
            }}
            ul, ol {{
                margin: 10px 0;
                padding-left: 30px;
            }}
            li {{
                margin: 5px 0;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                border-left: 4px solid #3498db;
                overflow-x: auto;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin: 15px 0;
                color: #555;
                font-style: italic;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #3498db;
                color: white;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """

    # Convert HTML to PDF
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(styled_html.encode("utf-8")), dest=pdf_buffer)

    if pisa_status.err:
        raise Exception("PDF generation failed")

    pdf_buffer.seek(0)
    return pdf_buffer


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
