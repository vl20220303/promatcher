import pandas as pd
import json
import os
from pathlib import Path

base_path = Path(os.path.dirname(os.path.abspath(__file__)))

output_path = Path(base_path / "synthea/processed-data")
output_path.mkdir(exist_ok=True)

base_path = base_path / "synthea/synthea-data/csv"
patients = pd.read_csv(base_path / "patients.csv")

# write initial JSON files with demographics only
for _, row in patients.iterrows():
    pid = row["Id"]
    patient_json = {
        "demographics": row.to_dict(),
        "conditions": [],
        "observations": [],
        "medications": [],
        "procedures": [],
        "encounters": []
    }
    with open(output_path / f"{pid}.json", "w") as f:
        json.dump(patient_json, f)

# function to append data to existing JSON file
def append_to_patient_json(pid, key, record):
    file_path = output_path / f"{pid}.json"
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        data[key].append(record)
        with open(file_path, "w") as f:
            json.dump(data, f)
    except FileNotFoundError:
        pass  # skip if patient file doesn't exist

# stream each large file in chunks
def stream_and_append(file_name, key, chunksize=5000):
    for chunk in pd.read_csv(base_path / file_name, chunksize=chunksize):
        patient_updates = {}

        # accumulate updates per patient
        for _, row in chunk.iterrows():
            pid = row["PATIENT"]
            if pid not in patient_updates:
                patient_updates[pid] = []
            patient_updates[pid].append(row.to_dict())

        # apply updates per patient
        for pid, records in patient_updates.items():
            file_path = output_path / f"{pid}.json"
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                data[key].extend(records)
                with open(file_path, "w") as f:
                    json.dump(data, f)
            except FileNotFoundError:
                pass

        print(f'Reading chunk {chunk}')
        print(f'Reading rows \033[31m{chunk.head(1).index[0]}-{chunk.tail(1).index[0]}\033[37m of \033[33m{file_name}\033[37m')

stream_and_append("conditions.csv", "conditions")
input("\033[31mEnter to continue\033[37m")
stream_and_append("medications.csv", "medications")
input("\033[31mEnter to continue\033[37m")
stream_and_append("procedures.csv", "procedures")
input("\033[31mEnter to continue\033[37m")
stream_and_append("encounters.csv", "encounters")
input("\033[31mEnter to continue\033[37m")
stream_and_append("observations.csv", "observations")