import numpy as np
import pandas as pd

CV_STABLE_MAX = 0.05
CV_MODERATE_MAX = 0.15
def add_rolling_average(df, window=3):
    df = df.sort_values(["domain", "condition", "time_step"]).copy()
    df["rolling_average_signal"] = (
        df.groupby(["domain", "condition"])["signal"]
          .transform(lambda s: s.rolling(window=window, min_periods=1).mean())
    )
    return df

def add_normalized_signal(df):
    df = df.copy()
    valid = df["baseline_signal"].notna() & (df["baseline_signal"] != 0)
    df["normalized_signal"] = np.where(valid, df["signal"] / df["baseline_signal"], np.nan)
    return df

def add_power_feature(df):
    df = df.copy()
    valid = (df["domain"] == "Electronics") & df["voltage_v"].notna() & df["current_a"].notna()
    df["power_w"] = np.where(valid, df["voltage_v"] * df["current_a"], np.nan)
    return df

def add_error_percent(df):
    df = df.copy()
    valid = df["expected_signal"].notna() & (df["expected_signal"] != 0) & df["signal"].notna()
    df["error_percent"] = np.where(
        valid, ((df["signal"] - df["expected_signal"]) / df["expected_signal"]) * 100, np.nan
    )
    return df

def add_stress_ratio(df):
    df = df.copy()
    valid = (
        (df["domain"] == "Mechanical")
        & df["stress_mpa"].notna()
        & df["reference_stress_mpa"].notna()
        & (df["reference_stress_mpa"] != 0)
    )
    df["stress_ratio"] = np.where(valid, df["stress_mpa"] / df["reference_stress_mpa"], np.nan)
    return df

def add_ml_readiness_flag(df):
    df = df.copy()

    base_valid = (
        df["signal"].notna()
        & df["expected_signal"].notna()
        & df["input_value"].notna()
        & df["domain"].notna()
        & df["condition"].notna()
    )

    group_cols = ["domain", "condition", "input_type", "input_value", "input_unit", "signal_unit"]
    group_cv = df.groupby(group_cols)["signal"].transform(
        lambda s: s.std(ddof=1) / s.mean() if len(s.dropna()) >= 2 and s.mean() != 0 else np.nan
    )

    stable_enough = group_cv.abs() <= CV_MODERATE_MAX
    df["ml_ready"] = base_valid & stable_enough.fillna(False)
    return df

def save_engineered_features(df, output_path):
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    import sys
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from replicate_statistics import load_data

    df = load_data(sys.argv[1])
    df = add_rolling_average(df)
    df = add_normalized_signal(df)
    df = add_power_feature(df)
    df = add_error_percent(df)
    df = add_stress_ratio(df)
    df = add_ml_readiness_flag(df)
    print(df.to_string())
