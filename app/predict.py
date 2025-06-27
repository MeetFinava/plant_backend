# 📁 backend/app/predict.py
import numpy as np
from PIL import Image
import io
from translator import translate_label, get_treatment

def predict_image(model, class_names, image_bytes, lang='en'):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_batch)[0]
    idx = int(np.argmax(preds))
    confidence = round(float(preds[idx]) * 100, 2)
    label_en = class_names[idx]
    label_translated = translate_label(label_en, lang)
    treatment = get_treatment(label_en)

    return {
        "english_label": label_en,
        "translated_label": label_translated,
        "confidence": confidence,
        "treatment": treatment
    }

