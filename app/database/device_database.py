import motor.motor_asyncio

from common import device_helper

from database.commons import database_client

from bson.objectid import ObjectId


device_database = database_client.device

device_collection = device_database.get_collection("device_collection")

async def retrieve_devices():
    devices = []
    async for device in device_collection.find():
        devices.append(device_helper(device))
    return devices


# Add a new device into to the database
async def add_device(device_data: dict) -> dict:
    device = await device_collection.insert_one(device_data)
    new_device = await device_collection.find_one({"_id": ObjectId(device.inserted_id)})
    return device_helper(new_device)


# Retrieve a device with a matching device ID (not internal id)
async def retrieve_device(device_id: str) -> dict:
    device = await device_collection.find_one({"device_id": device_id})
    if device:
        return device_helper(device)


# Update a device with a matching device ID (not internal id)
async def update_device(device_id: str, data: dict):
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
async def delete_device(device_id: str):
    device = await device_collection.find_one({"device_id": device_id})
    if device:
        await device_collection.delete_one({"device_id": device_id})
        return True
