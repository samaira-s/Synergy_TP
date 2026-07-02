# Task 4: Messy CSV Cleaning

## Objective
Clean a messy CSV dataset using pandas and produce a clean dataset, validation checks, and a written cleaning report.

## Folder Structure
```
Synergy_TP/
  task_4/
    README.md
    data/
      messy_students.csv
    output/
      cleaned_students.csv
      cleaning_report.md
      summary_before.json
      summary_after.json
    src/
      clean_data.py
      validate_data.py
      main.py
```
## Required Packages
pandas
## Setup Instructions
```bash
source venv/Scripts/activate
pip install -r task_1/requirements.txt
```

## Run Command
```bash
python task_4/src/main.py task_4/data/messy_students.csv task_4/output/cleaned_students.csv
```

## Expected Output Files
- task_4/output/cleaned_students.csv
- task_4/output/summary_before.json
- task_4/output/summary_after.json
- task_4/output/cleaning_report.md

## Logic Explanation
- clean_data.py handles all cleaning steps: removing duplicates, standardizing domains, converting units, handling missing values
- validate_data.py runs validation checks on the cleaned data to ensure correctness
- main.py ties everything together, generates before/after summaries and writes the cleaning report

## Cleaning Report
The full cleaning report is available at:
task_4/output/cleaning_report.md