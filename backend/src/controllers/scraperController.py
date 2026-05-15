from src.schema.request import Url
from src.services.scraperService import connectToPage

async def scrapeController(url: Url):
    return await connectToPage(url.url)
