import sys
sys.path.append("task_2/src")

from analyzer import (
    read_submissions,
    get_submitted_students,
    calculate_average_score,
    get_domain_wise_average,
    get_missing_submissions,
    write_summary
)

def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    data = read_submissions(input_path)
    submitted = get_submitted_students(data)
    missing = get_missing_submissions(data)
    avg_score = calculate_average_score(data)
    domain_avg = get_domain_wise_average(data)

    all_scores = [(s["name"], float(s["score"])) for s in data]
    submitted_scores = [(s["name"], float(s["score"])) for s in submitted]

    highest = max(all_scores, key=lambda x: x[1])
    lowest_submitted = min(submitted_scores, key=lambda x: x[1])
    below_5 = [s["name"] for s in data if float(s["score"]) < 5]

    summary = {
        "total_students": len(data),
        "submitted_count": len(submitted),
        "missing_count": len(missing),
        "average_score": avg_score,
        "highest_scorer": {"name": highest[0], "score": highest[1]},
        "lowest_scorer_submitted": {"name": lowest_submitted[0], "score": lowest_submitted[1]},
        "domain_wise_average": domain_avg,
        "missing_submissions": missing,
        "students_below_5": below_5
    }

    print(f"Total Students     : {summary['total_students']}")
    print(f"Submitted          : {summary['submitted_count']}")
    print(f"Missing            : {summary['missing_count']}")
    print(f"Average Score      : {summary['average_score']}")
    print(f"Highest Scorer     : {highest[0]} ({highest[1]})")
    print(f"Missing Submissions: {missing}")

    write_summary(summary, output_path)
    print(f"Summary written to {output_path}")

if __name__ == "__main__":
    main()