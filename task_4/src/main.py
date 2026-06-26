import sys
import os
sys.path.append("task_4/src")

import json
import pandas as pd
from clean_data import (
    load_data, generate_summary, remove_duplicates,
    standardize_domains, clean_attendance, clean_scores,
    clean_study_hours, clean_height, clean_weight,
    clean_submitted, handle_missing_values, save_cleaned_data
)
from validate_data import validate_cleaned_data

def write_report(report_path: str) -> None:
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write("# Data Cleaning Report\n\n")
        f.write("## 1. Duplicates\n")
        f.write("Removed duplicate row for S005 (Rohan) which appeared twice.\n\n")
        f.write("## 2. Domain Standardization\n")
        f.write("Mapped all variations to: ML, Web, Electronics, Mechanical.\n\n")
        f.write("## 3. Attendance\n")
        f.write("Removed % signs. Set -10 and 105% to None (invalid). Filled with median.\n\n")
        f.write("## 4. Score\n")
        f.write("Converted word 'nine' to 9. Missing values filled with median.\n\n")
        f.write("## 5. Study Hours\n")
        f.write("Converted word 'two' to 2. Missing values filled with median.\n\n")
        f.write("## 6. Height\n")
        f.write("Converted all values to cm. 1.62 m became 162.0 cm.\n\n")
        f.write("## 7. Weight\n")
        f.write("Removed kg units and converted to float.\n\n")
        f.write("## 8. Submitted\n")
        f.write("Mapped Y/Yes/N/No to consistent yes/no values.\n\n")
        f.write("## 9. Missing Values\n")
        f.write("Numeric columns filled with median. Submitted filled with 'no'.\n\n")

def write_json(data: dict, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)

def main():
    if len(sys.argv) != 3:
        print("Usage: python task_4/src/main.py task_4/data/messy_students.csv task_4/output/cleaned_students.csv")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    df = load_data(input_path)
    summary_before = generate_summary(df)
    write_json(summary_before, "task_4/output/summary_before.json")
    print("Before summary written.")

    df = remove_duplicates(df)
    df = standardize_domains(df)
    df = clean_attendance(df)
    df = clean_scores(df)
    df = clean_study_hours(df)
    df = clean_height(df)
    df = clean_weight(df)
    df = clean_submitted(df)
    df = handle_missing_values(df)

    summary_after = generate_summary(df)
    write_json(summary_after, "task_4/output/summary_after.json")
    print("After summary written.")

    save_cleaned_data(df, output_path)
    print(f"Cleaned data saved to {output_path}")
   
    validate_cleaned_data(df)

    write_report("task_4/output/cleaning_report.md")
    print("Cleaning report written.")

if __name__ == "__main__":
    main()