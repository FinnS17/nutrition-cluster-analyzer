from main import run_pipeline
from labeling import auto_label_cluster
from clustering import find_optimal_k
from preprocessing import load_data, calculate_macros, map_data

"""
This script is intended for manual development checks and local debugging.
It runs the pipeline on a specific dataset with fixed parameters.
Not used in production or the Streamlit app.
"""

df = load_data("data/HealthAutoExport-2025-06-06-2025-07-06 2.csv")
df_labeled, cluster_labels, best_k = run_pipeline(df, 3000, 85)
print(df_labeled['protein_g'])  