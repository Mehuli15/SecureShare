import os
import math
import string
import joblib


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "anomaly_model.pkl"
)


# Same extension encoding used during training
EXTENSION_MAP = {
    ".txt": 0,
    ".pdf": 1,
    ".docx": 2,
    ".pptx": 3,
    ".jpg": 4,
    ".jpeg": 4,
    ".csv": 5,
    ".zip": 6,
}


def filename_entropy(filename):
    """Calculate Shannon entropy of the filename."""

    if not filename:
        return 0.0

    probabilities = []

    for char in set(filename):
        probability = filename.count(char) / len(filename)
        probabilities.append(probability)

    return -sum(
        p * math.log2(p)
        for p in probabilities
        if p > 0
    )


def extract_features(file_path):
    """Extract the four ML features."""

    filename = os.path.basename(file_path)

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    filename_length = len(filename)

    name_entropy = filename_entropy(filename)

    extension = os.path.splitext(filename)[1].lower()

    file_type = EXTENSION_MAP.get(
        extension,
        -1
    )

    return [[
        file_size_mb,
        filename_length,
        name_entropy,
        file_type
    ]]


def analyze_file(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    model = joblib.load(MODEL_PATH)

    features = extract_features(file_path)

    prediction = model.predict(features)[0]

    score = model.decision_function(features)[0]

    if prediction == 1:
        status = "NORMAL"
    else:
        status = "ANOMALOUS"

    return {
        "status": status,
        "score": float(score),
        "features": features[0]
    }