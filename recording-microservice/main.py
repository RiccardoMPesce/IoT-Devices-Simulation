from asyncio.log import logger
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.mqtt import fast_mqtt
from api.endpoint import endpoint
from db.database import database
from models.recording import Record, IntRecord, BooleanRecord, StringRecord, FloatRecord

app = FastAPI()

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

@app.on_event("startup")
async def startup_event():
    if not database.is_connected:
        await database.connect()
    logger.info("Creating some test entries")
    # Test entries
    # await IntRecord.objects.get_or_create("test_id_int")
    # await BooleanRecord.objects.get_or_create("test_id_boolean")
    # await StringRecord.objects.get_or_create("test_id_string")
    # await FloatRecord.objects.get_or_create("test_id_float")
    await Record.objects.get_or_create("test_id")
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8001)