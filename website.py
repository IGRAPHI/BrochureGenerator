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

        # More comprehensive headers to mimic a real browser
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0",
        }

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                raise Exception(
                    f"Access denied (403 Forbidden) for {url}. The website is blocking automated requests. Try a different URL or contact the website administrator."
                )
            else:
                raise Exception(f"HTTP error {response.status_code}: {e}")
        except requests.exceptions.Timeout:
            raise Exception(
                f"Request timeout for {url}. The website took too long to respond."
            )
        except requests.exceptions.ConnectionError:
            raise Exception(
                f"Connection error for {url}. Check your internet connection or the URL."
            )
        except Exception as e:
            raise Exception(f"Failed to fetch {url}: {str(e)}")

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
