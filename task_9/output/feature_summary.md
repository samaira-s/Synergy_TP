# Feature Summary

## General features (all domains)
rolling_average_signal, normalized_signal, error_percent, ml_ready.

## Domain-specific features
power_w (Electronics only), stress_ratio (Mechanical only).

## Rows not ML-ready
No rows were excluded in this dataset.

## Most useful feature per domain
Electronics: power_w. Mechanical: stress_ratio. Biochem: normalized_signal.

## Why leave invalid features blank instead of zero?
A forced 0 would look like a real measurement (e.g. "zero power" for a Biochem row), silently injecting false information. Blank (NaN) correctly signals "not applicable."

## How can feature engineering mislead?
Rolling averages can smooth over a real sudden failure; a wrong baseline silently distorts every normalized value; error percent explodes when expected_signal is near zero; features built from information not available at prediction time cause data leakage.
