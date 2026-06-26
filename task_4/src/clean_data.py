import pandas as pd
import json
import os
import re

def load_data(filepath:str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"file not found {filepath}")
    return pd.read_csv(filepath)
def generate_summary(df)->dict:
    return {"total_rows":len(df),
            "missing_values":df.isnull().sum().to_dict(),
            "duplicates":int(df.duplicated().sum()),
            "dtypes":df.dtypes.astype(str).to_dict()
            }

def remove_duplicates(df):
    return df.drop_duplicates()

def standardize_domains(df):
     mapping = {
        "ml": "ML", "ML": "ML", "MACHINE LEARNING": "ML",
        "web": "Web", "Web Dev": "Web", "web development": "Web",
        "electronics": "Electronics", "Electronics": "Electronics",
        "Mechanical": "Mechanical"
    }
     df["domain"] = df["domain"].map(mapping).fillna(df["domain"])
     return df
def clean_attendance(df):
    df["attendance_percent"] = df["attendance_percent"].astype(str).str.replace("%", "", regex=False)
    df["attendance_percent"] = pd.to_numeric(df["attendance_percent"], errors="coerce")
    df.loc[df["attendance_percent"] < 0, "attendance_percent"] = None
    df.loc[df["attendance_percent"] > 100, "attendance_percent"] = None
    df["attendance_percent"] = df["attendance_percent"].fillna(df["attendance_percent"].median())
    return df

def clean_scores(df):
    word_to_num = {"nine": 9, "two": 2, "one": 1, "zero": 0}
    df["score"] = df["score"].astype(str).str.lower().map(
        lambda x: word_to_num.get(x, x) # for each value, check if it's in the dictionary. If yes replace it, if no keep it as is
    )
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["score"] = df["score"].fillna(df["score"].median())
    return df

def clean_study_hours(df):
    word_to_num = {"two": 2, "one": 1, "zero": 0, "three": 3}
    df["study_hours"] = df["study_hours"].astype(str).str.lower().map(
        lambda x: word_to_num.get(x, x)
    )
    df["study_hours"] = pd.to_numeric(df["study_hours"], errors="coerce")
    df["study_hours"] = df["study_hours"].fillna(df["study_hours"].median())
    return df

def clean_height(df):
    def convert_height(val):
        val = str(val).strip().lower()
        if "cm" in val:
            return float(val.replace("cm", "").strip())
        elif "m" in val:
            return float(val.replace("m", "").strip()) * 100
        return None
    df["height_cm"] = df["height"].apply(convert_height)
    df = df.drop(columns=["height"])
    return df

def clean_weight(df):
    def convert_weight(val):
        val = str(val).strip().lower().replace("kg", "").replace(" ", "")
        try:
            return float(val)
        except:
            return None
    df["weight_kg"] = df["weight"].apply(convert_weight)
    df = df.drop(columns=["weight"])
    return df

def clean_submitted(df):
    mapping = {"yes": "yes", "y": "yes", "no": "no", "n": "no"}
    df["submitted"] = df["submitted"].astype(str).str.lower().map(mapping)
    return df

def handle_missing_values(df):
    df["attendance_percent"] = df["attendance_percent"].fillna(df["attendance_percent"].median())
    df["score"] = df["score"].fillna(df["score"].median())
    df["study_hours"] = df["study_hours"].fillna(df["study_hours"].median())
    df["height_cm"] = df["height_cm"].fillna(df["height_cm"].median())
    df["weight_kg"] = df["weight_kg"].fillna(df["weight_kg"].median())
    df["submitted"] = df["submitted"].fillna("no")
    return df

def save_cleaned_data(df, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)