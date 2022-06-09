from datetime import datetime

from fastapi import APIRouter

from api.device_api import router as device_router 

endpoint = APIRouter()

endpoint.include_router(device_router)

@endpoint.get("/", tags=["Root"], description="Root page, to show if the app is running or not")
def root():
    return {"status": "up", "timestamp": datetime.now()}