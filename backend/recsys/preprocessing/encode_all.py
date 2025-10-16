import json
import os
from pathlib import Path
from encode_all_doctors import build_vocab_maps_from_doctors, encode_all_doctors
from encode_all_patients import build_vocab_maps, encode_all_patients

base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

patient_dir = Path(base_path / "data/synthea/processed-data")
doctor_dir = Path(base_path / "data/npi/npi-data")

vocab_maps = build_vocab_maps(patient_dir)
vocab_maps = build_vocab_maps_from_doctors(doctor_dir, vocab_maps)

out_path = base_path / "data" / "vocab_maps.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(vocab_maps, f, indent=2, ensure_ascii=False, default=str)

encode_all_patients(vocab_maps)
encode_all_doctors(vocab_maps)