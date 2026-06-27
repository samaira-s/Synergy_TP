# Task 3: Manual CSV Parser and Pandas Comparison

## Objective
Build a CSV parser manually using Python file I/O, then repeat the same analysis using pandas to understand how raw CSV text becomes structured Python data.

## Folder Structure
Synergy_TP/
  task_3/
    README.md
    data/
      submissions.csv
    output/
      manual_summary.json
      pandas_summary.json
      comparison_report.md
    src/
      manual_parser.py
      pandas_parser.py
      main.py
Synergy_TP/
  task_3/
    README.md
    data/
      submissions.csv
    output/
      manual_summary.json
      pandas_summary.json
      comparison_report.md
    src/
      manual_parser.py
      pandas_parser.py
      main.py
## Setup Instructions
```bash
source venv/Scripts/activate
pip install -r task_1/requirements.txt
```

## Run Command
```bash
python task_3/src/main.py task_3/data/submissions.csv
```

## Expected Output Files
- task_3/output/manual_summary.json
- task_3/output/pandas_summary.json
- task_3/output/comparison_report.md

## Logic Explanation
- manual_parser.py reads the CSV using only open() and string splitting — no pandas or csv module
- pandas_parser.py reads the same CSV using pd.read_csv()
- Both calculate the same summary statistics
- main.py runs both and writes a comparison report showing whether outputs match