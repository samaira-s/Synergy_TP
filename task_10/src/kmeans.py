import numpy as np 
def initialise_centroid(X,k):
    np.random.seed(42)
    indices=np.random.choice(X.shape[0],size=k,replace=False)
    centroid=X[indices]
    return centroid

def compute_distances(X,centroid):
    n_samples=X.shape[0]
    k=centroid.shape[0]
    dist=np.zeros((n_samples,k))

    for i in range(k):
        diff=X-centroid[i]
        dist[:, i]=np.sqrt(np.sum(diff**2,axis=1))    #sum along each row
    return dist

def assign_cluster(distance):
    return np.argmin(distance,axis=1)

def update_centroid(X,cluster_assignments,k):
    n_features=X.shape[1]
    new_centroids=np.zeros((k,n_features))
    
    for i in range (k):
        point_in_cluster=X[cluster_assignments==i]
        if len(point_in_cluster)>0:
            new_centroids[i]=np.mean(point_in_cluster,axis=0)
        else:
            new_centroids[i]=X[np.random.choice(X.shape[0])]
    return new_centroids

def kmeans(X,k,max_iteration=1000,tol=1e-4):
    centroids=initialise_centroid(X,k)
    for iteration in range (max_iteration):
        distance=compute_distances(X,centroids)
        cluster=assign_cluster(distance)
        new_centroids=update_centroid(X,cluster,k)

        centroid_shift=np.sqrt(np.sum((new_centroids-centroids)**2))
        centroids=new_centroids
        if centroid_shift<tol:
            break
    return centroids,cluster,iteration+1
    
#Inertia = sum of squared distances from every point to its own assigned centroid, added up across all clusters. 
def inertia(X,centroids,cluster):
    total=0.0
    for i in range(centroids.shape[0]):
        point_in_cluster=X[cluster==i]
        total+=np.sum((point_in_cluster-centroids[i])**2)
    return total

def compute_silhouette_score(X, cluster_assignments, k):
    n = X.shape[0]
    silhouette_values = np.zeros(n)

    for idx in range(n):
        own_cluster = cluster_assignments[idx]
        own_cluster_points = X[cluster_assignments == own_cluster]

        if len(own_cluster_points) <= 1:
            silhouette_values[idx] = 0.0
            continue

        a = np.mean(np.sqrt(np.sum((own_cluster_points - X[idx]) ** 2, axis=1)))
        a = a * len(own_cluster_points) / (len(own_cluster_points) - 1)  # exclude self

        b_values = []
        for other_cluster in range(k):
            if other_cluster == own_cluster:
                continue
            other_points = X[cluster_assignments == other_cluster]
            if len(other_points) == 0:
                continue
            b_values.append(np.mean(np.sqrt(np.sum((other_points - X[idx]) ** 2, axis=1))))

        b = min(b_values) if b_values else 0.0
        silhouette_values[idx] = (b - a) / max(a, b) if max(a, b) > 0 else 0.0

    return np.mean(silhouette_values)

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from data_utils import prep, split, CLUSTERING_FEATURES

    df = prep(sys.argv[1])
    train_df, val_df, test_df = split(df)
    X = train_df[CLUSTERING_FEATURES].to_numpy(dtype=float)

    centroids, assignments, n_iter = kmeans(X, k=3)
    print("Converged in", n_iter, "iterations")
    print("Centroids (T, RH):\n", centroids)
    print("Cluster sizes:", np.bincount(assignments))
    print("Inertia:", inertia(X, centroids, assignments))

