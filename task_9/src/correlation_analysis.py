import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RELATIONSHIPS = [
    ("Biochem: signal vs concentration", "Biochem", "input_value", "signal"),
    ("Electronics: signal vs load", "Electronics", "input_value", "signal"),
    ("Electronics: signal vs temperature", "Electronics", "temperature_c", "signal"),
    ("Mechanical: signal vs load", "Mechanical", "input_value", "signal"),
    ("Mechanical: stress vs load", "Mechanical", "input_value", "stress_mpa"),
]

def calculate_correlations(df):
    rows = []
    for label, domain, xcol, ycol in RELATIONSHIPS:
        sub = df[df["domain"] == domain][[xcol, ycol]].dropna()
        n = len(sub)

        if n >= 2 and sub[xcol].nunique() > 1:
            pearson_r, pearson_p = scipy_stats.pearsonr(sub[xcol], sub[ycol])
            spearman_r, spearman_p = scipy_stats.spearmanr(sub[xcol], sub[ycol])
        else:
            pearson_r = pearson_p = spearman_r = spearman_p = None

        rows.append({
            "relationship": label,
            "domain": domain,
            "x_column": xcol,
            "y_column": ycol,
            "n_samples": n,
            "pearson_r": pearson_r,
            "pearson_p_value": pearson_p,
            "spearman_r": spearman_r,
            "spearman_p_value": spearman_p,
        })
    return pd.DataFrame(rows)

def _linear_fit_metrics(x, y):
    if len(x) < 2:
        return {"slope": None, "intercept": None, "r_squared": None, "mae": None, "rmse": None}

    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept
    residuals = y - y_pred

    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else None

    mae = np.mean(np.abs(residuals))
    rmse = np.sqrt(np.mean(residuals ** 2))

    return {"slope": slope, "intercept": intercept, "r_squared": r_squared, "mae": mae, "rmse": rmse}

def fit_calibration_line(df):
    rows = []
    for label, domain, xcol, ycol in RELATIONSHIPS:
        sub = df[df["domain"] == domain][[xcol, ycol]].dropna()
        x = sub[xcol].to_numpy(dtype=float)
        y = sub[ycol].to_numpy(dtype=float)
        metrics = _linear_fit_metrics(x, y)
        rows.append({"relationship": label, "domain": domain, "x_column": xcol, "y_column": ycol,
                      "n_samples": len(sub), **metrics})
    return pd.DataFrame(rows)

def calculate_fit_metrics(df):
    corr_df = calculate_correlations(df)
    fit_df = fit_calibration_line(df)

    merged = corr_df.merge(
        fit_df.drop(columns=["domain", "x_column", "y_column", "n_samples"]),
        on="relationship", how="left"
    )
    return merged

def plot_calibration_curve(summary_df, domain, output_path):
    sub = summary_df[summary_df["domain"] == domain].sort_values("input_value")
    if sub.empty:
        return

    x = sub["input_value"].to_numpy(dtype=float)
    y = sub["mean_signal"].to_numpy(dtype=float)

    lower = sub["confidence_interval_lower"].to_numpy(dtype=float)
    upper = sub["confidence_interval_upper"].to_numpy(dtype=float)
    yerr_lower = y - lower
    yerr_upper = upper - y
    yerr = np.vstack([yerr_lower, yerr_upper])
    yerr = np.nan_to_num(yerr, nan=0.0)

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ax.errorbar(x, y, yerr=yerr, fmt="o-", color="#4C72B0", ecolor="#DD8452",
                capsize=4, markersize=6, linewidth=1.5)
    ax.set_xlabel(f"Input value ({sub['input_unit'].iloc[0]})")
    ax.set_ylabel(f"Mean signal ({sub['signal_unit'].iloc[0]})")
    ax.set_title(f"{domain} Calibration Curve (mean signal ± 95% CI)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=130)
    plt.close(fig)

def plot_signal_input_scatter(df, output_path):
    fig, ax = plt.subplots(figsize=(6.5, 5))
    colors = {"Biochem": "#55A868", "Electronics": "#4C72B0", "Mechanical": "#C44E52"}
    for domain, group in df.groupby("domain"):
        ax.scatter(group["input_value"], group["signal"], label=domain,
                   color=colors.get(domain, "gray"), alpha=0.8, s=35)
    ax.set_xlabel("Input value (domain-specific unit)")
    ax.set_ylabel("Raw signal (domain-specific unit)")
    ax.set_title("Raw Signal vs Input Value (all domains)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=130)
    plt.close(fig)

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from replicate_statistics import load_data
    df = load_data(sys.argv[1])
    print(calculate_fit_metrics(df).to_string())