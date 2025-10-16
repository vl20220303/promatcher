import torch

def flatten_patient(profile, condition_vocab_size):
    cat = torch.tensor(profile["categorical"], dtype=torch.float)
    dense = torch.tensor(profile.get("dense", []), dtype=torch.float)

    cond = torch.zeros(condition_vocab_size)
    for idx in profile["multi_hot"].get("conditions", []):
        cond[idx] = 1.0

    return torch.cat([dense, cat, cond])

def flatten_doctor(profile, condition_vocab_size, specialty_map=None, reverse_vocab=None):
    cat = torch.tensor(profile["categorical"], dtype=torch.float)

    accepted = profile["multi_hot"].get("conditions", [])
    if not accepted and specialty_map and reverse_vocab:
        specialty_id = profile["categorical"][1]
        specialty_name = reverse_vocab["specialty"].get(specialty_id, "")
        accepted = specialty_map.get(specialty_name, [])

    cond = torch.zeros(condition_vocab_size)
    for idx in accepted:
        cond[idx] = 1.0

    return torch.cat([cat, cond])

import torch.nn.functional as F

def compute_similarity(p_vec, d_vec, method="cosine"):
    if method == "cosine":
        return F.cosine_similarity(p_vec.unsqueeze(0), d_vec.unsqueeze(0)).item()
    elif method == "dot":
        return torch.dot(p_vec, d_vec).item()
    else:
        raise ValueError("Unsupported similarity method")
    
def rank_doctors_for_patient(patient, doctors, condition_vocab_size, specialty_map=None, reverse_vocab=None, top_k=5):
    p_vec = flatten_patient(patient, condition_vocab_size)
    scores = []
    for doc in doctors:
        d_vec = flatten_doctor(doc, condition_vocab_size, specialty_map, reverse_vocab)
        score = compute_similarity(p_vec, d_vec)
        scores.append((doc["doctor_id"], score))

    ranked = sorted(scores, key=lambda x: -x[1])
    return ranked[:top_k]