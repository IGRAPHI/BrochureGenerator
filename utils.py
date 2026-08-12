"""
Utility functions for link extraction and content aggregation.
"""

import json
import urllib.parse
import google.generativeai as genai
from website import Website


def get_links(website: Website, model) -> dict:
    """
    Extract and classify relevant links from a website using LLM.

    Args:
        website (Website): Website object with links and url attributes
        model: Configured Gemini model instance

    Returns:
        dict: JSON structure with classified links
              Format: {"links": [{"type": str, "url": str}, ...]}
    """
    if not hasattr(website, "links") or not hasattr(website, "url"):
        raise ValueError("get_links expects a Website instance")

    prompt = """You are a link classifier that extracts relevant links for brochure generation.
Return ONLY a JSON object with relevant links classified by type.

Example format:
{
    "links": [
        {
            "type": "about",
            "url": "https://www.example.com/about/"
        },
        {
            "type": "products",
            "url": "https://www.example.com/products/"
        },
        {
            "type": "careers",
            "url": "https://www.example.com/careers/"
        },
        {
            "type": "press",
            "url": "https://www.example.com/newsroom/"
        }
    ]
}

"""
    prompt += (
        f"\nHere is the list of links {website.links} from the website {website.url}.\n"
    )
    prompt += "Return a JSON with only relevant links (about, products, careers, press, team) for brochure generation."

    try:
        response = model.generate_content(prompt)
        # Handle different response types
        text = getattr(response, "text", None) or str(response)

        # Parse JSON response
        links_data = json.loads(text)
        return links_data
    except json.JSONDecodeError:
        # Fallback: return empty structure
        print("Warning: Could not parse LLM response as JSON")
        return {"links": []}
    except Exception as e:
        print(f"Error in get_links: {e}")
        return {"links": []}


def website_content_all(main_url: str, model) -> str:
    """
    Fetch main website content and aggregate content from relevant sub-pages.

    Args:
        main_url (str): The main website URL to process
        model: Configured Gemini model instance

    Returns:
        str: Aggregated content from main page and sub-pages
    """
    # Fetch main website
    website = Website(main_url)
    website_body = f"# {website.title}\n\n{website.website_content}\n"

    # Get classified links
    links_data = get_links(website, model)

    # Fetch content from each relevant link
    for link_item in links_data.get("links", []):
        try:
            # Resolve relative URLs to absolute
            absolute_url = urllib.parse.urljoin(website.url, link_item["url"])

            print(f"Fetching {link_item['type']}: {absolute_url}")

            # Fetch sub-page
            sub_website = Website(absolute_url)

            # Append to main content with header
            website_body += (
                f"\n\n## {link_item['type'].upper()}\n\n{sub_website.website_content}\n"
            )

        except Exception as e:
            # Skip broken links but log the error
            print(f"Skipping {link_item.get('url', 'unknown')}: {e}")
            continue

    return website_body


def create_brochure(website_url: str, model_brochure) -> str:
    """
    Generate a professional company brochure from website content.

    Args:
        website_url (str): The company website URL
        model_brochure: Configured Gemini model with system instructions

    Returns:
        str: Formatted markdown brochure content
    """
    # Get the model used for link extraction (needs JSON config)
    import os
    from dotenv import load_dotenv

    load_dotenv()
    load_dotenv(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local"),
        override=True,
    )
    api_key = os.getenv("GENAI_API_KEY")

    if not api_key:
        raise ValueError("GENAI_API_KEY not found in environment variables")

    genai.configure(api_key=api_key)

    # Model for link extraction (JSON output)
    generation_config = {
        "response_mime_type": "application/json",
    }
    model_links = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp", generation_config=generation_config
    )

    # Fetch aggregated content
    print(f"Fetching content from {website_url}...")
    web_content = website_content_all(website_url, model_links)

    # Generate brochure
    print("Generating brochure...")
    prompt = f"""Create a detailed company brochure for the following content:

{web_content}

The brochure should include sections such as:
- Company Overview
- Products/Services
- Mission & Vision
- Team (if available)
- Contact Information

Format the brochure in a professional, engaging manner using Markdown.
Use proper headings, bullet points, and formatting to make it visually appealing.
"""

    response = model_brochure.generate_content(prompt)
    return response.text
