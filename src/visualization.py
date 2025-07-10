import matplotlib.pyplot as plt
import seaborn as sns

def plot_feature_distributions(df):
    """
    Plot the distribution of nutritional features per cluster using boxplots.

    This function visualizes how different clusters differ with respect to
    calorie intake and macronutrient amounts (protein, carbohydrates, fat).

    Parameters:
        df (pd.DataFrame): DataFrame containing the features and cluster assignments.

    Returns:
        None
    """
    features = ["kcal", "protein_g", "carb_g", "fat_g"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, feature in enumerate(features):
        sns.boxplot(
            x="cluster",
            y=feature,
            data=df,
            palette="tab10",
            ax=axes[i]
        )
        axes[i].set_title(f"{feature} by Cluster")
        axes[i].set_xlabel("Cluster")
        axes[i].set_ylabel(feature.capitalize())
        axes[i].grid(True)

    plt.tight_layout()
    plt.show()
