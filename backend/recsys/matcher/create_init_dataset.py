import json
import os
from pathlib import Path

import pandas as pd
from create_dataset_helpers import compute_similarity, flatten_doctor, flatten_patient

base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_vocab_path = base_path / "data" / "vocab_maps.json"
if _vocab_path.exists():
    with open(_vocab_path, "r", encoding="utf-8") as _f:
        _VOCAB_MAPS = json.load(_f)
else:
    _VOCAB_MAPS = {}
    print(f"{_vocab_path} not found")
MODULE_CONDITION_VOCAB_SIZE = len(_VOCAB_MAPS.get("conditions", {}))

def build_synthetic_dataset(condition_vocab_size = MODULE_CONDITION_VOCAB_SIZE, threshold=0.7):
    synthetic_pairs = []

    base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    patients_dir = Path(base_path / "data/synthea/encoded-patients")
    doctors_dir = Path(base_path / "data/npi/encoded-doctors")

    out_dir = Path(base_path / "data/synthetic_pairs_by_patient")
    out_dir.mkdir(parents=True, exist_ok=True)

    doctors = []
    for dfile in doctors_dir.glob("*.json"):
        try:
            with open(dfile, "r", encoding="utf-8") as f:
                doctors.append(json.load(f))
        except Exception:
            continue

    for pfile in patients_dir.glob("*.json"):
        try:
            with open(pfile, "r", encoding="utf-8") as f:
                p = json.load(f)
        except Exception:
            continue
        
        p_vec = flatten_patient(p, condition_vocab_size)
        for d in doctors:
            d_vec = flatten_doctor(d, condition_vocab_size)
            sim = compute_similarity(p_vec, d_vec)
            label = 1 if sim >= threshold else 0
            synthetic_pairs.append({
                "patient_id": p["patient_id"],
                "doctor_id": d["doctor_id"],
                "similarity": sim,
                "label": label
            })

    df = pd.DataFrame(synthetic_pairs)
    df.to_csv(out_dir / "synthetic_pairs.csv", index=False)

if(__name__=='__main__'):
    build_synthetic_dataset()