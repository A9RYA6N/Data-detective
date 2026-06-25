from fastapi import FastAPI
from src.routes.scraperRoutes import router
from src.services.schedulerService import lifespan
from src.config.db import Base
from src.config.db import engine

app=FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

app.include_router(router)
@app.get("/")
async def fallback():
    return {
        "message":"Hello"
    }