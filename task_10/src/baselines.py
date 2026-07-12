import numpy as np

def mean_baseline(y_train,n_predictions):
    baseline_value=np.mean(y_train)
    return np.full(n_predictions,baseline_value)    #creates an array of length n_predictions, every single entry equal to baseline_value

def majority_class_baseline(y_train,n_predictions):
    values,counts=np.unique(y_train,return_counts=True)
    majority_class=values[np.argmax(counts)]
    return np.full(n_predictions, majority_class)

