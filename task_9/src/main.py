import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd

from replicate_statistics import (
    load_data, calculate_replicate_statistics, save_replicate_summary,
)
from correlation_analysis import (
    calculate_fit_metrics, plot_calibration_curve, plot_signal_input_scatter,
)
from feature_engineering import (
    add_rolling_average, add_normalized_signal, add_power_feature,
    add_error_percent, add_stress_ratio, add_ml_readiness_flag,
    save_engineered_features,
)

def run_pipeline(input_csv, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    df = load_data(input_csv)
    replicate_summary = calculate_replicate_statistics(df)
    save_replicate_summary(replicate_summary, os.path.join(output_dir, "replicate_summary.csv"))

    #  Part 2: Calibration + correlation 
    correlation_summary = calculate_fit_metrics(df)
    correlation_summary.to_csv(os.path.join(output_dir, "correlation_summary.csv"), index=False)
    # calibration_summary.csv reuses the replicate summary -- it's literally the
    # same mean/CI-per-group table the calibration curve is built from
    replicate_summary.to_csv(os.path.join(output_dir, "calibration_summary.csv"), index=False)

    for domain in ["Biochem", "Electronics", "Mechanical"]:
        plot_calibration_curve(
            replicate_summary, domain,
            os.path.join(output_dir, f"calibration_curve_{domain.lower()}.png")
        )
    plot_signal_input_scatter(df, os.path.join(output_dir, "correlation_signal_input.png"))
# Part 3: Feature engineering 
    feat_df = df.copy()
    feat_df = add_rolling_average(feat_df)
    feat_df = add_normalized_signal(feat_df)
    feat_df = add_power_feature(feat_df)
    feat_df = add_error_percent(feat_df)
    feat_df = add_stress_ratio(feat_df)
    feat_df = add_ml_readiness_flag(feat_df)
    save_engineered_features(feat_df, os.path.join(output_dir, "engineered_features.csv"))

    ml_ready_df = feat_df[feat_df["ml_ready"] == True].copy()
    ml_ready_df.to_csv(os.path.join(output_dir, "ml_ready_dataset.csv"), index=False)

    write_replicate_analysis(replicate_summary, output_dir)
    write_correlation_limitations(correlation_summary, output_dir)
    write_feature_dictionary(output_dir)
    write_feature_summary(feat_df, output_dir)

    print(f"Pipeline complete. Outputs written to: {output_dir}")
def fmt(x, nd=4):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "N/A"
    return f"{x:.{nd}f}"


def write_replicate_analysis(summary, output_dir):
    valid = summary.dropna(subset=["coefficient_of_variation"])
    most_stable = valid.loc[valid["coefficient_of_variation"].idxmin()]
    most_noisy = valid.loc[valid["coefficient_of_variation"].idxmax()]
    ci_width = summary["confidence_interval_upper"] - summary["confidence_interval_lower"]
    widest_ci_row = summary.loc[ci_width.idxmax()]

    def group_label(row):
        return f"{row['domain']} / {row['condition']} (input_value={row['input_value']} {row['input_unit']})"

    text = f"""# Replicate Analysis

## Which replicate group is most stable?
**{group_label(most_stable)}** — lowest CV ({fmt(most_stable['coefficient_of_variation'])}).

## Which replicate group is most noisy?
**{group_label(most_noisy)}** — highest CV ({fmt(most_noisy['coefficient_of_variation'])}), flagged **{most_noisy['stability_flag']}**.

## Which group has the widest confidence interval?
**{group_label(widest_ci_row)}**, width = {fmt(ci_width.max())}.

## Which group has the highest coefficient of variation?
Same as most noisy: **{group_label(most_noisy)}**.

## Why is mean alone not enough for judging reliability?
Mean shows the center but nothing about spread — two groups can share a mean while one is tightly clustered and one is scattered. Only std/SE/CI/CV reveal that difference.

## Why does replicate count affect confidence interval width?
SE = std / sqrt(n). Larger n shrinks SE, narrowing the CI, giving a more precise estimate of the mean.

## Which readings should be investigated before ML use?
The **{group_label(most_noisy)}** group — specifically its reading furthest from its replicate peers.
"""
    with open(os.path.join(output_dir, "replicate_analysis.md"), "w") as f:
        f.write(text)


def write_correlation_limitations(corr, output_dir):
    strongest = corr.loc[corr["pearson_r"].abs().idxmax()]
    weakest = corr.loc[corr["pearson_r"].abs().idxmin()]

    text = f"""# Correlation Limitations

## Strongest relationship
**{strongest['relationship']}**, Pearson r = {fmt(strongest['pearson_r'])}, R² = {fmt(strongest['r_squared'])}.

## Weakest / noisiest relationship
**{weakest['relationship']}**, Pearson r = {fmt(weakest['pearson_r'])}, R² = {fmt(weakest['r_squared'])}.

## Does high correlation prove causation?
No — a confound or coincidence can produce a strong correlation without any direct causal link.

## Can correlation be trusted with small sample size?
Not fully — with n=9 per relationship, one unusual point can shift r noticeably.

## Can correlation miss nonlinear relationships?
Yes — Pearson only measures straight-line strength; a strong curved relationship can show r near 0.

## How can outliers affect correlation?
A single extreme point can pull slope, intercept, r, MAE, and RMSE, especially with small n.

## How can confounding variables act here?
E.g. temperature rises alongside Electronics load — if temperature independently affects voltage, the load-signal relationship could partly reflect temperature instead.

## Why avoid mixed-domain correlation?
Different domains measure physically unrelated quantities in different units — any resulting correlation would be coincidental, not meaningful.
"""
    with open(os.path.join(output_dir, "correlation_limitations.md"), "w") as f:
        f.write(text)


def write_feature_dictionary(output_dir):
    text = """# Feature Dictionary

## rolling_average_signal
Formula: rolling mean of signal, window=3, grouped by domain+condition, ordered by time_step.
Applies to: all domains. Invalid when: time_step ordering is meaningless.
Useful for ML: smooths short-term noise into a stable trend estimate.

## normalized_signal
Formula: signal / baseline_signal. Applies to: all domains with a valid non-zero baseline.
Invalid when: baseline missing or zero. Useful for ML: makes readings comparable across conditions/instruments.

## power_w
Formula: voltage_v * current_a. Applies to: Electronics only.
Invalid when: domain isn't Electronics, or V/I missing. Useful for ML: P=VI is a physically meaningful derived quantity.

## error_percent
Formula: ((signal - expected_signal) / expected_signal) * 100. Applies to: all domains with valid expected_signal.
Invalid when: expected_signal missing or zero. Useful for ML: direct calibration-accuracy signal.

## stress_ratio
Formula: stress_mpa / reference_stress_mpa. Applies to: Mechanical only.
Invalid when: domain isn't Mechanical, or either stress value missing/zero.
Useful for ML: expresses stress relative to a known reference, relevant to failure risk.

## ml_ready
Formula: True only if signal/expected_signal/input_value/domain/condition are present AND the row's replicate-group CV is stable or moderate (<=0.15).
Useful for ML: single explicit gate for whether a row should be trusted for training.
"""
    with open(os.path.join(output_dir, "feature_dictionary.md"), "w") as f:
        f.write(text)


def write_feature_summary(feat_df, output_dir):
    not_ready = feat_df[feat_df["ml_ready"] == False]
    not_ready_text = "No rows were excluded in this dataset." if not_ready.empty else \
        f"Excluded rows: {', '.join(not_ready['record_id'].tolist())}."

    text = f"""# Feature Summary

## General features (all domains)
rolling_average_signal, normalized_signal, error_percent, ml_ready.

## Domain-specific features
power_w (Electronics only), stress_ratio (Mechanical only).

## Rows not ML-ready
{not_ready_text}

## Most useful feature per domain
Electronics: power_w. Mechanical: stress_ratio. Biochem: normalized_signal.

## Why leave invalid features blank instead of zero?
A forced 0 would look like a real measurement (e.g. "zero power" for a Biochem row), silently injecting false information. Blank (NaN) correctly signals "not applicable."

## How can feature engineering mislead?
Rolling averages can smooth over a real sudden failure; a wrong baseline silently distorts every normalized value; error percent explodes when expected_signal is near zero; features built from information not available at prediction time cause data leakage.
"""
    with open(os.path.join(output_dir, "feature_summary.md"), "w") as f:
        f.write(text)
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_csv> <output_dir>")
        sys.exit(1)
    run_pipeline(sys.argv[1], sys.argv[2])