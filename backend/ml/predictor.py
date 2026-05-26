import json
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"


def recommend_category(features):
    # This helper keeps the recommendation understandable and explainable for students.
    category = features.get("package_category", "").strip()
    if category:
        return category

    budget = float(features.get("user_budget", 0))
    ratings = float(features.get("user_ratings", 4.0))
    interests = str(features.get("interests", "")).lower()

    if "honeymoon" in interests or "romantic" in interests:
        return "Honeymoon"
    if "adventure" in interests or float(features.get("trip_duration", 0)) >= 5:
        return "Adventure"
    if budget <= 8000:
        return "Budget"
    if ratings >= 4.5:
        return "Luxury"
    return "Family"


def predict_booking(features):
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model file not found. Train the model first using train_model.py")

    model = joblib.load(MODEL_PATH)
    row = pd.DataFrame([features])
    prediction = model.predict(row)[0]
    probabilities = model.predict_proba(row)[0]
    classes = model.classes_
    confidence = float(max(probabilities))

    probability_map = {label: round(float(prob), 2) for label, prob in zip(classes, probabilities)}
    result = {
        "prediction_label": prediction,
        "recommended_category": recommend_category(features),
        "confidence": round(confidence, 2),
        "probabilities": probability_map,
    }
    return result
