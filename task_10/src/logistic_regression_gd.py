import numpy as np


def initialize_weights(n_features):
    weights = np.zeros(n_features)
    bias = 0.0
    return weights, bias

def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1 / (1 + np.exp(-z)) #Clipping caps z's range before the exponential, preventing that crash
def predict_proba(X, weights, bias):
    z = X @ weights + bias
    return sigmoid(z)


def predict(X, weights, bias, threshold=0.5):
    probabilities = predict_proba(X, weights, bias)
    return (probabilities >= threshold).astype(int)

def log_loss(y_true, y_pred_proba):
    eps = 1e-15
    y_pred_proba = np.clip(y_pred_proba, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred_proba) + (1 - y_true) * np.log(1 - y_pred_proba))

def compute_gradients(X, y, weights, bias):
    n = X.shape[0]
    y_pred_proba = predict_proba(X, weights, bias)
    error = y_pred_proba - y

    grad_weights = (1 / n) * (X.T @ error)
    grad_bias = (1 / n) * np.sum(error)

    return grad_weights, grad_bias

def train_logistic_regression(X, y, learning_rate=0.1, n_iterations=1000):
    n_features = X.shape[1]
    weights, bias = initialize_weights(n_features)
    loss_history = []

    for i in range(n_iterations):
        y_pred_proba = predict_proba(X, weights, bias)
        loss = log_loss(y, y_pred_proba)
        loss_history.append(loss)

        grad_weights, grad_bias = compute_gradients(X, y, weights, bias)

        weights = weights - learning_rate * grad_weights
        bias = bias - learning_rate * grad_bias

    return weights, bias, loss_history

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from data_utils import (
        prep,split,compute,apply_scaling,compute_thresh,compute_label,get_X_y,CLASSIFICATION_FEAUTURES)
    
    from metrics import accuracy_score, precision_score, recall_score, f1_score, confus_matrix
    from baselines import majority_class_baseline

    df = prep(sys.argv[1])
    train_df, val_df, test_df = split(df)

    threshold = compute_thresh(train_df)
    train_df = compute_label(train_df, threshold)
    test_df = compute_label(test_df, threshold)

    means, stds = compute(train_df, CLASSIFICATION_FEAUTURES)
    train_scaled = apply_scaling(train_df, CLASSIFICATION_FEAUTURES, means, stds)
    test_scaled = apply_scaling(test_df, CLASSIFICATION_FEAUTURES, means, stds)

    X_train, y_train = get_X_y(train_scaled, CLASSIFICATION_FEAUTURES, "pollution_class")
    X_test, y_test = get_X_y(test_scaled, CLASSIFICATION_FEAUTURES, "pollution_class")

    weights, bias, loss_history = train_logistic_regression(X_train, y_train, learning_rate=0.5, n_iterations=1000)
    print("Final training loss:", loss_history[-1])
    print("First loss:", loss_history[0])

    y_pred = predict(X_test, weights, bias)
    print("Model    -> Acc:", accuracy_score(y_test, y_pred), "Prec:", precision_score(y_test, y_pred),
          "Recall:", recall_score(y_test, y_pred), "F1:", f1_score(y_test, y_pred))
    print("Confusion matrix:", confus_matrix(y_test, y_pred))

    y_baseline = majority_class_baseline(y_train, len(y_test))
    print("Baseline -> Acc:", accuracy_score(y_test, y_baseline), "Prec:", precision_score(y_test, y_baseline),
          "Recall:", recall_score(y_test, y_baseline), "F1:", f1_score(y_test, y_baseline))