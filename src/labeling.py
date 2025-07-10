def auto_label_cluster(df, maintenance_kcal, bodyweight_kg, config):
    """
    Automatically assigns descriptive labels to each cluster based on average nutritional values
    compared to user-specific thresholds and configuration settings.

    Parameters:
    - df (pd.DataFrame): DataFrame that includes a 'cluster' column for each day.
    - maintenance_kcal (float): User's daily maintenance calorie requirement.
    - bodyweight_kg (float): User's bodyweight in kilograms.
    - config (dict): Configuration dictionary containing threshold values for labeling.

    Returns:
    - df (pd.DataFrame): Original DataFrame with an added 'cluster_label' column.
    - cluster_labels (dict): Mapping from cluster index to human-readable labels.
    """
    cluster_means = df.groupby("cluster")[["kcal", "protein_g", "carb_g", "fat_g"]].mean()
    
    thresholds = config["labeling"]
    kcal_thresholds = thresholds["kcal_thresholds"]
    
    cluster_labels = {}
    for cluster_id, row in cluster_means.iterrows():
        parts = []

        # Calories
        ratio = row["kcal"] / maintenance_kcal
        if ratio < kcal_thresholds["hard_cut"]:
            parts.append("hohes Defizit")
        elif ratio < kcal_thresholds["cut"]:
            parts.append("moderates Defizit")
        elif ratio < kcal_thresholds["maintain"]:
            parts.append("Erhaltungskalorien")
        elif ratio < kcal_thresholds["lean_bulk"]:
            parts.append("moderater Überschuss")
        else:
            parts.append("hoher Überschuss")

        # Protein
        protein_per_kg = row["protein_g"] / bodyweight_kg
        if protein_per_kg < thresholds["protein_per_kg"]["low"]:
            parts.append("Low Protein")
        elif protein_per_kg > thresholds["protein_per_kg"]["high"]:
            parts.append("High Protein")
        else:
            parts.append("Medium Protein")

        # Fat
        fat_per_kg = row["fat_g"] / bodyweight_kg
        if fat_per_kg < thresholds["fat_per_kg"]["low"]:
            parts.append("Low Fat")
        elif fat_per_kg > thresholds["fat_per_kg"]["high"]:
            parts.append("High Fat")
        else:
            parts.append("Medium Fat")

        # Carbohydrates
        carb_per_kg = row["carb_g"] / bodyweight_kg
        if carb_per_kg < thresholds["carb_per_kg"]["low"]:
            parts.append("Low Carb")
        elif carb_per_kg > thresholds["carb_per_kg"]["high"]:
            parts.append("High Carb")
        else:
            parts.append("Medium Carb")

        # Combine parts into a full label
        cluster_labels[cluster_id] = ", ".join(parts)

    # Assign labels to the original DataFrame
    df["cluster_label"] = df["cluster"].map(cluster_labels)
    return df, cluster_labels