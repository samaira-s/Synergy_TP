# Error Analysis

## 1. Largest regression errors
The 3 largest absolute errors on the test set were:
- Actual CO(GT) = 4.800, Predicted = 2.815, Error = 1.985
- Actual CO(GT) = 6.300, Predicted = 4.322, Error = 1.978
- Actual CO(GT) = 3.300, Predicted = 1.439, Error = 1.861

Likely reasons: a simple linear model cannot capture non-linear sensor response or sudden
pollution spikes (e.g. traffic surges) that don't follow the average linear sensor-to-CO
relationship learned from the rest of the data; sensor drift over the collection period may
also mean the relationship between PT08 readings and CO(GT) wasn't perfectly constant
throughout.

## 2. Classification mistakes
101 out of 1102 test rows were misclassified. Misclassifications
are most likely to occur for rows near the classification threshold itself
(1.8000), where the true CO(GT) value is only marginally above
or below the median split — a case that's genuinely ambiguous, not necessarily a modeling
failure.

## 3. Is the classification task balanced or imbalanced?
Test set class counts: {np.int64(0): np.int64(624), np.int64(1): np.int64(478)}.
Balance ratio (minority/majority) = 0.766. Since this label was created
with a median split by construction, the classes are close to balanced
(though this run shows some imbalance) —
this is a designed property of the median-threshold approach, not an accident of the raw data.

## 4. Does the clustering result align with a meaningful pattern?
The cluster centroids (see `clustering_metrics.json`) separate primarily along temperature and
humidity, which plausibly reflects real day/night or seasonal weather regimes rather than
random groupings — supported by silhouette score = 0.4554. This is a
plausible, physically-grounded pattern, but was not validated against any external ground
truth (e.g. actual time-of-day or season labels), so it remains an interpretation, not a proven fact.

## 5. Limitations of the current baseline models
- Linear regression assumes a straight-line relationship between sensors and CO(GT); any real
  non-linear sensor behavior is not captured.
- The classification threshold (median split) is somewhat arbitrary — a different, domain-driven
  threshold (e.g. a WHO air-quality guideline value) might produce a more practically meaningful label.
- KMeans assumes round, similarly-sized clusters and is sensitive to the random initialization
  and the choice of k, neither of which was extensively tuned here.
- All three models use a single chronological train/val/test split rather than multiple
  validation folds, so performance estimates carry some uncertainty from that one split alone.
