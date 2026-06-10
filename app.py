import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import os
from datasets import Dataset
import transformers
if not hasattr(transformers, 'training_args'):
    import transformers.training_args
if not hasattr(transformers.training_args, 'default_logdir'):
    def default_logdir():
        import datetime
        return os.path.join("runs", datetime.datetime.now().strftime("%b%d_%H-%M-%S"))
    transformers.training_args.default_logdir = default_logdir

from setfit import SetFitModel
from contextlib import asynccontextmanager

# Global model variable
model = None

# Map predictions back to original string intents
LABEL_MAP = {0: "LEAD", 1: "SUPPORT", 2: "SPAM", 3: "IDLE"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on startup
    global model
    print("Loading SetFit model into memory from ./setfit_intent_model_final ...")
    model = SetFitModel.from_pretrained("./setfit_intent_model_final")
    print("Model successfully loaded and ready for predictions!")
    yield
    # This runs on shutdown
    print("Cleaning up model...")
    model = None

# Initialize FastAPI application
app = FastAPI(title="Social Media Intent Classification API", lifespan=lifespan)

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict_intent(request: PredictRequest):
    # Perform prediction
    prediction = model.predict([request.text])[0]
    
    # Convert potential tensor/numpy output to native python int
    if hasattr(prediction, "item"):
        pred_val = prediction.item()
    else:
        pred_val = int(prediction)
        
    # Retrieve the string intent
    intent_label = LABEL_MAP.get(pred_val, "UNKNOWN")
    
    return {
        "text": request.text,
        "intent": intent_label
    }

if __name__ == "__main__":
    print("Starting API Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
