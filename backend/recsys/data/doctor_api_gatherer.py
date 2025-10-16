import json
import requests
from pathlib import Path
import os

base_path = Path(os.path.dirname(os.path.abspath(__file__)))

output_path = Path(base_path / "npi/npi-data")
output_path.mkdir(exist_ok=True)

def gather_doctors(zip, limit=50):
    new_chunk={'results' : []}; n=0
    while (len(new_chunk['results']) > 0 or n==0) and n < limit:
        url = f"https://npiregistry.cms.hhs.gov/api/?number=&enumeration_type=NPI-1&taxonomy_description=&name_purpose=&first_name=&use_first_name_alias=&last_name=&organization_name=&address_purpose=&city=&state=&postal_code={zip}*&country_code=US&limit=200&skip={n*200}&pretty=&version=2.1"
        print(f'Accessing chunk {n} of zips {zip}*...')
        new_chunk = requests.get(url).json()
        print(f'Got chunk {n} of zips {zip}*, contains {new_chunk['result_count']} results.')

        for entry in new_chunk['results']:
            entry_number = entry['number']
            with open(output_path / f'{entry_number}.json', 'w') as f:
                json.dump(entry, f)

        n+=1
    
def gather_all_zips():
    for i in range(10):
        for j in range(10):
            gather_doctors(i*10 + j)

gather_doctors(94, 2)