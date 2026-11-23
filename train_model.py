
import random
import string
import json
import joblib
import pandas as pd

from features_extraction import extract_features

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# SENTINEL AI - MODEL TRAINING
# ==========================================

print("\n🛡️ SENTINEL AI MODEL TRAINING")
print("=" * 45)

random.seed(42)


# ==========================================
# GENERATE SYNTHETIC PASSWORDS
# ==========================================

def generate_password():
    length = random.randint(4, 24)

    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*()_+-="
    )

    return "".join(random.choices(characters, k=length))


# ==========================================
# CLASSIFY SYNTHETIC SAMPLES
# ==========================================

def classify_sample(password):
    score = 0

    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    else:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(not c.isalnum() for c in password):
        score += 2

    if any(password.count(c) > 2 for c in set(password)):
        score -= 2

    sequences = [
        "123", "234", "345", "456",
        "567", "678", "789",
        "abc", "bcd", "cde", "def", "qwerty"
    ]

    if any(sequence in password.lower() for sequence in sequences):
        score -= 2

    if score <= 3:
        return "Weak"
    elif score <= 6:
        return "Medium"
    else:
        return "Strong"


# ==========================================
# CREATE DATASET
# ==========================================

print("\nGenerating synthetic dataset...")

passwords = [
    generate_password()
    for _ in range(10000)
]

# extract_features returns dictionaries,
# so convert them directly into a DataFrame.
features = pd.DataFrame([
    extract_features(password)
    for password in passwords
])

labels = [
    classify_sample(password)
    for password in passwords
]

dataset = features.copy()
dataset["strength"] = labels

print("\nDataset generated successfully!")
print("Dataset size:", len(dataset))

class_distribution = (
    dataset["strength"].value_counts().to_dict()
)

print("\nClass distribution:")
for category, count in class_distribution.items():
    print(f"{category}: {count}")


# ==========================================
# SPLIT DATASET
# ==========================================

X = dataset.drop("strength", axis=1)
y = dataset["strength"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Input features:", len(X.columns))


# ==========================================
# TRAIN RANDOM FOREST MODEL
# ==========================================

print("\nTraining Random Forest Classifier...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ==========================================
# MODEL EVALUATION
# ==========================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
) * 100

report = classification_report(
    y_test,
    predictions,
    output_dict=True,
    zero_division=0
)

matrix = confusion_matrix(
    y_test,
    predictions,
    labels=["Weak", "Medium", "Strong"]
)

print("\n" + "=" * 45)
print("MODEL EVALUATION")
print("=" * 45)

print(f"\nAccuracy: {accuracy:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(matrix)


# ==========================================
# SAVE TRAINED MODEL
# ==========================================

joblib.dump(model, "password_model.pkl")

print("\nModel saved successfully!")
print("File: password_model.pkl")


# ==========================================
# SAVE MODEL METRICS
# ==========================================

metrics = {
    "accuracy": round(float(accuracy), 2),
    "train_samples": int(len(X_train)),
    "test_samples": int(len(X_test)),
    "dataset_size": int(len(dataset)),
    "feature_count": int(X.shape[1]),

    "class_distribution": {
        str(key): int(value)
        for key, value in class_distribution.items()
    },

    "labels": [
        "Weak",
        "Medium",
        "Strong"
    ],

    "confusion_matrix": matrix.tolist(),

    "classification_report": report
}

with open("model_metrics.json", "w") as file:
    json.dump(metrics, file, indent=4)

print("\nMetrics saved successfully!")
print("File: model_metrics.json")


# ==========================================
# COMPLETED
# ==========================================

print("\n" + "=" * 45)
print("✅ SENTINEL AI TRAINING COMPLETED!")
print("=" * 45)
