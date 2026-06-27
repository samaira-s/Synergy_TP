import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os 

def load_cleaned_data(filepath:str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"file is not found {filepath}")
    return pd.read_csv(filepath)

def plot_domain_average_score(df,outputpath:str)->None:
    domain_avg=df.groupby("domain")["score"].mean()
    plt.figure(figsize=(8,5))
    plt.bar(domain_avg.index,domain_avg.values,color="blue")
    plt.title("Average Score by Domain")
    plt.xlabel("Domain")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig(outputpath)
    plt.close()

def plot_attendance_vs_score(df, outputpath: str) -> None:
    plt.figure(figsize=(8,5))
    plt.scatter(df["attendance_percent"],df["score"],color="blue")
    plt.title("Attendance vs Score")
    plt.xlabel("Attendance Percent")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig(outputpath)
    plt.close()

def plot_submission_status_count(df, output_path: str) -> None:
    count=df["submitted"].value_counts()
    plt.figure(figsize=(8,5))
    plt.bar(count.index,count.values,color="blue") 
    plt.title("Submission Status Count")
    plt.xlabel("Submitted")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def write_plot_summary(outputpath: str) -> None:
    os.makedirs(os.path.dirname(outputpath),exist_ok=True)
    with open(outputpath,"w") as f:
        f.write("#Plot summary\n\n")
        f.write("##1.Average score for each domain ")
        f.write("this bar chart shows average score for each domain .ml and electronics tend to score higher than web and mechanical.\n\n")
        f.write("##Relationship between attendance percent and score\n")
        f.write("this scatter plot shows the relationship between attendance percentage and score.Students withhigher attendance usually score better.\n\n")
        f.write("##Count of submitted and non submitted students\n")
        f.write("this bar chart shows how many student submitted v/s not submitted.most students submitted their work\n\n")