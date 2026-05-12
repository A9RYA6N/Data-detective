from fastapi import FastAPI
from src.routes.testRoutes import router

app=FastAPI()

app.include_router(router)