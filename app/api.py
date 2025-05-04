from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, validator
from typing import Optional
from .llm import TrendsToStory
from .scraper import TrendScraper

app = FastAPI()

llm = TrendsToStory()
scraper = TrendScraper()

# Define valid sources and themes
VALID_SOURCES = ["news", "youtube", "google"]

VALID_THEMES = [
    "comedy",
    "tragedy",
    "arcasm",
    "drama",
    "adventure",
    "horror",
    "romance",
    "mystery"
]

class StoryRequest(BaseModel):
    source: str
    theme: str

class StoryResponse(BaseModel):
    story: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest, response: Response):
    if not request.source:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StoryResponse(error="Source is required")
    if not request.theme:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StoryResponse(error="Theme is required")
        
    if request.source not in VALID_SOURCES:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StoryResponse(error="Invalid source")
    if request.theme not in VALID_THEMES:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return StoryResponse(error="Invalid theme")
    
    try:
        trends = await scraper.get_trends(request.source)
        response = await llm.generate_story(trends, request.theme)
        return StoryResponse(story=response)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return StoryResponse(error=str(e))