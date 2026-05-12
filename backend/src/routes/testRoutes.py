from fastapi import APIRouter
from src.controllers.testController import testController

router=APIRouter()

@router.get("/")
async def root():
    return await testController()