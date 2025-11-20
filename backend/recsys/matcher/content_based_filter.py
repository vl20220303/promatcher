import json
import os
from pathlib import Path

import pandas as pd
from create_init_dataset import build_synthetic_dataset
import xgboost as xgb
from sklearn.model_selection import train_test_split
from load_dataset_helpers import build_feature_vector, load_doctor, load_patient

base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
out_dir = Path(base_path / "matcher")

_vocab_path = base_path / "data" / "vocab_maps.json"
if _vocab_path.exists():
    with open(_vocab_path, "r", encoding="utf-8") as _f:
        _VOCAB_MAPS = json.load(_f)
else:
    _VOCAB_MAPS = {}
    print(f"{_vocab_path} not found")
vocab_sizes = len(_VOCAB_MAPS.get("conditions", {}))

def train_init_model():
    data_path = Path(base_path / "data/synthetic_pairs_by_patient/synthetic_pairs.csv")

    if not data_path.exists():
        build_synthetic_dataset()
    
    df = pd.read_csv(data_path)

    X = []
    y = []

    for _, row in df.iterrows():
        p = load_patient(row["patient_id"])
        d = load_doctor(row["doctor_id"])
        features = build_feature_vector(p, d, vocab_sizes)
        X.append(features)
        y.append(row["label"])

    model = xgb.XGBClassifier(
        objective="binary:logistic",
        eval_metric=["logloss", "auc"],
        use_label_encoder=False
    )

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    evals_result = {}
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, "train"), (X_val, "val")],
        eval_metric=["logloss", "auc"],
        early_stopping_rounds=10,
        verbose=True,
        evals_result=evals_result
    )

    print("Validation AUC:", evals_result["val"]["auc"][-1])
    print("Validation Logloss:", evals_result["val"]["logloss"][-1])

def incorporate_new_data(new_data):
    data_path = Path(base_path / "data/real_pairs/real_pairs.csv")

    if data_path.exists():
        df = pd.read_csv(data_path)
    else:
        df = pd.DataFrame()

train_init_model()