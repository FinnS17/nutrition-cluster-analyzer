from preprocessing import load_data, calculate_macros, select_features
from clustering import standardize_features, find_optimal_k, run_kmeans
from visualization import plot_feature_distributions
from labeling import auto_label_cluster
import os
import yaml

# Step 1: Determine the path to the config.yaml file relative to main.py
config_path = os.path.join(
    os.path.dirname(__file__),  # path to the main.py file
    "..",                       # go one directory up
    "config",                   # into the "config" folder
    "config.yaml"               # the file itself
)

# Step 2: Open and load the config.yaml file
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

def run_pipeline(df, maintenance_kcal, bodyweight_kg, config):
    """
    Runs the full nutrition clustering pipeline: macro calculation, feature extraction,
    standardization, k-means clustering, and automatic cluster labeling.

    Parameters:
    - df (pd.DataFrame): Input dataframe with nutrition data.
    - maintenance_kcal (float): User's estimated maintenance calorie intake.
    - bodyweight_kg (float): User's bodyweight in kilograms.
    - config (dict): Configuration dictionary loaded from YAML.

    Returns:
    - df_labeled (pd.DataFrame): The original dataframe with added cluster and label columns.
    - cluster_labels (dict): Mapping of cluster index to descriptive label.
    - best_k (int): Optimal number of clusters determined via Elbow method.
    """
    df = calculate_macros(df)
    features = select_features(df)
    X_scaled = standardize_features(features)
    best_k = find_optimal_k(X_scaled, k_range=(2, 8)) 
    model, labels = run_kmeans(X_scaled, n_clusters=best_k)
    df['cluster'] = labels
    df_labeled, cluster_labels = auto_label_cluster(df, maintenance_kcal, bodyweight_kg, config)
    return df_labeled, cluster_labels, best_k

if __name__ == "__main__":
    # Load a CSV file containing nutrition data
    df = load_data("data/diet_data.csv")  # adjust path if necessary

    # Run the full pipeline
    df_labeled, cluster_labels, best_k = run_pipeline(df, 3000, 85, config)

    # Output cluster labels and a preview of the labeled dataset
    cluster_means = df_labeled.groupby("cluster")[["kcal", "protein_g", "carb_g", "fat_g"]].mean()
    print(cluster_labels)
    print(df_labeled.head(50))