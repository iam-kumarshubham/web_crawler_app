import asyncio
import re
from typing import List, Dict, Set
from repositories.web_repository import WebRepository

class CrawlerService:
    def __init__(self, max_pages: int = 100, max_depth: int = 3):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.product_patterns = [
            r'/product/',
            r'/item/',
            r'/p/',
            r'/products/',
            r'/shop/',
            r'/buy/',
            r'/collection/'
        ]
        self.visited_urls: Set[str] = set()
        self.product_urls: Dict[str, Set[str]] = {}

    def is_product_url(self, url: str) -> bool:
        """Check if the URL matches any product URL patterns."""
        return any(re.search(pattern, url.lower()) for pattern in self.product_patterns)

    async def crawl_domain(self, domain: str) -> Dict[str, Set[str]]:
        """Crawl a single domain and collect product URLs."""
        if not domain.startswith(('http://', 'https://')):
            domain = 'https://' + domain

        self.visited_urls = set()
        self.product_urls[domain] = set()

        queue = [(domain, 0)]

        async with WebRepository() as repo:
            while queue and len(self.visited_urls) < self.max_pages:
                current_url, depth = queue.pop(0)

                if current_url in self.visited_urls or depth > self.max_depth:
                    continue

                self.visited_urls.add(current_url)

                if self.is_product_url(current_url):
                    self.product_urls[domain].add(current_url)

                html = await repo.fetch_page(current_url)
                if not html:
                    continue

                links = repo.extract_links(html, current_url)
                for link in links:
                    if link not in self.visited_urls:
                        queue.append((link, depth + 1))

        return {
            "domain": domain,
            "product_urls": list(self.product_urls[domain]),
            "status": "completed"
        }

    async def crawl_domains(self, domains: List[str]) -> List[Dict]:
        """Crawl multiple domains concurrently."""
        tasks = [self.crawl_domain(domain) for domain in domains]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out any exceptions and return successful results
        return [result for result in results if not isinstance(result, Exception)]