from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io
from model_loader import load_model_and_classes
from predict import predict_image
from translator import translate_label, get_treatment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model, class_names = load_model_and_classes()

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...), lang: str = Form("en")):
    contents = await file.read()
    prediction = predict_image(model, class_names, contents, lang)
    return JSONResponse(prediction)
