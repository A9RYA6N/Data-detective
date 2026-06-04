from fastapi import FastAPI
from src.routes.scraperRoutes import router
from src.services.schedulerService import lifespan

app=FastAPI(lifespan=lifespan)

app.include_router(router)
@app.get("/")
async def fallback():
    return {
        "message":"Hello"
    }