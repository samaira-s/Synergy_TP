import os 
import sys

sys.path.insert(0,os.path.dirname(__file__))

import numpy as np
import pandas as pd 
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import (prep,split,compute,apply_scaling,compute_thresh,compute_label,get_X_y,REGRESSION_FEATURES,REGRESSION_TARGET,CLASSIFICATION_FEAUTURES,CLUSTERING_FEATURES)
from metrics import (mean_abs_error,mean_square_error,root_mean_squared_error,r_squared,accuracy_score,precision_score,recall_score,f1_score,confus_matrix)
from baselines import (mean_baseline,majority_class_baseline)
from linear_regression_gd import train_linear_regression,predict as lr_predict
from logistic_regression_gd import train_logistic_regression,predict as lg_predict
from kmeans import kmeans,inertia,compute_silhouette_score

def run_regression_pipeline(df, output_dir):
    train_df, val_df, test_df = split(df)
    means, stds = compute(train_df, REGRESSION_FEATURES)
    train_scaled = apply_scaling(train_df, REGRESSION_FEATURES, means, stds)
    test_scaled = apply_scaling(test_df, REGRESSION_FEATURES, means, stds)
    X_train, y_train = get_X_y(train_scaled, REGRESSION_FEATURES, REGRESSION_TARGET)
    X_test, y_test = get_X_y(test_scaled, REGRESSION_FEATURES, REGRESSION_TARGET)

    weights, bias, loss_history = train_linear_regression(X_train, y_train, learning_rate=0.1, n_iterations=1000)
    y_pred = lr_predict(X_test, weights, bias)
    y_baseline = mean_baseline(y_train, len(y_test))

    results = {
        "model_mae": mean_abs_error(y_test, y_pred),
        "model_rmse": root_mean_squared_error(y_test, y_pred),
        "model_r2": r_squared(y_test, y_pred),
        "baseline_mae": mean_abs_error(y_test, y_baseline),
        "baseline_rmse": root_mean_squared_error(y_test, y_baseline),
        "baseline_r2": r_squared(y_test, y_baseline),
        "weights": dict(zip(REGRESSION_FEATURES, weights)),
        "bias": bias,
    }
    results["test_actual"] = y_test
    results["test_predicted"] = y_pred

    plot_loss_curve(loss_history, "Regression Training Loss (MSE)", os.path.join(output_dir, "regression_loss_curve.png"))
    plot_actual_vs_predicted(y_test, y_pred, os.path.join(output_dir, "actual_vs_predicted.png"))

    return results


def run_classification_pipeline(df, output_dir):
    train_df, val_df, test_df = split(df)
    threshold = compute_thresh(train_df)
    train_df = compute_label(train_df, threshold)
    test_df = compute_label(test_df, threshold)

    means, stds = compute(train_df, CLASSIFICATION_FEAUTURES)
    train_scaled = apply_scaling(train_df,CLASSIFICATION_FEAUTURES , means, stds)
    test_scaled = apply_scaling(test_df, CLASSIFICATION_FEAUTURES, means, stds)

    X_train, y_train = get_X_y(train_scaled, CLASSIFICATION_FEAUTURES, "pollution_class")
    X_test, y_test = get_X_y(test_scaled, CLASSIFICATION_FEAUTURES, "pollution_class")
    weights, bias, loss_history = train_logistic_regression(X_train, y_train, learning_rate=0.5, n_iterations=1000)
    y_pred = lg_predict(X_test, weights, bias)
    y_baseline = majority_class_baseline(y_train, len(y_test))

    cm = confus_matrix(y_test, y_pred)

    results = {
        "classification_threshold": threshold,
        "model_accuracy": accuracy_score(y_test, y_pred),
        "model_precision": precision_score(y_test, y_pred),
        "model_recall": recall_score(y_test, y_pred),
        "model_f1": f1_score(y_test, y_pred),
        "baseline_accuracy": accuracy_score(y_test, y_baseline),
        "baseline_precision": precision_score(y_test, y_baseline),
        "baseline_recall": recall_score(y_test, y_baseline),
        "baseline_f1": f1_score(y_test, y_baseline),
        "confusion_matrix": cm,
        "weights": dict(zip(CLASSIFICATION_FEAUTURES, weights)),
        "bias": bias,
    }
    results["test_actual"] = y_test
    results["test_predicted"] = y_pred

    plot_loss_curve(loss_history, "Classification Training Loss (Log Loss)", os.path.join(output_dir, "classification_loss_curve.png"))
    plot_confusion_matrix(cm, os.path.join(output_dir, "confusion_matrix.png"))

    return results


def run_clustering_pipeline(df, output_dir, k=3):
    train_df, val_df, test_df = split(df)
    X = train_df[CLUSTERING_FEATURES].to_numpy(dtype=float)
    centroids, cluster_assignments, n_iterations = kmeans(X, k=k)
    inertiaa = inertia(X, centroids, cluster_assignments)
    silhouette = compute_silhouette_score(X, cluster_assignments, k)

    cluster_summary = []
    for i in range(k):
        points = X[cluster_assignments == i]
        cluster_summary.append({
            "cluster": i,
            "size": len(points),
            "centroid": dict(zip(CLUSTERING_FEATURES, centroids[i])),
            "feature_means": dict(zip(CLUSTERING_FEATURES, points.mean(axis=0))),
        })
        results = {
        "k": k,
        "n_iterations": n_iterations,
        "inertia": inertiaa,
        "silhouette_score": silhouette,
        "cluster_summary": cluster_summary,
    }
    results["X_used"] = X
    results["cluster_assignments"] = cluster_assignments
    plot_clusters_2d(X, cluster_assignments, centroids, os.path.join(output_dir, "clustering_plot.png"))

    return results

import json

def _to_jsonable(obj):
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def save_regression_outputs(results, test_df, output_dir):
    metrics = {k: v for k, v in results.items() if k not in ("test_actual", "test_predicted")}
    with open(os.path.join(output_dir, "regression_metrics.json"), "w") as f:
        json.dump(_to_jsonable(metrics), f, indent=2)

    pred_df = pd.DataFrame({
        "actual_CO_GT": results["test_actual"],
        "predicted_CO_GT": results["test_predicted"],
    })
    pred_df.to_csv(os.path.join(output_dir, "regression_predictions.csv"), index=False)


def save_classification_outputs(results, output_dir):
    metrics = {k: v for k, v in results.items() if k not in ("test_actual", "test_predicted")}
    with open(os.path.join(output_dir, "classification_metrics.json"), "w") as f:
        json.dump(_to_jsonable(metrics), f, indent=2)

    pred_df = pd.DataFrame({
        "actual_class": results["test_actual"],
        "predicted_class": results["test_predicted"],
    })
    pred_df.to_csv(os.path.join(output_dir, "classification_predictions.csv"), index=False)


def save_clustering_outputs(results, output_dir):
    metrics = {k: v for k, v in results.items() if k not in ("X_used", "cluster_assignments")}
    with open(os.path.join(output_dir, "clustering_metrics.json"), "w") as f:
        json.dump(_to_jsonable(metrics), f, indent=2)

    assign_df = pd.DataFrame(results["X_used"], columns=CLUSTERING_FEATURES)
    assign_df["cluster"] = results["cluster_assignments"]
    assign_df.to_csv(os.path.join(output_dir, "clustering_assignments.csv"), index=False)
def plot_loss_curve(loss_history, title, output_path):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.plot(loss_history, color="blue")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Loss")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

def plot_actual_vs_predicted(y_true, y_pred, output_path):
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(y_true, y_pred, alpha=0.4,  color="blue")#s=15,
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    ax.plot(lims, lims, "--", color="blue", label="Perfect prediction")
    ax.set_xlabel("Actual CO(GT)")
    ax.set_ylabel("Predicted CO(GT)")
    ax.set_title("Actual vs Predicted")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=130)
    plt.close(fig)    

def plot_confusion_matrix(cm, output_path):
    matrix = np.array([[cm["true_negative"], cm["false_positive"]],
                        [cm["false_negative"], cm["true_positive"]]])
    fig, ax = plt.subplots(figsize=(5, 4.5))
    im = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Predicted 0", "Predicted 1"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["Actual 0", "Actual 1"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center",
                    color="white" if matrix[i, j] > matrix.max() / 2 else "black")
    ax.set_title("Confusion Matrix")
    #fig.colorbar(im)
    fig.tight_layout()
    fig.savefig(output_path, dpi=130)
    plt.close(fig)


def plot_clusters_2d(X, cluster_assignments, centroids, output_path):
    fig, ax = plt.subplots(figsize=(6, 5))
    colors = ["blue", "orange", "green", "red", "violet"]
    for i in range(centroids.shape[0]):
        points = X[cluster_assignments == i]
        ax.scatter(points[:, 0], points[:, 1], s=15, alpha=0.5, color=colors[i % len(colors)], label=f"Cluster {i}")
    ax.scatter(centroids[:, 0], centroids[:, 1], s=200, marker="X", color="black", label="Centroids")
    ax.set_xlabel(CLUSTERING_FEATURES[0])
    ax.set_ylabel(CLUSTERING_FEATURES[1])
    ax.set_title("2D Cluster Visualization")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=130)
    plt.close(fig)


def run_pipeline(input_csv, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    df = prep(input_csv)

    regression_results = run_regression_pipeline(df, output_dir)
    classification_results = run_classification_pipeline(df, output_dir)
    clustering_results = run_clustering_pipeline(df, output_dir)

    save_regression_outputs(regression_results, None, output_dir)
    save_classification_outputs(classification_results, output_dir)
    save_clustering_outputs(clustering_results, output_dir)

    write_model_comparison(regression_results, classification_results, clustering_results, output_dir)
    write_error_analysis(regression_results, classification_results, clustering_results, output_dir)

    print(f"Pipeline complete. Outputs written to: {output_dir}")
def write_model_comparison(reg, clf, clust, output_dir):
    reg_better = reg["model_r2"] > reg["baseline_r2"]
    clf_better = clf["model_accuracy"] > clf["baseline_accuracy"]
    cm = clf["confusion_matrix"]

    text = f"""# Model Comparison

## 1. Regression target
Target: **CO(GT)**, the reference-analyzer carbon monoxide concentration (mg/m^3). This is a
valid continuous prediction task because CO(GT) is a real-valued physical measurement, not a
category, and it can be predicted from other, independently-measured sensor readings
(PT08 tin-oxide sensors, temperature, humidity) without directly using CO(GT) or any value
derived from it as an input feature.

## 2. Regression vs baseline
- Model    -> MAE: {reg['model_mae']:.4f}, RMSE: {reg['model_rmse']:.4f}, R2: {reg['model_r2']:.4f}
- Baseline -> MAE: {reg['baseline_mae']:.4f}, RMSE: {reg['baseline_rmse']:.4f}, R2: {reg['baseline_r2']:.4f}
The trained model {"clearly outperforms" if reg_better else "does not outperform"} the mean
baseline, {"explaining a large share of the variance in CO(GT) that the baseline (which explains none, by definition) cannot." if reg_better else "suggesting the chosen features may not carry enough signal for this target."}

## 3. Classification target
Target: **pollution_class**, a binary label derived by splitting CO(GT) at the training set's
median value (threshold = {clf['classification_threshold']:.4f}): 1 = high pollution, 0 = low
pollution. The threshold was computed only from training data to avoid leaking test-set
information into the label definition itself.

## 4. Classification vs baseline
- Model    -> Accuracy: {clf['model_accuracy']:.4f}, Precision: {clf['model_precision']:.4f}, Recall: {clf['model_recall']:.4f}, F1: {clf['model_f1']:.4f}
- Baseline -> Accuracy: {clf['baseline_accuracy']:.4f}, Precision: {clf['baseline_precision']:.4f}, Recall: {clf['baseline_recall']:.4f}, F1: {clf['baseline_f1']:.4f}
The model {"clearly outperforms" if clf_better else "does not outperform"} the majority-class
baseline. The baseline's precision/recall/F1 are 0 whenever it never predicts the minority
class at all, which is expected baseline behavior, not an error.

## 5. Which classification error is more serious?
For air pollution monitoring, a **false negative** (predicting "low pollution" when it's
actually high) is more serious than a false positive, since it means a real high-pollution
event goes undetected/unflagged, with real health/safety consequences, whereas a false
positive only causes an unnecessary precaution. This model's confusion matrix
(TP={cm['true_positive']}, FP={cm['false_positive']}, FN={cm['false_negative']}, TN={cm['true_negative']})
shows recall ({clf['model_recall']:.4f}) is {"higher than" if clf['model_recall'] > clf['model_precision'] else "lower than"} precision
({clf['model_precision']:.4f}), which is the safer direction for this particular error tradeoff.

## 6. Clustering features and label usage
Features used: **{', '.join(CLUSTERING_FEATURES)}**. No label (CO(GT) or pollution_class) was
used anywhere in the clustering process — KMeans only ever saw temperature and humidity,
consistent with clustering being unsupervised by definition; using a label would defeat the
purpose of discovering structure without supervision.

## 7. Are the clusters meaningful or artificial?
With k={clust['k']}, the algorithm converged in {clust['n_iterations']} iterations, inertia =
{clust['inertia']:.2f}, silhouette score = {clust['silhouette_score']:.4f}. A silhouette score
{"clearly above 0 suggests reasonably real, separable structure" if clust['silhouette_score'] > 0.25 else "close to 0 suggests weak or overlapping structure"} rather than
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
{reg['model_r2']:.4f}), so it is reasonable to try stronger models. However, known dataset
issues (missing NMHC(GT), sensor drift over the ~1-year collection period, hourly
autocorrelation) should be addressed with more careful validation (e.g. multiple chronological
folds) before trusting a more complex model's results.
"""
    with open(os.path.join(output_dir, "model_comparison.md"), "w") as f:
        f.write(text)
def write_error_analysis(reg, clf, clust, output_dir):
    reg_errors = np.abs(reg["test_actual"] - reg["test_predicted"])
    worst_idx = np.argsort(reg_errors)[-3:][::-1]

    clf_wrong = np.where(clf["test_actual"] != clf["test_predicted"])[0]
    n_wrong = len(clf_wrong)

    class_counts = np.unique(clf["test_actual"], return_counts=True)
    class_balance_ratio = class_counts[1].min() / class_counts[1].max()

    text = f"""# Error Analysis

## 1. Largest regression errors
The 3 largest absolute errors on the test set were:
"""
    for i in worst_idx:
        text += (f"- Actual CO(GT) = {reg['test_actual'][i]:.3f}, "
                  f"Predicted = {reg['test_predicted'][i]:.3f}, "
                  f"Error = {reg_errors[i]:.3f}\n")

    text += f"""
Likely reasons: a simple linear model cannot capture non-linear sensor response or sudden
pollution spikes (e.g. traffic surges) that don't follow the average linear sensor-to-CO
relationship learned from the rest of the data; sensor drift over the collection period may
also mean the relationship between PT08 readings and CO(GT) wasn't perfectly constant
throughout.

## 2. Classification mistakes
{n_wrong} out of {len(clf['test_actual'])} test rows were misclassified. Misclassifications
are most likely to occur for rows near the classification threshold itself
({clf['classification_threshold']:.4f}), where the true CO(GT) value is only marginally above
or below the median split — a case that's genuinely ambiguous, not necessarily a modeling
failure.

## 3. Is the classification task balanced or imbalanced?
Test set class counts: {dict(zip(class_counts[0].astype(int), class_counts[1].astype(int)))}.
Balance ratio (minority/majority) = {class_balance_ratio:.3f}. Since this label was created
with a median split by construction, the classes are close to balanced
({"confirmed here" if class_balance_ratio > 0.8 else "though this run shows some imbalance"}) —
this is a designed property of the median-threshold approach, not an accident of the raw data.

## 4. Does the clustering result align with a meaningful pattern?
The cluster centroids (see `clustering_metrics.json`) separate primarily along temperature and
humidity, which plausibly reflects real day/night or seasonal weather regimes rather than
random groupings — supported by silhouette score = {clust['silhouette_score']:.4f}. This is a
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
"""
    with open(os.path.join(output_dir, "error_analysis.md"), "w") as f:
        f.write(text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_csv> <output_dir>")
        sys.exit(1)
    run_pipeline(sys.argv[1], sys.argv[2])