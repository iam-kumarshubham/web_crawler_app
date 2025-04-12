from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from services.crawler_service import CrawlerService

app = FastAPI(title="E-commerce URL Crawler")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CrawlRequest(BaseModel):
    domains: List[str]
    max_pages: Optional[int] = 100
    max_depth: Optional[int] = 3

class CrawlResponse(BaseModel):
    domain: str
    product_urls: List[str]
    status: str

@app.post("/crawl", response_model=List[CrawlResponse])
async def crawl_websites(request: CrawlRequest):
    try:
        service = CrawlerService(
            max_pages=request.max_pages,
            max_depth=request.max_depth
        )
        results = await service.crawl_domains(request.domains)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}