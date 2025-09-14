import os
from pathlib import Path
import json
from build_vocab_maps import build_vocab_maps
from encode_patient import encode_patient

base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

input_dir = Path(base_path / "data/synthea/processed-data")
output_dir = Path(base_path / "data/synthea/encoded-patients")
output_dir.mkdir(exist_ok=True)

#build vocab maps
vocab_maps = build_vocab_maps(input_dir)

#encode and save
for file in input_dir.glob("*.json"):
    encoded = encode_patient(file, vocab_maps)
    out_path = output_dir / f"{encoded['patient_id']}.json"
    with open(out_path, "w") as f:
        json.dump(encoded, f)