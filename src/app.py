"""
Streamlit app for clustering and analyzing daily nutrition logs.

Features:
- Manual or calculated maintenance calorie input
- Upload of nutrition CSV file (macronutrients)
- Clustering of eating patterns
- Intelligent labeling (e.g., "High Protein, Caloric Surplus")
- Pie chart visualization of pattern distribution
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import yaml

from main import run_pipeline  # Main logic (preprocessing, clustering, labeling)
from calorie_calculator import calculate_maintenance_kcal

# ------------------ Load Config ------------------ #
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml"))

if not os.path.exists(config_path):
    st.error("❌ Configuration file not found.")
    st.stop()

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# ------------------ App Layout ------------------ #
st.set_page_config(page_title="Nutrition Clustering", layout="centered")
st.title("🥗 Nutrition Pattern Analyzer")

st.subheader("🔢 Enter or Calculate Your Maintenance Calories")

use_calculator = st.checkbox("I don't know my daily calorie needs – please calculate")

if use_calculator:
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    sex = st.radio("Sex", ["Männlich", "Weiblich"])
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=180)
    bodyweight_kg = st.number_input("Weight (kg)", min_value=30, max_value=200, value=80)
    activity_level = st.selectbox("Activity Level", [
        "Sitzend", "Leicht aktiv", "Moderat aktiv", "Sehr aktiv", "Extrem aktiv"
    ])
    maintenance_kcal = calculate_maintenance_kcal(age, sex, height, bodyweight_kg, activity_level)
    st.success(f"Your estimated maintenance calories: **{maintenance_kcal} kcal/day**")

else:
    maintenance_kcal = st.number_input("Enter your maintenance calories (kcal/day)", min_value=1000, max_value=6000, value=2500, step=50)
    bodyweight_kg = st.number_input("⚖️ Current Bodyweight (kg)", min_value=30, max_value=200, value=80, step=1)

# ------------------ File Upload ------------------ #
st.markdown("---")
st.info("""
⬇️ Please upload a CSV file with your nutrition data.  
Expected columns (case-insensitive, flexible order):

- `date`
- `kcal`  
- `protein_g`  
- `carb_g`  
- `fat_g`

Alternatively supported columns (will be auto-mapped):
- `dietary Energy (kJ)`
- `protein (g)`
- `carbohydrates (g)`
- `total Fat (g)`
""")


uploaded_file = st.file_uploader("📄 Upload CSV File", type="csv")

# ------------------ Analysis Logic ------------------ #
def run_analysis(df, maintenance_kcal, bodyweight_kg, config):
    result_df, cluster_labels, best_k = run_pipeline(df, maintenance_kcal, bodyweight_kg, config)
    
    st.subheader("🔎 Analysis Results")
    st.markdown(f"##### The AI has detected **{best_k}** typical nutrition patterns (sorted by frequency):")

    cluster_counts = result_df['cluster'].value_counts(normalize=True) * 100
    for key in cluster_counts.index:
        st.write(f"**Pattern {key+1}:** {cluster_labels[key]} — **{cluster_counts[key]:.1f}%** of days")

    # Pie chart
    fig, ax = plt.subplots()
    ax.pie(
        cluster_counts.values,
        labels=[cluster_labels[i] for i in cluster_counts.index],
        autopct='%1.1f%%',
        startangle=90,
        counterclock=False
    )
    ax.axis('equal')
    st.markdown("##### 📊 Distribution of Nutrition Patterns")
    st.pyplot(fig)

    if st.checkbox("✅ Show full daily data with assigned pattern:"):
        st.dataframe(result_df[["date", "kcal", "protein_g", "carb_g", "fat_g", "cluster_label"]])

# ------------------ Run if file uploaded ------------------ #
if uploaded_file:
    df = pd.read_csv(uploaded_file) #, sep=";", if necessary
    run_analysis(df, maintenance_kcal, bodyweight_kg, config)