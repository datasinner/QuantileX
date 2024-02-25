from fastapi import FastAPI
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from src.components.model_trainer import ModelTrainer
import pandas as pd
import json

text: str = "What is price of BTC?"

app = FastAPI()


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/predict")
async def predict_route():
    try:
        os.system("python main.py")
        with open("artifacts/output/output_of_BTC-USD.json", "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise e


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
