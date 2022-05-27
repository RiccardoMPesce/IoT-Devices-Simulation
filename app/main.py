
import uvicorn

from datetime import datetime

from fastapi import FastAPI

from api.device_router import router as device_router

app = FastAPI(title="Monitoring & Management Microservice")
app.include_router(device_router, tags=["Device"], prefix="/device")

@app.get("/", tags=["Root"], description="Root page, to show if the app is running or not")
def root():
    return {"status": "up", "timestamp": datetime.now()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)