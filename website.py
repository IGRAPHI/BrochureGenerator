"""
Website content extraction module.
Provides the Website class for fetching and parsing web content.
"""

import requests
from bs4 import BeautifulSoup
from typing import List


class Website:
    """
    A class to represent a website and extract its title, content, and links.

    Attributes:
        url (str): The URL of the website
        title (str): The page title
        website_content (str): Cleaned text content of the page
        links (List[str]): List of all links found on the page
    """

    def __init__(self, url: str):
        """
        Initialize a Website object by fetching and parsing the given URL.

        Args:
            url (str): The URL to fetch and parse
        """
        self.url = url
        self.links = []  # initialize links list

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # use html.parser as a fallback if lxml isn't available
        try:
            soup = BeautifulSoup(response.text, "lxml")
        except Exception:
            soup = BeautifulSoup(response.text, "html.parser")

        # TITLE IS LOADED (use safe access)
        self.title = getattr(soup.title, "string", url)

        # BODY IS CLEANED
        for tag in soup.find_all(["meta", "script", "style", "noscript"]):
            tag.decompose()

        # WEB-CONTENT IS LOADED
        self.website_content = soup.get_text(separator=" ", strip=True)

        # LINKS ARE LOADED
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if href:
                self.links.append(href)
