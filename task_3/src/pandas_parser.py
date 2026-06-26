import pandas as pd
import json
import os

def read_csv_pandas(filepath:str):
    if not os.path.exists(filepath):
        raise FileNotFoundError (f"file not found:{filepath}")
    df=pd.read_csv(filepath)
    if df.empty:
        raise ValueError("CSV is empty")
    return df

def calculate_summary_pandas(df) -> dict:
    submitted = df[df["submitted"] == "yes"]
    missing = df[df["submitted"] == "no"]
    high=df.loc[df["score"].idxmax()]
    low=df.loc[df["score"].idxmin()]
    below_5=df[df["score"]<5]["name"].tolist()
    domain_avg=df.groupby("domain")["score"].mean().round(2).to_dict()

    return {
        "total_students": len(df),
        "submitted_count": len(submitted),
        "missing_count": len(missing),
        "average_score": round(df["score"].mean(), 2),
        "highest_scorer": {"name": high["name"], "score": int(high["score"])},
        "lowest_scorer": {"name": low["name"], "score": int(low["score"])},
        "domain_wise_avg": domain_avg,
        "missing_submission": missing["name"].tolist(),
        "students_below_5": below_5
    }
def write_json(data: dict, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    