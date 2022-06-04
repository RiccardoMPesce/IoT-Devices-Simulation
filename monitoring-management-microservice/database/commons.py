import motor.motor_asyncio

# with open(".env", "r+") as env_file:
#     mongo_params = dict(line.strip().split("=") for line in env_file.readlines() if line.strip() != "") 

# mongo_host = mongo_params["MONGO_HOST"]
# mongo_port = mongo_params["MONGO_PORT"]
# mongo_user = mongo_params["MONGO_USER"]
# mongo_password = mongo_params["MONGO_PASSWORD"]
# mongo_db = mongo_params["MONGO_DB"]
# #mongo_details = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}"
# mongo_details = f"mongodb://{mongo_user}:{mongo_password}@db:{mongo_port}/{mongo_db}"

# database_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_details)
