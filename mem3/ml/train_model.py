import numpy as np
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# ============================================================
# NORMAL FILE-TRANSFER DATA
# ============================================================

np.random.seed(42)

N = 500

# File size in MB
file_size = np.random.lognormal(
    mean=2.0,
    sigma=1.0,
    size=N
)

# Filename length
filename_length = np.random.normal(
    loc=18,
    scale=6,
    size=N
)

# Filename character entropy
filename_entropy = np.random.normal(
    loc=3.2,
    scale=0.5,
    size=N
)

# Extension/type encoding
# 0 = txt
# 1 = pdf
# 2 = docx
# 3 = pptx
# 4 = jpg
# 5 = csv
# 6 = zip
file_type = np.random.choice(
    [0, 1, 2, 3, 4, 5, 6],
    size=N
)


X_normal = np.column_stack([
    file_size,
    filename_length,
    filename_entropy,
    file_type
])


# ============================================================
# TRAIN ISOLATION FOREST
# ============================================================

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X_normal)


# ============================================================
# SAVE MODEL
# ============================================================

model_path = "ml/anomaly_model.pkl"

joblib.dump(model, model_path)

print("=" * 60)
print("ML MODEL TRAINING COMPLETE")
print("=" * 60)

print(f"Training samples : {N}")
print(f"Features         : {X_normal.shape[1]}")
print(f"Model            : Isolation Forest")
print(f"Saved to         : {model_path}")