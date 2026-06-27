# Task 5: Matplotlib Visualization

## Objective
Generate three properly labeled plots from the cleaned dataset produced in Task 4.

## Folder Structure
Synergy_TP/
  task_5/
    README.md
    output/
      domain_average_score.png
      attendance_vs_score.png
      submission_status_count.png
      plot_summary.md
    src/
      visualize.py
      main.py
## Required Packages
pandas,matplotlib
## Setup Instructions
```bash
source venv/Scripts/activate
pip install -r task_1/requirements.txt
```

## Run Command
```bash
python task_5/src/main.py task_4/output/cleaned_students.csv task_5/output
```

## Expected Output Files
- task_5/output/domain_average_score.png
- task_5/output/attendance_vs_score.png
- task_5/output/submission_status_count.png
- task_5/output/plot_summary.md

## Logic Explanation
- visualize.py contains all plotting functions using matplotlib
- main.py loads the cleaned CSV from Task 4 and saves all three plots as PNG files
- All plots have titles, axis labels, and are saved using savefig()
