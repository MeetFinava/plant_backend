# 📁 backend/app/translator.py
import json

translations = {
    "hi": {
        "Potato___Early_blight": "आलू — अर्ली ब्लाइट",
        "Potato___Late_blight": "आलू — लेट ब्लाइट",
        "Potato___healthy": "आलू — स्वस्थ"
    },
    "gu": {
        "Potato___Early_blight": "બટાકું — આરંભિક બ્લાઇટ",
        "Potato___Late_blight": "બટાકું — મોડું બ્લાઇટ",
        "Potato___healthy": "બટાકું — તંદુરસ્ત"
    }
}

with open("treatments.json") as f:
    treatments = json.load(f)

def translate_label(label, lang='en'):
    return translations.get(lang, {}).get(label, label)

def get_treatment(label):
    return treatments.get(label, "No treatment info available")