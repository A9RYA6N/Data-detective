from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.services.rescrapeService import rescrapeData
from zoneinfo import ZoneInfo

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        rescrapeData,
        CronTrigger(
            day_of_week="sun",
            hour=0,
            minute=0,
            timezone=ZoneInfo("Asia/Kolkata")
        ),
        id="weekly_scraper_job",
        coalesce=True,
        max_instances=1,
    )
    scheduler.start()
    app.state.scheduler=scheduler
    yield
    scheduler.shutdown()