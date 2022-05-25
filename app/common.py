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