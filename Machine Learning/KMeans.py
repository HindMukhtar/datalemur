import numpy as np

class Kmeans: 
    def __init__(self, k:int, max_iters:int): 
        self.epochs = max_iters
        self.k = k 
        self.centroids = None 
    
    def fit(self, X):
        n_samples, n_features = X.shape 
        centroids = X[np.random.choice(n_samples, self.k, replace=False)] # Shape: k, n_features
        prev_centroids = None 

        for i in range(self.epochs): 
            # np.newaxis adds a dimension
            distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2) # Shape: n_samples, k 
            labels = np.argmin(distances, axis=1) # Shape: n_samples 
            for cluster_idx in range(self.k): 
                points = X[labels == cluster_idx]
                if len(points) > 0: 
                    centroids[cluster_idx] = np.mean(X[labels == i], axis = 0)

            if prev_centroids: 
                # if centroids haven't changed, clusters have converged 
                if np.all(prev_centroids == centroids): 
                    break 
            prev_centroids = centroids.copy() 

        self.centroids = centroids 

        return 


    def predict(self, X): 
        # find nearest cluster 
        if self.centroids: 
            distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
            return np.argmin(distances, axis=1)
        else: 
            return 



