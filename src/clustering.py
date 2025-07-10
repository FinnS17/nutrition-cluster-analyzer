from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from kneed import KneeLocator

def standardize_features(X):
    """
    Standardizes the feature matrix so that all columns have equal influence.
    
    Why?
    - KMeans clustering relies on distances.
    - Without standardization, features with larger scales (e.g., kcal) would dominate the clustering.
    
    Parameters:
    - X (pd.DataFrame or np.ndarray): The feature matrix.

    Returns:
    - np.ndarray: Standardized feature matrix.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def find_optimal_k(X_scaled, k_range=(2, 8)):
    """
    Determines the optimal number of clusters (k) using the Elbow method and KneeLocator.
    
    Parameters:
    - X_scaled (np.ndarray): Standardized feature matrix.
    - k_range (tuple): Range of k values to test (inclusive).

    Returns:
    - int: The optimal number of clusters.
    """
    inertias = []
    ks = list(range(k_range[0], k_range[1] + 1))

    for k in ks:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)

    # Determine elbow point
    kl = KneeLocator(ks, inertias, curve="convex", direction="decreasing")
    optimal_k = kl.elbow

    # Optional visualization:
    # plt.plot(ks, inertias, marker='o')
    # plt.vlines(optimal_k, min(inertias), max(inertias), colors='red', linestyles='dashed')
    # plt.title("Elbow Method")
    # plt.xlabel("Number of Clusters")
    # plt.ylabel("Inertia")
    # plt.grid(True)
    # plt.show()
    
    return optimal_k
        

def run_kmeans(X_scaled, n_clusters):
    """
    Performs KMeans clustering on the standardized feature matrix.

    Parameters:
    - X_scaled (np.ndarray): Standardized feature matrix.
    - n_clusters (int): Number of clusters to form.

    Returns:
    - model (KMeans): Trained KMeans model.
    - labels (np.ndarray): Cluster labels assigned to each row in the input data.
    """
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(X_scaled)
    return model, labels