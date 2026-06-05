from sqlalchemy.orm import Session
from fastapi import Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.schema.request import Url
from src.services.scraperService import connectToPage
from src.db.repo.productRepo import createProduct, getAllProducts, getProductByIdentifier
from datetime import datetime
from zoneinfo import ZoneInfo

def getCleanUrl(url: str):
    cleanUrl = url.split("/?")[0]
    cleanUrl = cleanUrl.split("/ref")[0]
    return cleanUrl

async def scrapeController(url: Url, db: Session):
    urlString = url.url
    urlString = getCleanUrl(urlString)

    prod_identifier = urlString.split("/")[-1]
    prod = getProductByIdentifier(db, prod_identifier)
    if prod["exists"]:
        return {
            "success": True,
            "message": "Already had data",
            "data": prod["data"]
        }
    
    data = await connectToPage(urlString)
    print(data)
    for key, value in data.items():
        print(key, value, type(value))
    
    product = createProduct(db, data)

    return{
        "success": True,
        "message": "Scraped data",
        "data": product["product"]
    }

async def getAllDataController(db: Session):
    data = getAllProducts(db)
    return{
        "success": True,
        "message": "Data fetched successfully",
        "data": data
    }

async def rescrapeDataController(request: Request):
    scheduler: AsyncIOScheduler = request.app.state.scheduler

    scheduler.modify_job(
        job_id="weekly_scraper_job",
        next_run_time=datetime.now(ZoneInfo("Asia/Kolkata"))
    )
    return{
        "success": True,
        "message": "Rescraper in progress",
    }