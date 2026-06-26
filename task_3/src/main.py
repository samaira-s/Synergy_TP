import sys
import os
sys.path.append("task_3/src")

from manual_parser import read_csv_manual, convert_types, calculate_summary, write_json
from pandas_parser import read_csv_pandas, calculate_summary_pandas

def write_comparison_report(manual: dict, pandas: dict, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    match = manual == pandas
    with open(output_path, "w") as f:
        f.write("# Comparison Report\n\n")
        f.write(f"## Do both outputs match? {'Yes' if match else 'No'}\n\n")
        f.write("## Manual Summary\n")
        for k, v in manual.items():
            f.write(f"- {k}: {v}\n")
        f.write("\n## Pandas Summary\n")
        for k, v in pandas.items():
            f.write(f"- {k}: {v}\n")
        if not match:
            f.write("\n## Differences\n")
            for k in manual:
                if manual[k] != pandas[k]:
                    f.write(f"- {k}: manual={manual[k]}, pandas={pandas[k]}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python task_3/src/main.py task_3/data/submissions.csv")
        sys.exit(1)

    file_path = sys.argv[1]

    # Manual parser
    rows = read_csv_manual(file_path)
    rows = convert_types(rows)
    manual_summary = calculate_summary(rows)
    write_json(manual_summary, "task_3/output/manual_summary.json")
    print("Manual summary written.")

    # Pandas parser
    df = read_csv_pandas(file_path)
    pandas_summary = calculate_summary_pandas(df)
    write_json(pandas_summary, "task_3/output/pandas_summary.json")
    print("Pandas summary written.")

    # Comparison report
    write_comparison_report(manual_summary, pandas_summary, "task_3/output/comparison_report.md")
    print("Comparison report written.")

if __name__ == "__main__":
    main()