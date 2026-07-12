import numpy as np

def initialise(n_features):
    weights=np.zeros(n_features)
    bias=0.0
    return weights,bias
def predict(X,weights,bias):
    return X@weights+bias

def compute_gradient(X,y,weights,bias):
    n=X.shape[0]
    y_pred=predict(X,weights,bias)
    error=y_pred-y
    grad_weights=(2/n)*(X.T@error)
    grad_bias=(2/n)*np.sum(error)
    return grad_weights,grad_bias

def train_linear_regression(X, y, learning_rate=0.01, n_iterations=1000):
    n_features = X.shape[1]
    weights, bias = initialise(n_features)
    loss_history = []
    for i in range(n_iterations):
        y_pred = predict(X, weights, bias)
        loss = np.mean((y_pred - y) ** 2)
        loss_history.append(loss)
        grad_weights, grad_bias = compute_gradient(X, y, weights, bias)

        weights = weights - learning_rate * grad_weights
        bias = bias - learning_rate * grad_bias
    return weights, bias, loss_history

if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(__file__))
    from data_utils import(
        prep,split,compute,apply_scaling,get_X_y,REGRESSION_FEATURES,REGRESSION_TARGET)
    from metrics import mean_abs_error,root_mean_squared_error,r_squared
    from baselines import mean_baseline

    df=prep(sys.argv[1])
    train_df,val_df,test_df=split(df)

    means,stds=compute(train_df,REGRESSION_FEATURES)
    train_scaled=apply_scaling(train_df,REGRESSION_FEATURES,means,stds)
    test_scaled=apply_scaling(test_df,REGRESSION_FEATURES,means,stds)
    X_train,y_train=get_X_y(train_scaled,REGRESSION_FEATURES,REGRESSION_TARGET)
    X_test,y_test=get_X_y(test_scaled,REGRESSION_FEATURES,REGRESSION_TARGET)

    weights,bias,loss_hist=train_linear_regression(X_train,y_train)
    print("final training loss: ",loss_hist[-1])
    print("first loss: ",loss_hist[0])

    y_pred=predict(X_test,weights,bias)
    print("model -> MAE: ",mean_abs_error(y_test,y_pred),"RMSE:", root_mean_squared_error(y_test, y_pred), "R2:", r_squared(y_test, y_pred))

    y_baseline = mean_baseline(y_train, len(y_test))
    print("Baseline -> MAE:", mean_abs_error(y_test, y_baseline), "RMSE:", root_mean_squared_error(y_test, y_baseline), "R2:", r_squared(y_test, y_baseline))