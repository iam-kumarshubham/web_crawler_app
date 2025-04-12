import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set

class WebRepository:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, url: str) -> str:
        """Fetch the content of a webpage."""
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                return ""
        except Exception:
            return ""

    def extract_links(self, html: str, base_url: str) -> Set[str]:
        """Extract all links from the HTML content."""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()

        for a in soup.find_all('a', href=True):
            href = a['href']
            absolute_url = urljoin(base_url, href)

            # Only include URLs from the same domain
            if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                links.add(absolute_url)

        return links