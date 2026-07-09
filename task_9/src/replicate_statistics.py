import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

GROUP_COLS = ["domain", "condition", "input_type", "input_value", "input_unit", "signal_unit"]

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def calculate_confidence_interval(mean, std, n):
    if n < 2 or std is None or pd.isna(std):
        return (None, None)

    dof = n - 1
    se = std / np.sqrt(n)
    t_crit = scipy_stats.t.ppf(0.975, dof)
    margin = t_crit * se
    return (mean - margin, mean + margin)

def assign_stability_flag(coefficient_of_variation):
    if coefficient_of_variation is None or pd.isna(coefficient_of_variation):
        return "unreliable"
    cv = abs(coefficient_of_variation)
    if cv <= 0.05:
        return "stable"
    elif cv <= 0.15:
        return "moderate"
    else:
        return "unstable"
    
def calculate_replicate_statistics(df):
    records = []

    for group_key, group_df in df.groupby(GROUP_COLS, dropna=False):
        signals = group_df["signal"].dropna()
        n = len(signals)
        mean_signal = signals.mean() if n > 0 else None
        median_signal = signals.median() if n > 0 else None
        min_signal = signals.min() if n > 0 else None
        max_signal = signals.max() if n > 0 else None

        if n >= 2:
            variance_signal = signals.var(ddof=1)
            std_signal = signals.std(ddof=1)
            se_signal = std_signal / np.sqrt(n)
            ci_lower, ci_upper = calculate_confidence_interval(mean_signal, std_signal, n)
            cv = std_signal / mean_signal if mean_signal not in (0, None) else None
        else:
            variance_signal = None
            std_signal = None
            se_signal = None
            ci_lower, ci_upper = None, None
            cv = None

        stability_flag = assign_stability_flag(cv)
        record = dict(zip(GROUP_COLS, group_key))
        record.update({
            "replicate_count": n,
            "mean_signal": mean_signal,
            "median_signal": median_signal,
            "variance_signal": variance_signal,
            "standard_deviation_signal": std_signal,
            "standard_error_signal": se_signal,
            "confidence_interval_lower": ci_lower,
            "confidence_interval_upper": ci_upper,
            "coefficient_of_variation": cv,
            "minimum_signal": min_signal,
            "maximum_signal": max_signal,
            "stability_flag": stability_flag,
        })
        records.append(record)
    summary_df = pd.DataFrame(records)
    return summary_df
def save_replicate_summary(summary_df, output_path):
    summary_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    import sys
    df = load_data(sys.argv[1])
    summary = calculate_replicate_statistics(df)
    print(summary.to_string())