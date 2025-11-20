import torch

def flatten_patient(profile, condition_vocab_size):
    cat = torch.cat([torch.tensor(profile["categorical"], dtype=torch.float), torch.zeros(1)])
    dense = torch.tensor(profile.get("dense", []), dtype=torch.float)

    cond = torch.zeros(condition_vocab_size)
    for idx in profile["multi_hot"].get("conditions", []):
        cond[idx-1] = 1.0

    return torch.cat([dense, cat, cond])

def flatten_doctor(profile, condition_vocab_size):
    cat = torch.tensor(profile["categorical"], dtype=torch.float)
    dense = torch.zeros(2)

    cond = torch.zeros(condition_vocab_size)
    for idx in profile["multi_hot"].get("conditions", []):
        cond[idx-1] = 1.0

    return torch.cat([dense, cat, cond])

import torch.nn.functional as F

def compute_similarity(p_vec, d_vec, method="cosine"):
    if method == "cosine":
        return F.cosine_similarity(p_vec.unsqueeze(0), d_vec.unsqueeze(0)).item()
    elif method == "dot":
        return torch.dot(p_vec, d_vec).item()
    else:
        raise ValueError("Unsupported similarity method")
    
def rank_doctors_for_patient(patient, doctors, condition_vocab_size, top_k=5):
    p_vec = flatten_patient(patient, condition_vocab_size)
    scores = []
    for doc in doctors:
        d_vec = flatten_doctor(doc, condition_vocab_size)
        score = compute_similarity(p_vec, d_vec)
        scores.append((doc["doctor_id"], score))

    ranked = sorted(scores, key=lambda x: -x[1])
    return ranked[:top_k]