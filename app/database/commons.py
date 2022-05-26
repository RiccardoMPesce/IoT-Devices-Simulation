import motor.motor_asyncio

with open(".env", "r+") as env_file:
    mongo_params = dict(line.strip().split("=") for line in env_file.readlines() if line.strip() != "") 

mongo_host = mongo_params["MONGO_HOST"]
mongo_port = mongo_params["MONGO_PORT"]
mongo_details = f"mongodb://{mongo_host}:{mongo_port}"

database_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_details)
