import json
import os
from typing import List

from bson.json_util import dumps
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from db.database_manager import DeviceDatabaseManager, MeasureDatabaseManager
from models.device_schema import Device
from models.measure_schema import Measure
from utils.logger import logger_config

logger = logger_config(__name__)


class DeviceMongoManager(DeviceDatabaseManager):
    """
    This class extends from ./database_manager.py
    which have the abstract methods to be re-used here.
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    # database connect and close connections
    async def connect_to_database(self, path: str):
        logger.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)

        if os.getenv("ENVIRONMENT") == "PRD":
            self.db = self.client.devices_prd
        elif os.getenv("ENVIRONMENT") == "STG":
            self.db = self.client.devices_stg
        else:
            self.db = self.client.devices_dev

        logger.info(
            "Connected to MongoDB -  %s environment!", os.getenv("ENVIRONMENT", "DEV")
        )

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

    async def device_update_one(self, device: Device) -> list:
        _device = device.dict()
        await self.db.devices.update_one({"device_id": _device["device_id"]}, {"$set": _device})
        device_updated = await self.device_get_one(device_id=_device["device_id"])

        return device_updated

    async def device_delete_one(self, device: Device) -> List[Device]:
        await self.db.devices.delete_one(device.dict())

        device_deleted = await self.device_get_one(device_id=device.dict()["device_id"])

        return device_deleted


class MeasureMongoManager(MeasureDatabaseManager):
    """
    This class extends from ./database_manager.py
    which have the abstract methods to be re-used here.
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    # database connect and close connections
    async def connect_to_database(self, path: str):
        logger.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)

        if os.getenv("ENVIRONMENT") == "PRD":
            self.db = self.client.measures_prd
        elif os.getenv("ENVIRONMENT") == "STG":
            self.db = self.client.measures_stg
        else:
            self.db = self.client.measures_dev

        logger.info(
            "Connected to MongoDB -  %s environment!", os.getenv("ENVIRONMENT", "DEV")
        )

    async def close_database_connection(self):
        logger.info("Closing connection to MongoDB")
        self.client.close()
        logger.info("MongoDB connection closed")

    # to be used from /api/public endpoints
    async def measure_get_total(self) -> int:
        total = await self.db.measures.count_documents({})
        return total

    async def measure_get_actives(self) -> int:
        measures = self.db.measures.find({"status": True})
        measures_list = []
        async for measure in measures:
            measures_list.append(json.loads(dumps(measure)))

        return len(measures_list)

    async def measure_get_all(self) -> List[Measure]:
        measures_list = []
        measures = self.db.measures.find()

        async for measure in measures:
            del measure["_id"]
            measures_list.append(json.loads(dumps(measure)))

        return measures_list

    async def measure_get_one(self, measure_id: str) -> Measure:
        measures = self.db.measures.find({"measure_id": measure_id})

        async for measure in measures:
            del measure["_id"]
            return json.loads(dumps(measure))

    async def measure_insert_one(self, measure: Measure) -> Measure:
        measure_exist = await self.measure_get_one(measure_id=measure.dict()["measure_id"])
        if measure_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"measure: {measure_exist['measure_id']} already exist",
            )

        await self.db.measures.insert_one(measure.dict())

        measure = await self.measure_get_one(measure_id=measure.dict()["measure_id"])

        return measure

    async def measure_update_one(self, measure: Measure) -> list:
        _measure = measure.dict()
        await self.db.measures.update_one({"measure_id": _measure["measure_id"]}, {"$set": _measure})
        measure_updated = await self.measure_get_one(measure_id=_measure["measure_id"])

        return measure_updated

    async def measure_delete_one(self, measure: Measure) -> List[Measure]:
        await self.db.measures.delete_one(measure.dict())

        measure_deleted = await self.measure_get_one(measure_id=measure.dict()["measure_id"])

        return measure_deleted
