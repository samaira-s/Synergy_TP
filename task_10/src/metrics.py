import numpy as np

def mean_abs_error(y_true,y_pred):
    return np.mean(np.abs(y_true-y_pred))
def mean_square_error(y_true,y_pred):
    return np.mean((y_true-y_pred)**2)
def root_mean_squared_error(y_true,y_pred):
    return np.sqrt(mean_square_error(y_true,y_pred))

def r_squared(y_true,y_pred):
    ss_res=np.sum((y_true-y_pred)**2)
    ss_tot=np.sum((y_true-np.mean(y_true))**2)
    return 1- ss_res/ss_tot if ss_tot!=0 else None

def confus_matrix(y_true,y_pred):
    true_positive=np.sum((y_true==1)&(y_pred==1))
    true_negative=np.sum((y_true==0) & (y_pred==0))
    false_negative=np.sum((y_true==1)&(y_pred==0))
    false_positive=np.sum((y_true==0)&(y_pred==1))
    return {
        "true_positive": int(true_positive),
        "true_negative": int(true_negative),
        "false_positive": int(false_positive),
        "false_negative": int(false_negative),
    }

def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred)

def precision_score(y_true, y_pred):
    counts = confus_matrix(y_true, y_pred)
    tp, fp = counts["true_positive"], counts["false_positive"]
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0

def recall_score(y_true, y_pred):
    counts = confus_matrix(y_true, y_pred)
    tp, fn = counts["true_positive"], counts["false_negative"]
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0

def f1_score(y_true, y_pred):
    p = precision_score(y_true, y_pred)
    r = recall_score(y_true, y_pred)
    return 2 * p * r / (p + r) if (p + r) > 0 else 0.0