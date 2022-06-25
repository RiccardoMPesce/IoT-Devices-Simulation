from datetime import datetime

from fastapi import APIRouter

endpoint = APIRouter()

@endpoint.get("/", tags=["Root"], description="Root page, to show if the app is running or not")
async def root():
    return {"status": "up", "timestamp": datetime.now()}