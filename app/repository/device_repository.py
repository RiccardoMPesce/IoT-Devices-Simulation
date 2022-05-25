from fastapi.encoders import jsonable_encoder

import motor.motor_asyncio

with open(".env", "r+") as env_file:
    mongo_params = dict(line.strip().split("=") for line in env_file.readlines() if line.strip() != "") 

mongo_host = mongo_params["MONGO_HOST"]
mongo_port = mongo_params["MONGO_PORT"]
mongo_details = f"mongodb://{mongo_host}:{mongo_port}"

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_details)

device_database = client.device

device_collection = device_database.get_collection("device_collection")


# Helper function
def device_helper(device) -> dict:
    return {
        "id": str(device["_id"]),
        "device_id": device["device_id"],
        "measure": device["measure"],
        "publish_qos": str(device["publish_"]),
        "status": str(device["status"]),
        "update_datetime": str(device["update_datetime"])
    }

class DeviceRepository:
    def __init__(self):
        pass

    async def retrieve_devices(self):
        devices = []
        async for device in device_collection.find():
            devices.append(device_helper(device))
        return devices

    # Add a new device into to the database
    async def add_device(self, device_data: dict) -> dict:
        device = await device_collection.insert_one(device_data)
        new_device = await device_collection.find_one({"_id": device.inserted_id})
        return device_helper(new_device)

    # Retrieve a device with a matching device ID (not internal id)
    async def retrieve_device(self, device_id: str) -> dict:
        device = await device_collection.find_one({"device_id": device_id})
        if device:
            return device_helper(device)

    # Update a device with a matching device ID (not internal id)
    async def update_device(self, device_id: str, data: dict):
        # Return false if an empty request body is sent.
        if len(data) < 1:
            return False
        device = await device_collection.find_one({"device_id": device_id})
        if device:
            updated_device = await device_collection.update_one(
                {"device_id": device_id}, {"$set": data}
            )
            return True if updated_device else False

    # Delete a device from the database
    async def delete_device(self, device_id: str):
        device = await device_collection.find_one({"device_id": device_id})
        if device:
            await device_collection.delete_one({"device_id": device_id})
            return True