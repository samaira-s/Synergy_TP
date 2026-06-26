def validate_cleaned_data(df) -> bool:
    valid = True

    # No duplicate student IDs
    if df["student_id"].duplicated().any():
        print("Validation failed: duplicate student IDs found")
        valid = False

    # Attendance between 0 and 100
    if not df["attendance_percent"].between(0, 100).all():
        print("Validation failed: attendance_percent out of range")
        valid = False

    # Score is numeric
    if not df["score"].dtype in ["float64", "int64"]:
        print("Validation failed: score is not numeric")
        valid = False

    # Study hours is numeric
    if not df["study_hours"].dtype in ["float64", "int64"]:
        print("Validation failed: study_hours is not numeric")
        valid = False

    # Height is numeric
    if not df["height_cm"].dtype in ["float64", "int64"]:
        print("Validation failed: height_cm is not numeric")
        valid = False

    # Weight is numeric
    if not df["weight_kg"].dtype in ["float64", "int64"]:
        print("Validation failed: weight_kg is not numeric")
        valid = False

    # Submitted only contains yes/no
    valid_submitted = {"yes", "no"}
    if not set(df["submitted"].unique()).issubset(valid_submitted):
        print("Validation failed: submitted contains invalid values")
        valid = False

    # Domain only contains valid values
    valid_domains = {"ML", "Web", "Electronics", "Mechanical"}
    if not set(df["domain"].unique()).issubset(valid_domains):
        print("Validation failed: domain contains invalid values")
        valid = False

    # No missing values in critical columns
    critical = ["student_id", "name", "domain", "score", "submitted"]
    for col in critical:
        if df[col].isnull().any():
            print(f"Validation failed: missing values in {col}")
            valid = False

    if valid:
        print("All validation checks passed!")

    return valid