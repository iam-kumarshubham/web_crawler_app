# E-commerce URL Crawler

A FastAPI-based web crawler that discovers product URLs across multiple e-commerce websites.

## Features

- Concurrent crawling of multiple domains
- Intelligent product URL pattern matching
- Configurable crawling depth and page limits
- Asynchronous processing for better performance
- Robust error handling

## Live Deployment

The crawler API is deployed and accessible here:

**URL:** [https://webcrawlerapp-production.up.railway.app](https://webcrawlerapp-production.up.railway.app)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /crawl
Crawl multiple domains for product URLs.

Request body:
```json
{
    "domains": [
        "https://www.virgio.com/",
        "https://www.tatacliq.com/",
        "https://nykaafashion.com/",
        "https://www.westside.com/"
    ],
    "max_pages": 100,
    "max_depth": 3
}
```

### GET /health
Check the health status of the API.

## Configuration

The crawler can be configured with the following parameters:
- `max_pages`: Maximum number of pages to crawl per domain (default: 100)
- `max_depth`: Maximum depth to crawl from the root URL (default: 3)

## Product URL Patterns

The crawler recognizes product URLs based on common patterns:
- /product/
- /item/
- /p/
- /products/
- /shop/
- /buy/
- /collection/

## Error Handling

The crawler includes robust error handling for:
- Network timeouts
- Invalid URLs
- Rate limiting
- Connection errors 