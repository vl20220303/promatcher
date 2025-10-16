import json
import random
from pathlib import Path
import os
    
def select_doctors(arr, start, step, num_entries):
    length = len(arr)
    for i in range(num_entries):
        idx = (start + (i*step))%length
        path = arr[idx]
        with open(path, 'r') as f:
            doctor = json.load(f)
            print(f'{doctor.get('number')}, {doctor['basic'].get('first_name')} {doctor['basic'].get('last_name')}')

base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
input_dir = Path(base_path / "data/npi/npi-data")

doctors = list(input_dir.glob("*.json"))
start = random.randint(0, len(doctors)); step = 15; num_entries = 100
print(f'{start}, {step}, {num_entries} for list of size {len(doctors)}')

select_doctors(doctors, start, step, num_entries)