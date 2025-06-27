# 📁 backend/app/model_loader.py
import json
import tensorflow as tf
from tensorflow.keras.layers import Lambda
from keras.utils import custom_object_scope


def load_model_and_classes():
    # Register the custom Lambda layer by name 'TrueDivide'
    print("Loading model...")
    with custom_object_scope({'TrueDivide': Lambda(lambda x: x / 255.0)}):
        model = tf.keras.models.load_model("../model/plant_disease_model.h5")  # ✅ Corrected path
    print("Model loaded!")

    # Load class names from JSON file
    with open("../app/class_names.json") as f:  # ✅ Corrected path
        class_names = json.load(f)

    return model, class_names
