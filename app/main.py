
import uvicorn

from datetime import datetime

from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Root"], description="Root page, to show if the app is running or not")
def root():
    return {"status": "up", "timestamp": datetime.now()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)