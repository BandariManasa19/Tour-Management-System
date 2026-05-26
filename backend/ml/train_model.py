import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "tourism_dataset.csv"
MODEL_PATH = BASE_DIR / "model.pkl"


def build_dataset():
    # This is a small synthetic dataset, created to help students see a realistic
    # ML workflow without requiring a live external data source.
    rows = []
    destinations = ["Goa", "Jaipur", "Kerala", "Manali", "Maldives", "Udaipur", "Rishikesh"]
    seasons = ["Summer", "Winter", "Monsoon", "Spring"]
    categories = ["Adventure", "Family", "Honeymoon", "Budget", "Luxury"]

    for destination in destinations:
        for season in seasons:
            for category in categories:
                for i in range(15):
                    budget = 5000 + i * 350
                    duration = 2 + (i % 4)
                    previous_bookings = i % 5
                    ratings = 3.5 + (i % 5) * 0.3

                    # Booking probability rule: higher ratings, stronger budget fit,
                    # and category-style destinations get better scores.
                    score = 0
                    if budget >= 8000:
                        score += 1
                    if duration >= 4:
                        score += 1
                    if previous_bookings >= 2:
                        score += 1
                    if ratings >= 4.2:
                        score += 1
                    if category in ["Luxury", "Honeymoon"] and budget >= 12000:
                        score += 1
                    if category == "Budget" and budget <= 8000:
                        score += 1

                    if score >= 4:
                        label = "High"
                    elif score >= 2:
                        label = "Medium"
                    else:
                        label = "Low"

                    rows.append(
                        {
                            "user_budget": budget,
                            "preferred_destination": destination,
                            "trip_duration": duration,
                            "previous_bookings": previous_bookings,
                            "user_ratings": round(ratings, 1),
                            "travel_season": season,
                            "package_category": category,
                            "booking_probability": label,
                        }
                    )

    dataset = pd.DataFrame(rows)
    dataset.to_csv(DATASET_PATH, index=False)
    return dataset


def train_model():
    if not DATASET_PATH.exists():
        dataset = build_dataset()
    else:
        dataset = pd.read_csv(DATASET_PATH)

    feature_columns = [
        "user_budget",
        "preferred_destination",
        "trip_duration",
        "previous_bookings",
        "user_ratings",
        "travel_season",
        "package_category",
    ]
    target_column = "booking_probability"

    X = dataset[feature_columns]
    y = dataset[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    categorical_features = ["preferred_destination", "travel_season", "package_category"]
    numeric_features = ["user_budget", "trip_duration", "previous_bookings", "user_ratings"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features),
        ]
    )

    model = Pipeline(
        [
            ("preprocess", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
        ]
    )

    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved at {MODEL_PATH}")
    print(f"Model accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    train_model()
