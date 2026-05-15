from fastapi import FastAPI
from src.routes.scraperRoutes import router

app=FastAPI()

app.include_router(router)
@app.get("/")
async def fallback():
    return {
        "message":"Hello"
    }