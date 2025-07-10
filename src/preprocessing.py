import pandas as pd

def load_data(path):
    """
    Load a CSV file from the specified path.

    Parameters:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data.
    """
    df = pd.read_csv(path)
    return df

def map_data(df):
    """
    Standardize and rename columns for consistent processing.
    
    Converts column names to lowercase, strips whitespace, and applies
    mapping to unify different naming conventions. Also converts kJ to kcal if needed.

    Parameters:
        df (pd.DataFrame): Raw input data.

    Returns:
        pd.DataFrame: Processed data with renamed columns.
    """
    df.columns = df.columns.str.strip().str.lower()

    COLUMN_MAPPING = {
        "dietary energy (kj)": "kcal",
        "protein (g)": "protein_g",
        "carbohydrates (g)": "carb_g",
        "total fat (g)": "fat_g",
        "date": "date",  # optional
    }

    if "dietary energy (kj)" in df.columns:
        df["dietary energy (kj)"] = df["dietary energy (kj)"] / 4.184  # convert kJ to kcal

    df.rename(columns={col: COLUMN_MAPPING.get(col, col) for col in df.columns}, inplace=True)
    return df

def calculate_macros(df):
    """
    Calculate macro calorie contributions and percentages.

    Removes missing rows, maps columns, and computes:
    - kcal from protein, carbs, and fat
    - total kcal from macros
    - percentage share of each macronutrient

    Parameters:
        df (pd.DataFrame): Input DataFrame with nutritional values.

    Returns:
        pd.DataFrame: Enhanced DataFrame with macro calories and percentages.
    """
    df.dropna(inplace=True)
    df = map_data(df)

    df['protein_kcal'] = df['protein_g'] * 4
    df['carb_kcal'] = df['carb_g'] * 4
    df['fat_kcal'] = df['fat_g'] * 9

    df['total_macro_kcal'] = df['protein_kcal'] + df['carb_kcal'] + df['fat_kcal']

    df['protein_pct'] = df['protein_kcal'] / df['total_macro_kcal']
    df['carb_pct'] = df['carb_kcal'] / df['total_macro_kcal']
    df['fat_pct'] = df['fat_kcal'] / df['total_macro_kcal']

    return df

def select_features(df):
    """
    Select final features for clustering analysis.

    Includes total kcal and macronutrient percentage contributions.

    Parameters:
        df (pd.DataFrame): DataFrame with computed macros.

    Returns:
        pd.DataFrame: DataFrame with selected features.
    """
    return df[['kcal', 'protein_pct', 'carb_pct', 'fat_pct']]