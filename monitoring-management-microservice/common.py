from datetime import datetime

# Helper dictionaries
status_to_bool_dict = {
    True: True,
    "on": True,
    1: True,
    1.0: True,
    False: False,
    "off": False,
    0: False,
    0.0: False
}

status_to_int_dict = {k: int(v) for k, v in status_to_bool_dict.items()}
status_to_float_dict = {k: float(v) for k, v in status_to_int_dict.items()}
status_to_string_dict = {k: "on" if v else "off" for k, v in status_to_bool_dict.items()}

# Helper function
def device_helper(device) -> dict:
    return {
        "id": str(device["_id"]),
        "device_id": device["device_id"],
        "measure": device["measure"],
        "publish_qos": str(device["publish_qos"]),
        "status": status_to_string_dict(device["status"]),
        "update_datetime": str(datetime.fromtimestamp(device["update_datetime"])) 
    }
