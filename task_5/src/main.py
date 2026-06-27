import sys
import os
sys.path.append("task_5/src")

from visualize import (load_cleaned_data,
    plot_domain_average_score,
    plot_attendance_vs_score,
    plot_submission_status_count,
    write_plot_summary)

def main():
    if len(sys.argv)!=3:
        print("Usage: python task_5/src/main.py task_4/output/cleaned_students.csv task_5/output")
        sys.exit(1)
    inputp=sys.argv[1]
    outputp=sys.argv[2]
    os.makedirs(outputp,exist_ok=True)
    df=load_cleaned_data(inputp)
    plot_domain_average_score(df,os.path.join(outputp,"domain_average_score.png"))
    print("domain_average_score.png saved.")
    plot_attendance_vs_score(df,os.path.join(outputp,"attendance_vs_score.png"))
    print("attendance_vs_score.png saved.")
    plot_submission_status_count(df,os.path.join(outputp,"submission_status_count.png"))
    print("submission_status_count.png saved.")
    write_plot_summary(os.path.join(outputp,"plot_summary.md"))
    print("plot_summary.md saved.")

if __name__=="__main__":
    main()