"""
Main entry point for AI-powered company brochure generation.
CLI interface for generating brochures from company websites.
"""

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from utils import create_brochure

# Load environment variables
load_dotenv()


def main():
    """Main CLI function for brochure generation."""

    # Get API key from environment
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        print("Error: GENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key:")
        print("GENAI_API_KEY=your_api_key_here")
        sys.exit(1)

    # Configure Gemini
    genai.configure(api_key=api_key)

    # System prompt for brochure generation
    system_prompt = """You are a professional marketing copywriter that creates detailed, 
    engaging company brochures based on website content. Your brochures are well-structured, 
    informative, and highlight the company's key strengths and offerings."""

    # Initialize model for brochure generation
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp", system_instruction=system_prompt
    )

    # Get website URL from command line or use default
    if len(sys.argv) > 1:
        website_url = sys.argv[1]
    else:
        website_url = input("Enter company website URL: ").strip()

    if not website_url:
        print("Error: No URL provided")
        sys.exit(1)

    # Ensure URL has protocol
    if not website_url.startswith(("http://", "https://")):
        website_url = "https://" + website_url

    try:
        # Generate brochure
        print(f"\n{'=' * 60}")
        print(f"Generating brochure for: {website_url}")
        print(f"{'=' * 60}\n")

        brochure = create_brochure(website_url, model)

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
