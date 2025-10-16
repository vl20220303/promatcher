import json
import os
from pathlib import Path
from recsys.matcher.content_based_filter import compute_similarity, flatten_doctor, flatten_patient

base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_vocab_path = base_path / "data" / "vocab_maps.json"
if _vocab_path.exists():
    with open(_vocab_path, "r", encoding="utf-8") as _f:
        _VOCAB_MAPS = json.load(_f)
else:
    _VOCAB_MAPS = {}

MODULE_SPECIALTY_MAP = _VOCAB_MAPS.get("specialty_map")
MODULE_REVERSE_VOCAB = _VOCAB_MAPS.get("reverse_vocab")
MODULE_CONDITION_VOCAB_SIZE = _VOCAB_MAPS.get("condition_vocab_size") or len(_VOCAB_MAPS.get("condition_vocab", {}))

def build_synthetic_dataset(patients, doctors, condition_vocab_size, threshold=0.7, specialty_map=None, reverse_vocab=None):
    synthetic_pairs = []

    for p in patients:
        p_vec = flatten_patient(p, condition_vocab_size)
        for d in doctors:
            d_vec = flatten_doctor(d, condition_vocab_size, specialty_map, reverse_vocab)
            sim = compute_similarity(p_vec, d_vec)
            label = 1 if sim >= threshold else 0
            synthetic_pairs.append({
                "patient_id": p["patient_id"],
                "doctor_id": d["doctor_id"],
                "similarity": sim,
                "label": label
            })

    return synthetic_pairs

build_synthetic_dataset()