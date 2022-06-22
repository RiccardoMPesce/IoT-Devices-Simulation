import uvicorn

from fastapi import FastAPI

from utils.mqtt import fast_mqtt

app = FastAPI()

# Init MQTT
fast_mqtt.init_app(app)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8001)