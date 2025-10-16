from collections import defaultdict
import json

def map_specialty_to_conditions(specialty_desc):
    specialty_to_icd10 = {
        "Family Practice": ["E11", "J45", "F41"],         # Diabetes, Asthma, Anxiety
        "Gastroenterology": ["K21", "K50", "K52"],        # GERD, Crohn’s Disease, IBS
        "Cardiology": ["I10", "I25", "I48"],              # Hypertension, CAD, Atrial Fibrillation
        "Psychiatry": ["F32", "F41", "F20"],              # Depression, Anxiety, Schizophrenia
        "Endocrinology": ["E03", "E11", "E66"],           # Hypothyroidism, Diabetes, Obesity
        "Pulmonology": ["J44", "J45", "R06"],             # COPD, Asthma, Dyspnea
        "Neurology": ["G40", "G43", "G20"],               # Epilepsy, Migraine, Parkinson’s Disease
        "Dermatology": ["L40", "L20", "B35"],             # Psoriasis, Eczema, Ringworm
        "Pediatrics": ["J00", "R50", "B34"],              # Common Cold, Fever, Viral Infections
        "Orthopedics": ["M16", "M17", "M54"],             # Hip/Knee Osteoarthritis, Back Pain
        "OB/GYN": ["N80", "O09", "Z34"],                  # Endometriosis, Pregnancy, Prenatal Care
        "Urology": ["N40", "N39", "R31"],                 # BPH, Urinary Incontinence, Hematuria
        "Oncology": ["C50", "C61", "C34"],                # Breast, Prostate, Lung Cancer
        "Nephrology": ["N18", "N19", "R80"],              # CKD, Renal Failure, Proteinuria
        "Infectious Disease": ["A09", "B20", "J09"],      # Diarrhea, HIV, Influenza
    }
    out = []
    for key in specialty_to_icd10:
        if key in str(specialty_desc):
            out.extend(specialty_to_icd10[key])
    return out

def encode_doctor_profile(doc_path, vocab_maps):
    with open(doc_path) as f:
        doc = json.load(f)

    # unique ID
    doctor_id = doc.get("number")
    print(f'Processing {doctor_id}')

    # categorical features
    gender_id = vocab_maps["gender"].get(doc["basic"].get("sex", ""), 0)
    specialty_desc = doc["taxonomies"][0]["desc"] if doc["taxonomies"] else ""
    specialty_id = vocab_maps["specialty"].get(specialty_desc, 0)

    # ZIP code from LOCATION address
    location = next((a for a in doc["addresses"] if a["address_purpose"] == "LOCATION"), None)
    zip_code = location["postal_code"][:5] if location else ""
    zip_id = vocab_maps["zip"].get(zip_code, 0)

    # multi-hot: accepted conditions (optional mapping from specialty)
    accepted_conditions = map_specialty_to_conditions(specialty_desc)
    accepted_ids = [vocab_maps["conditions"].get(c, 0) for c in accepted_conditions]
    
    print(f'Finished {doctor_id}')

    return {
        "doctor_id": doctor_id,
        "categorical": [gender_id, specialty_id, zip_id],
        "multi_hot": {
            "conditions": accepted_ids
        }
    }