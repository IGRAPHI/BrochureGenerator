"""
Main entry point for AI-powered company brochure generation.
CLI interface for generating brochures from company websites.
Also provides core functions used by the Streamlit app.
"""

import os
import sys
from dotenv import load_dotenv

# PDF export is shared with the rest of the app and has no AI-provider deps.
from pdf_export import markdown_to_pdf, PDF_AVAILABLE  # noqa: F401 (re-exported)

# Load environment variables
load_dotenv()

# System prompt for brochure generation (shared constant)
SYSTEM_PROMPT = """You are a professional marketing copywriter that creates detailed,
engaging company brochures based on website content. Your brochures are well-structured,
informative, and highlight the company's key strengths and offerings."""


def _genai():
    """Lazily import google-generativeai so the rest of the app runs without it."""
    try:
        import google.generativeai as genai
    except ImportError as e:  # pragma: no cover
        raise RuntimeError(
            "google-generativeai is not installed. Install it to use the "
            "Gemini-powered Company Brochure Generator."
        ) from e
    return genai


def get_api_key() -> str:
    """
    Get the Gemini API key from environment variables.

    Accepts the new GEMINI_API_KEY and the legacy GENAI_API_KEY.

    Returns:
        str: API key if found, None otherwise
    """
    return os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY")


def configure_genai(api_key: str = None) -> None:
    """
    Configure Google Gemini AI with API key.

    Args:
        api_key (str, optional): API key. If None, gets from environment.
    """
    if api_key is None:
        api_key = get_api_key()

    if not api_key:
        raise ValueError("Gemini API key not found. Please provide an API key.")

    _genai().configure(api_key=api_key)


def get_model(system_instruction: str = SYSTEM_PROMPT):
    """
    Get configured Gemini model for brochure generation.

    Args:
        system_instruction (str): System prompt for the model

    Returns:
        GenerativeModel: Configured Gemini model
    """
    return _genai().GenerativeModel(
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

    # Generate brochure (imported lazily so the studio runs without google deps)
    from utils import create_brochure

    brochure = create_brochure(website_url, model)

    return brochure


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
