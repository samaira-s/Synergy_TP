import json
import os

def read_csv_manual(filepath: str)->list:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"file not found:{filepath}")
    rows=[]
    with open(filepath,"r") as f:
        lines=f.readlines()
    if not lines:
        raise ValueError("CSV  file is empty")
    header=lines[0].strip().split(",")

    for line in lines[1:]:
        line=line.strip()
        if not line:
            continue
        values=line.split(",")
        if len(values)!=len(header):
            continue
        row={}
        for i in range(len(header)):
            row[header[i]]=values[i]
            rows.append(row)
    return rows


def convert_types(rows: list)-> list:   #list of dict
    for row in rows:
        row["score"]=int(row["score"])
        row["submitted"]=row["submitted"].strip().lower()
    return rows

def calculate_summary(rows:list)->dict:
    sub=[r for r in rows if r["submitted"]=="yes"]
    miss=[r for r in rows if r["submitted"]=="no"]
    score=[r["score"] for r in rows ]
    sub_score=[r["score"] for r in sub ]

    high_s=max(rows,key =lambda x:x["score"])
    low_s=min(rows,key=lambda x:x["score"])
    below_5=[r["name"]for r in rows if r["score"]<5]

    domains={}
    for r in rows:
        d=r["domain"]
        if d not in domains:
            domains[d]=[]
        domains[d].append(r["score"])
    domains_avg={d:round(sum(v)/len(v),2)for d,v in domains.items()}

    return {
        "total_students": len(rows),
        "submitted_count": len(sub),
        "missing_count": len(miss),
        "average_score": round(sum(score)/len(score),2),
        "highest_scorer": {"name":high_s["name"],"score": high_s["score"]},
        "lowest_scorer": {"name": low_s["name"],"score":low_s["score"]},
        "domain_wise_avg": domains_avg,
        "missing_submission": [r["name"] for r in miss],
        "students_below_5": below_5
    }

def write_json(data: dict,output_path:str)->None:
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    with open(output_path,"w") as f:    #with automatically closes the file when we're done
        json.dump(data,f,indent=2)