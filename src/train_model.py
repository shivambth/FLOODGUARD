"""Train and evaluate a demo classifier. Uses synthetic data by default."""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

try:
    from .generate_demo_data import make_data
except ImportError:
    from generate_demo_data import make_data

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "floodguard_demo_model.joblib"
METRICS_PATH = ROOT / "reports" / "demo_model_metrics.json"

FEATURES = [
    "rainfall_24h_mm", "rainfall_72h_mm", "river_level_m",
    "river_capacity_m", "soil_saturation_pct", "elevation_m",
    "drainage_score"
]
TARGET = "flood_within_24h"

def train():
    df = make_data(n=5000, seed=42)
    X, y = df[FEATURES], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(
            n_estimators=250, max_depth=9, min_samples_leaf=4,
            class_weight="balanced", random_state=42, n_jobs=-1
        ))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]
    metrics = {
        "dataset": "synthetic demonstration data",
        "rows": int(len(df)),
        "test_rows": int(len(y_test)),
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, prob)), 4),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "important_note": "These metrics only measure fit to synthetic teaching data. They do NOT indicate real-world flood prediction performance."
    }
    MODEL_PATH.parent.mkdir(exist_ok=True)
    METRICS_PATH.parent.mkdir(exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES, "target": TARGET}, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    train()
