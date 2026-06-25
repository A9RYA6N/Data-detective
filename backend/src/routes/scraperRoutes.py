from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.controllers.scraperController import scrapeController, getAllDataController, rescrapeDataController, getAllSnapshotsController
from src.schema.request import Url
from src.config.db import getDb

router=APIRouter()

@router.post("/api/scrape/")
async def scrape(url: Url, db: Session=Depends(getDb)):
    return await scrapeController(url, db)

@router.get("/api/")
async def getAllData(db: Session=Depends(getDb)):
    return await getAllDataController(db)

@router.get("/api/scrape/all")
async def rescrapeAllData(request: Request):
    return await rescrapeDataController(request)

@router.get("/api/snapshot/")
async def getAllSnapshots(db: Session=Depends(getDb)):
    return await getAllSnapshotsController(db)