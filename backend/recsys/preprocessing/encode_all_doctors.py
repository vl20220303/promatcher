from collections import defaultdict
import json
import os
from pathlib import Path

from encode_doctor import encode_doctor_profile, map_specialty_to_conditions

def build_vocab_maps_from_doctors(json_dir, vocab=None):
    if vocab is None:
        vocab = {
            "gender": {},
            "zip": {},
            "conditions": {},
            "specialty": {}
        }

    vocab['specialty'] = {}
    counters = {category: len(vocab[category]) for category in vocab}


    for file in Path(json_dir).glob("*.json"):
        with open(file) as f:
            doc = json.load(f)

        # gender
        gender = doc["basic"].get("sex")
        if gender and gender not in vocab["gender"]:
            counters["gender"] += 1
            vocab["gender"][gender] = counters["gender"]

        # ZIP
        location = next((a for a in doc["addresses"] if a["address_purpose"] == "LOCATION"), None)
        zip_code = location["postal_code"][:5] if location else None
        if zip_code and zip_code not in vocab["zip"]:
            counters["zip"] += 1
            vocab["zip"][zip_code] = counters["zip"]

        # conditions (from specialty mapping)
        specialty_desc = doc["taxonomies"][0]["desc"] if doc["taxonomies"] else ""
        condition_codes = map_specialty_to_conditions(specialty_desc)
        for code in condition_codes:
            if code not in vocab["conditions"]:
                counters["conditions"] += 1
                vocab["conditions"][code] = counters["conditions"]
            
        # specialty
        specialty = doc["taxonomies"][0]["desc"] if doc["taxonomies"] else None
        if specialty and specialty not in vocab["specialty"]:
            counters["specialty"] += 1
            vocab["specialty"][specialty] = counters["specialty"]

    return vocab

def encode_all_doctors(vocab_maps):
    base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    input_dir = Path(base_path / "data/npi/npi-data")
    output_dir = Path(base_path / "data/npi/encoded-doctors")
    output_dir.mkdir(exist_ok=True)

    #encode and save
    for file in input_dir.glob("*.json"):
        encoded = encode_doctor_profile(file, vocab_maps)
        out_path = output_dir / f"{encoded['doctor_id']}.json"
        with open(out_path, "w") as f:
            json.dump(encoded, f)