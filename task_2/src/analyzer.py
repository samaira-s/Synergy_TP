import csv
import json
import os
from typing import Any
def read_submissions(filep:str) -> list:
    if not os.path.exists(filep):
        raise FileNotFoundError(f"File not found: {filep}")
    with open(filep, newline="") as f:
        rows=list(csv.DictReader(f))
    if not rows:
        raise ValueError("CSV file is empty.")
    return rows

def get_submitted_students(data: list) ->list:
    return [s for s in data if s["submitted"]=="yes"]

def calculate_average_score(data: list) -> float:
    scores=[float(s["score"])for s in data]
    return round(sum(scores)/len(scores),2)

def get_domain_wise_average(data:list) -> dict:
    domains={}
    for s in data:
        domain=s["domain"]
        score=float(s["score"])
        if domain not in domains:
            domains[domain]=[]
        domains[domain].append(score)
    return {d: round(sum(v)/len(v),2) for d, v in domains.items()}

def get_missing_submissions(data :list)-> list:
    return [s["name"]for s in data if s["submitted"]=="no"]

def write_summary(summary:dict,output_path: str)->None:
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)