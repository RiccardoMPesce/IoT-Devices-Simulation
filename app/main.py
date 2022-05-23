from fastapi import FastAPI

import uvicorn

from models.device import Device

app = FastAPI()

@app.get("/")
def root_msg():
    return {"status": "up"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)