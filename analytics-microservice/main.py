import asyncio
import uvicorn
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# logger = logger_config(__name__)
# settings = get_config()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.include_router(endpoint)

# Init MQTT


@app.on_event("startup")
async def startup_event():
    pass
        
@app.on_event("shutdown")
async def shutdown_event():
    pass
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8001)