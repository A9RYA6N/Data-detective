from sqlalchemy.orm import Session
from fastapi import Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.schema.request import Url
from src.services.scraperService import connectToPage
from src.db.repo.productRepo import createProduct, getAllProducts, getAllProductsUrlAndId
from src.services.rescrapeService import rescrapeData
from datetime import datetime
from zoneinfo import ZoneInfo

async def scrapeController(url: Url, db: Session):
    data = await connectToPage(url.url)
    print(data)
    for key, value in data.items():
        print(key, value, type(value))
    
    product = createProduct(db, data)

    return{
        "success": True,
        "message": "Scraped data" if product["existed"]==False else "Already had data",
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