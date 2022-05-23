from pymongo import MongoClient

class DeviceRepository:
    def __init__(self):
        with open(".env", "r") as env_file:
            params = dict(line.strip().split("=") for line in env_file.readlines() if line.strip() != "")
        self.client = MongoClient(params["MONGO_HOST"], params["MONGO_PORT"])



