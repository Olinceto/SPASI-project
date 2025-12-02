import json
import hashlib
import re

INPUT = "registеr.json"
OUTPUT = "register_anonymized.json"

#Name hashing
def hash_name(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()

#Masking the expert solution number
def mask_decision_number(text: str) -> str:
    match = re.match(r"\s*(\d+)", text)
    if not match:
        return text

    num = match.group(1)
    
    masked = num[0] + "*" * (len(num) - 1)

    return text.replace(num, masked, 1)


#Generalization
def generalize_location(place: str) -> str:
    return "Община Бобошево"

def process():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    header = data[0]
    out = [header]

    idx_name = header.index("Имена на лицето")
    idx_place = header.index("Населено място")
    idx_decision = header.index("№ и дата на експертно решение")

    for row in data[1:]:
        new = row.copy()

        new[idx_name] = hash_name(new[idx_name])

        new[idx_decision] = mask_decision_number(new[idx_decision])

        new[idx_place] = generalize_location(new[idx_place])

        out.append(new)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

process()