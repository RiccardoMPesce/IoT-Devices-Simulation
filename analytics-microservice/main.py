import asyncio
import uvicorn
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import test_ch, ch_init
from utils.logger import logger_config
from utils.config import get_config
from utils.kafka import consume
from api.endpoint import endpoint


logger = logger_config(__name__)

settings = get_config()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, description=settings.DESCRIPTION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(endpoint)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Testing clickhouse DB_URI {settings.DB_URI}")
    await test_ch()
    await ch_init()
    asyncio.create_task(consume())
        
@app.on_event("shutdown")
async def shutdown_event():
    pass
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8002)