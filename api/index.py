from fastapi import FastAPI, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from contextlib import asynccontextmanager
import logging

# 👇 Add proper lifespan usage
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.warning("🚀 FastAPI app started on Vercel!")
    yield

app = FastAPI(lifespan=lifespan)

# ✅ CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check route
@app.get("/")
def read_root():
    return JSONResponse({"message": "Backend is working!"})

# ✅ Load model
MODEL = tf.keras.models.load_model("saved_models/finalmodel.h5", compile=True)

# ✅ Define classes
CLASS_NAMES = [
    'Apple_brown_spot', 'Apple_healthy', 'Apple_scab',
    'Corn_common_rust', 'Corn_gray_leaf_spot', 'Corn_healthy', 'Corn_northern_leaf_blight',
    'Grape_Leaf_blight', 'Grape_black_measles', 'Grape_healthy',
    'Potato_Early_blight', 'Potato_Late_blight', 'Potato_healthy',
    'Strawberry_healthy', 'Strawberry_leaf_scorch',
    'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_healthy',
    'Watermelon_downy_mildew', 'Watermelon_healthy', 'Watermelon_mosaic_virus'
]

# ✅ Define medicine map
DISEASE_MEDICINE_MAP = {
    "Apple_brown_spot": {
        "name": "Captan",
        "description": "Controls brown spot in apples effectively.",
        "brand": "FungoStop"
    },
    "Apple_healthy": {
        "name": "No treatment needed",
        "description": "Your plant is healthy.",
        "brand": "-"
    },
    # ... (keep your full map here as is)
    "Watermelon_mosaic_virus": {
        "name": "Imidacloprid",
        "description": "Prevents viral spread by targeting aphid vectors.",
        "brand": "Confidor"
    }
}

# ✅ Helper to read file as image
def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")
    return image

# ✅ Predict route
@app.post("/predict")
async def predict(file: UploadFile = File(...), lang: str = Query("en")):
    image = await file.read()
    img_array = read_file_as_image(image)
    img_array = img_array.resize((256, 256))  # resize if needed to match model input
    img_batch = np.expand_dims(img_array, 0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    medicine = DISEASE_MEDICINE_MAP.get(predicted_class, {
        "name": "No specific medicine found",
        "description": "Please consult an expert for advice.",
        "brand": "N/A"
    })

    return {
        "disease": predicted_class,
        "confidence": float(confidence),
        "medicine": medicine
    }

# 👇 Required for Vercel
handler = app
