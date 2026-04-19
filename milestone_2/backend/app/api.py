from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.agent import run_agent

app = FastAPI()

class InputData(BaseModel):
    crop: str
    season: str
    state: str
    rainfall: float
    temperature: float
    pH: float
    fertilizer: float
    query: str


@app.post("/predict")
def predict(data: InputData):
    result = run_agent(data.dict())
    return result