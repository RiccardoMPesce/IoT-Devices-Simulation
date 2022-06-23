import uuid
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.mqtt import fast_mqtt
from utils.logger import logger_config
from api.endpoint import endpoint
from db.database import database, Record
# from models.recording import Record

app = FastAPI()

logger = logger_config(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(endpoint)

# Init MQTT
fast_mqtt.init_app(app)

app.state.database = database

@app.on_event("startup")
async def startup_event():
    database_ = app.state.database
    if not database_.is_connected:
        await database.connect()
        

@app.on_event("shutdown")
async def shutdown_event():
    database_ = app.state.database
    if database_.is_connected:
        await database.disconnect()
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8001)