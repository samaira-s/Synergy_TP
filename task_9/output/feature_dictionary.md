# Feature Dictionary

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
