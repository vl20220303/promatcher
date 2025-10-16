import json
from datetime import datetime

def compute_age(birthdate_str):
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = datetime.today()
    return (today - birthdate).days / 365.25

def encode_patient(json_path, vocab_maps):
    with open(json_path) as f:
        data = json.load(f)

    print(f'Processing patient {json_path}')

    #dense features
    age = compute_age(data["demographics"]["BIRTHDATE"])
    encounter_count = len(data["encounters"])
    dense = [age, encounter_count]

    #categorical
    gender_id = vocab_maps["gender"].get(data["demographics"]["GENDER"], 0)
    zip_id = vocab_maps["zip"].get(data["demographics"]["ZIP"], 0)
    categorical = [gender_id, zip_id]

    #multi-hot
    condition_ids = [vocab_maps["conditions"].get(c["CODE"], 0) for c in data["conditions"]]
    medication_ids = [vocab_maps["medications"].get(m["CODE"], 0) for m in data["medications"]]
    procedure_ids = [vocab_maps["procedures"].get(p["CODE"], 0) for p in data["procedures"]]

    print(f'Finished patient {json_path}')

    return {
        "patient_id": data["demographics"]["Id"],
        "dense": dense,
        "categorical": categorical,
        "multi_hot": {
            "conditions": condition_ids,
            "medications": medication_ids,
            "procedures": procedure_ids
        }
    }