# Correlation Limitations

## Strongest relationship
**Biochem: signal vs concentration**, Pearson r = 0.9993, R² = 0.9986.

## Weakest / noisiest relationship
**Mechanical: signal vs load**, Pearson r = 0.9841, R² = 0.9684.

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
