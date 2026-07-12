import numpy as np
import pandas as pd

REGRESSION_TARGET="CO(GT)"
REGRESSION_FEATURES=["PT08.S1(CO)", "PT08.S2(NMHC)", "PT08.S3(NOx)",
    "PT08.S4(NO2)", "PT08.S5(O3)", "T", "RH", "AH"]
CLASSIFICATION_FEAUTURES=REGRESSION_FEATURES
CLUSTERING_FEATURES=["T","RH"]

def load(filepath):
    df=pd.read_csv(filepath,sep=";",decimal=",")
    df=df.dropna(how="all")
    df=df.drop(columns=[s for s in df.columns if "Unnamed"in s])
    return df
def clean_missing(df,missing_marker=-200):  #The UCI dataset uses -200 to mean "missing," not a real reading
    numeric_cols=df.select_dtypes(include=[np.number]).columns
    df=df.copy()    #changes you make to it inside the function could unexpectedly also change the original DataFrame sitting outside the function
    df[numeric_cols]=df[numeric_cols].replace(missing_marker,np.nan)
    return df

def prep(filepath):
    df=load(filepath)
    df=clean_missing(df)
    needed_cols=list(set(REGRESSION_FEATURES+[REGRESSION_TARGET]+CLUSTERING_FEATURES))
    df=df.dropna(subset=needed_cols).reset_index(drop=True)
    return df

def split(df,train_frac=0.7,val_frac=0.15):
    n=len(df)
    train_end=int(n*train_frac)
    val_end=int(n*(train_frac+val_frac))
    train_df=df.iloc[:train_end].reset_index(drop=True)
    val_df=df.iloc[train_end:val_end].reset_index(drop=True)
    test_df=df.iloc[val_end:].reset_index(drop=True)
    return train_df,val_df,test_df

def compute(train_df,feature_cols):
    means=train_df[feature_cols].mean()
    stds=train_df[feature_cols].std(ddof=1)
    return means,stds
def apply_scaling(df,feature_cols,means,stds):
    df=df.copy()
    df[feature_cols]=(df[feature_cols]-means)/stds
    return df

#median-threshold split
def compute_thresh(train_df,target_col=REGRESSION_TARGET):
    return train_df[target_col].median()    #descision boundary
def compute_label(df,threshold,target_col=REGRESSION_TARGET):
    df=df.copy()
    df["pollution_class"]=(df[target_col]>threshold).astype(int)
    return df

def get_X_y(df,feature_cols,target_col):
    X=df[feature_cols].to_numpy(dtype=float)
    y=df[target_col].to_numpy(dtype=float)
    return X,y

if __name__=="__main__":
    import sys
    df=prep(sys.argv[1])
    print("shape after cleaning: ",df.shape)
    print(df[REGRESSION_FEATURES+[REGRESSION_TARGET]].describe())
    train_df, val_df, test_df = split(df)
    print("\nTrain/Val/Test sizes:", len(train_df), len(val_df), len(test_df))

    means, stds = compute(train_df, REGRESSION_FEATURES)
    train_scaled = apply_scaling(train_df, REGRESSION_FEATURES, means, stds)
    print("\nScaled train feature means (should be ~0):")
    print(train_scaled[REGRESSION_FEATURES].mean())

    threshold = compute_thresh(train_df)
    print("\nClassification threshold (train median CO(GT)):", threshold)
    train_labeled =compute_label(train_df, threshold)
    print(train_labeled["pollution_class"].value_counts())
    