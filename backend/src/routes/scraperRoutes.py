from fastapi import APIRouter
from src.controllers.scraperController import scrapeController
from src.schema.request import Url

router=APIRouter()

@router.post("/api/scrape/")
async def root(url: Url):
    return await scrapeController(url)