# Model Comparison

## 1. Regression target
Target: **CO(GT)**, the reference-analyzer carbon monoxide concentration (mg/m^3). This is a
valid continuous prediction task because CO(GT) is a real-valued physical measurement, not a
category, and it can be predicted from other, independently-measured sensor readings
(PT08 tin-oxide sensors, temperature, humidity) without directly using CO(GT) or any value
derived from it as an input feature.

## 2. Regression vs baseline
- Model    -> MAE: 0.3591, RMSE: 0.5030, R2: 0.8474
- Baseline -> MAE: 1.0463, RMSE: 1.3059, R2: -0.0283
The trained model clearly outperforms the mean
baseline, explaining a large share of the variance in CO(GT) that the baseline (which explains none, by definition) cannot.

## 3. Classification target
Target: **pollution_class**, a binary label derived by splitting CO(GT) at the training set's
median value (threshold = 1.8000): 1 = high pollution, 0 = low
pollution. The threshold was computed only from training data to avoid leaking test-set
information into the label definition itself.

## 4. Classification vs baseline
- Model    -> Accuracy: 0.9083, Precision: 0.8689, Recall: 0.9289, F1: 0.8979
- Baseline -> Accuracy: 0.5662, Precision: 0.0000, Recall: 0.0000, F1: 0.0000
The model clearly outperforms the majority-class
baseline. The baseline's precision/recall/F1 are 0 whenever it never predicts the minority
class at all, which is expected baseline behavior, not an error.

## 5. Which classification error is more serious?
For air pollution monitoring, a **false negative** (predicting "low pollution" when it's
actually high) is more serious than a false positive, since it means a real high-pollution
event goes undetected/unflagged, with real health/safety consequences, whereas a false
positive only causes an unnecessary precaution. This model's confusion matrix
(TP=444, FP=67, FN=34, TN=557)
shows recall (0.9289) is higher than precision
(0.8689), which is the safer direction for this particular error tradeoff.

## 6. Clustering features and label usage
Features used: **T, RH**. No label (CO(GT) or pollution_class) was
used anywhere in the clustering process — KMeans only ever saw temperature and humidity,
consistent with clustering being unsupervised by definition; using a label would defeat the
purpose of discovering structure without supervision.

## 7. Are the clusters meaningful or artificial?
With k=3, the algorithm converged in 17 iterations, inertia =
396492.65, silhouette score = 0.4554. A silhouette score
clearly above 0 suggests reasonably real, separable structure rather than
arbitrary groupings, though this should be checked visually against `clustering_plot.png`.

## 8. Data leakage risks in this implementation
- If scaling statistics or the classification threshold had been computed from the full
  dataset instead of training data only, that would be preprocessing/target leakage
  (avoided here by design).
- Including NOx(GT)/NO2(GT) as regression features would risk leaking other reference-lab
  measurements into a task meant to test low-cost sensor calibration (excluded here).
- Randomly shuffling this time-series data before splitting would leak near-identical
  adjacent-hour information from train into test (avoided by chronological splitting).

## 9. Is this dataset ready for stronger ML models?
The dataset shows real, learnable signal (regression model clearly beats baseline; R2 =
0.8474), so it is reasonable to try stronger models. However, known dataset
issues (missing NMHC(GT), sensor drift over the ~1-year collection period, hourly
autocorrelation) should be addressed with more careful validation (e.g. multiple chronological
folds) before trusting a more complex model's results.
