import json
from pathlib import Path
from collections import defaultdict

def build_vocab_maps(json_dir):
    vocab = {
        "gender": {},
        "zip": {},
        "conditions": {},
        "medications": {},
        "procedures": {}
    }

    counters = defaultdict(int)

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