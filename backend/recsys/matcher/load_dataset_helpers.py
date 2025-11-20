import json
from pathlib import Path
import torch

BASE_PATH = Path(__file__).resolve().parent.parent
PATIENTS_DIR = BASE_PATH / "data" / "synthea" / "encoded-patients"
DOCTORS_DIR = BASE_PATH / "data" / "npi" / "encoded-doctors"

def load_patient(patient_id):
    path = PATIENTS_DIR / f"{patient_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_doctor(doctor_id):
    path = DOCTORS_DIR / f"{doctor_id}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def pad_categorical(cat_list, target_len):
    return cat_list + [0] * (target_len - len(cat_list)) if len(cat_list) < target_len else cat_list[:target_len]

def flatten_patient(profile, condition_vocab_size, cat_len=3):
    dense = torch.tensor(profile.get("dense", []), dtype=torch.float)
    cat = torch.tensor(pad_categorical(profile["categorical"], cat_len), dtype=torch.float)

    cond = torch.zeros(condition_vocab_size)
    for idx in profile["multi_hot"].get("conditions", []):
        cond[idx] = 1.0

    return torch.cat([dense, cat, cond])

def flatten_doctor(profile, condition_vocab_size, cat_len=3, dense_dim=2):
    dense = torch.zeros(dense_dim)
    cat = torch.tensor(pad_categorical(profile["categorical"], cat_len), dtype=torch.float)

    cond = torch.zeros(condition_vocab_size)
    for idx in profile["multi_hot"].get("conditions", []):
        cond[idx] = 1.0

    return torch.cat([dense, cat, cond])

def build_feature_vector(patient, doctor, condition_vocab_size, cat_len=3, dense_dim=2):
    p_vec = flatten_patient(patient, condition_vocab_size, cat_len)
    d_vec = flatten_doctor(doctor, condition_vocab_size, cat_len, dense_dim)
    return torch.cat([p_vec, d_vec]).tolist()