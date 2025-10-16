import os
from pathlib import Path
import json
from encode_patient import encode_patient

from collections import defaultdict

def build_vocab_maps(json_dir, vocab=None):
    if vocab is None:
        vocab = {
            "gender": {},
            "zip": {},
            "conditions": {},
            "medications": {},
            "procedures": {}
        }

    counters = {category: len(vocab[category]) for category in vocab}

    for file in Path(json_dir).glob("*.json"):
        with open(file) as f:
            data = json.load(f)

        #gender
        gender = data["demographics"].get("GENDER")
        if gender and gender not in vocab["gender"]:
            counters["gender"] += 1
            vocab["gender"][gender] = counters["gender"]

        #zip
        zip_code = data["demographics"].get("ZIP")
        if zip_code and zip_code not in vocab["zip"]:
            counters["zip"] += 1
            vocab["zip"][zip_code] = counters["zip"]

        #conditions
        for c in data["conditions"]:
            code = c.get("CODE")
            if code and code not in vocab["conditions"]:
                counters["conditions"] += 1
                vocab["conditions"][code] = counters["conditions"]

        #medications
        for m in data["medications"]:
            code = m.get("CODE")
            if code and code not in vocab["medications"]:
                counters["medications"] += 1
                vocab["medications"][code] = counters["medications"]

        #procdeures
        for p in data["procedures"]:
            code = p.get("CODE")
            if code and code not in vocab["procedures"]:
                counters["procedures"] += 1
                vocab["procedures"][code] = counters["procedures"]

    return vocab

def encode_all_patients(vocab_maps):
    base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    input_dir = Path(base_path / "data/synthea/processed-data")
    output_dir = Path(base_path / "data/synthea/encoded-patients")
    output_dir.mkdir(exist_ok=True)

    #encode and save
    for file in input_dir.glob("*.json"):
        encoded = encode_patient(file, vocab_maps)
        out_path = output_dir / f"{encoded['patient_id']}.json"
        with open(out_path, "w") as f:
            json.dump(encoded, f)