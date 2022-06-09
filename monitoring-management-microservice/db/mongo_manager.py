import json
import os
from typing import List

from bson.json_util import dumps
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from db.database_manager import DatabaseManager
from models.device_schema import Device, UpdateDevice
from utils.logger import logger_config

logger = logger_config(__name__)


class MongoManager(DatabaseManager):
    """
    This class extends from ./database_manager.py
    which have the abstract methods to be re-used here.
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    # database connect and close connections
    async def connect_to_database(self, path: str, db_name: str):
        logger.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)

        self.db = self.client[db_name]

        logger.info("Connected to MongoDB - " + os.getenv("ENVIRONMENT", "dev") + " environment!")

    async def close_database_connection(self):
        logger.info("Closing connection to MongoDB")
        self.client.close()
        logger.info("MongoDB connection closed")

    # to be used from /api/public endpoints
    async def device_get_total(self) -> int:
        total = await self.db.devices.count_documents({})
        return total

    async def device_get_actives(self) -> int:
        devices = self.db.devices.find({"status": True})
        devices_list = []
        async for device in devices:
            devices_list.append(json.loads(dumps(device)))

        return len(devices_list)

    async def device_get_all(self) -> List[Device]:
        devices_list = []
        devices = self.db.devices.find()

        async for device in devices:
            del device["_id"]
            devices_list.append(json.loads(dumps(device)))

        return devices_list

    async def device_get_one(self, device_id: str) -> Device:
        devices = self.db.devices.find({"device_id": device_id})

        async for device in devices:
            del device["_id"]
            return json.loads(dumps(device))

    async def device_insert_one(self, device: Device) -> Device:
        device_exist = await self.device_get_one(device_id=device.dict()["device_id"])
        if device_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"device: {device_exist['device_id']} already exist",
            )

        await self.db.devices.insert_one(device.dict())

        device = await self.device_get_one(device_id=device.dict()["device_id"])

        return device

    async def device_update_one(self, device: UpdateDevice) -> list:
        _device = device.dict()
        device_to_update = await self.device_get_one(device_id=_device["device_id"])
        logger.info(str(device_to_update))

        if device_to_update:
            for k, v in _device.items():
                if v is not None:
                    device_to_update[k] = v

            await self.db.devices.update_one({"device_id": _device["device_id"]}, {"$set": device_to_update})
            device_updated = await self.device_get_one(device_id=_device["device_id"])

            return device_updated
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device with id " + _device["device_id"] + " not found"
            )

    async def device_delete_one(self, device_id: str) -> List[Device]:
        await self.db.devices.delete_one({"device_id": device_id})
            
        deleted_device = await self.device_get_one({"device_id": device_id})

        return deleted_device
