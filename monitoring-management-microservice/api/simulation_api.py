import json
import time

from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import JSONResponse
from typing import Union

from db.common import get_database, DatabaseManager
from utils.mqtt import fast_mqtt
from utils.config import get_config
from utils.logger import logger_config

logger = logger_config(__name__)

settings = get_config()

router = APIRouter(prefix="/simulate")

@router.put(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str}
    },
)
async def simulate_recording(device_id: str, 
                             measure_value: Union[int, bool, float], 
                             health: bool, 
                             db: DatabaseManager = Depends(get_database)) -> list:
    
    device = await db.device_get_one(device_id=device_id)

    if device and device["status"]:
        measure = {
            "device_id": device_id,
            "measure": device.get("measure"),
            "measure_value": float(measure_value),
            "health": int(health),
            "timestamp": int(time.time())
        }
        topic = settings.MQTT_TOPIC_PREFIX + device.get("measure") + "/" + device_id
        fast_mqtt.client.publish(
            topic, 
            payload=json.dumps(measure), 
            qos=device.get("publish_qos")
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Measure " + str(measure) + " pushed to topic " + topic)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measure not created",
        )

