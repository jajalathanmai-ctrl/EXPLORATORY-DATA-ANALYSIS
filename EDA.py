import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set visual style for plots
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)


# ==========================================
# 1. LOAD DATASET
# ==========================================
def load_data():
    """Loads the built-in 'Tips' dataset from Seaborn."""
    print("--- STEP 1: Loading Dataset ---")
    df = sns.load_dataset("tips")
    print(f"Dataset successfully loaded with {df.shape[0]} rows and {df.shape[1]} columns.\n")
    return df


# ==========================================
# 2. DATA PROFILING & QUALITY CHECK
# ==========================================
def profile_data(df):
    """Inspects the structural health, data types, and missing values."""
    print("--- STEP 2: Data Profiling & Structural Overview ---")

    print("\n[First 5 Rows]:")
    print(df.head())

    print("\n[Data Types and Missing Values Summary]:")
    print(df.info())

    print("\n[Missing Values Check Per Column]:")
    print(df.isnull().sum())

    print("\n[Unique Values Count for Categorical Columns]:")
    for col in df.select_dtypes(include=["category", "object"]).columns:
        print(f" - {col}: {df[col].nunique()} unique categories")
    print("\n")


# ==========================================
# 3. STATISTICAL SUMMARIES
# ==========================================
def summarize_statistics(df):
    """Generates numerical and categorical descriptive statistics."""
    print("--- STEP 3: Statistical Summary ---")

    print("\n[Descriptive Statistics for Numerical Features]:")
    print(df.describe().T)

    print("\n[Descriptive Statistics for Categorical Features]:")
    print(df.describe(include=["category", "object"]).T)
    print("\n")


# ==========================================
# 4. UNIVARIATE ANALYSIS (Visualizing Trends)
# ==========================================
def run_univariate_plots(df):
    """Analyzes the distribution of individual columns."""
    print("--- STEP 4: Plotting Univariate Distributions ---")
    os.makedirs("eda_outputs", exist_ok=True)

    # Plot 1: Target distribution (Total Bill vs Tips)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df["total_bill"], kde=True, ax=axes[0], color="skyblue")
    axes[0].set_title("Distribution of Total Bill Amounts")

    sns.histplot(df["tip"], kde=True, ax=axes[1], color="salmon")
    axes[1].set_title("Distribution of Tip Amounts")
    plt.tight_layout()
    plt.savefig("eda_outputs/01_univariate_numerical.png")
    plt.close()

    # Plot 2: Categorical distributions
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.countplot(x="day", data=df, ax=axes[0], palette="Set2")
    axes[0].set_title("Traffic Count by Day of Week")

    sns.countplot(x="time", data=df, ax=axes[1], palette="Set1")
    axes[1].set_title("Traffic Count by Meal Time")
    plt.tight_layout()
    plt.savefig("eda_outputs/02_univariate_categorical.png")
    plt.close()
    print("Saved univariate distribution plots to 'eda_outputs/' directory.\n")


# ==========================================
# 5. BIVARIATE & MULTIVARIATE ANALYSIS
# ==========================================
def run_multivariate_plots(df):
    """Explores interactions and distributions across multiple dimensions."""
    print("--- STEP 5: Plotting Relationships & Trends ---")

    # Plot 3: Categorical impact on numeric goals
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(
        x="day", y="total_bill", hue="smoker", data=df, ax=axes[0], palette="Pastel1"
    )
    axes[0].set_title("Total Bill Distribution by Day & Smoking Status")

    sns.barplot(x="time", y="tip", hue="sex", data=df, ax=axes[1], palette="muted")
    axes[1].set_title("Average Tip by Time of Day & Gender")
    plt.tight_layout()
    plt.savefig("eda_outputs/03_bivariate_analysis.png")
    plt.close()

    # Plot 4: Scatter Plot (Total Bill vs Tip by Size)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x="total_bill",
        y="tip",
        hue="time",
        size="size",
        sizes=(20, 200),
        data=df,
        palette="viridis",
    )
    plt.title("Tip vs Total Bill mapped with Dining Size & Time")
    plt.savefig("eda_outputs/04_scatter_interaction.png")
    plt.close()
    print("Saved multidimensional relationship plots to 'eda_outputs/' directory.\n")


# ==========================================
# 6. CORRELATION & INFLUENCE ANALYSIS
# ==========================================
def analyze_correlations(df):
    """Calculates numerical matrix and uncovers underlying data dependencies."""
    print("--- STEP 6: Correlation Analysis ---")

    # Filter out only the purely numeric types for correlation mapping
    numeric_df = df.select_dtypes(include=[np.number])

    correlation_matrix = numeric_df.corr()
    print("\n[Pearson Correlation Matrix]:")
    print(correlation_matrix)

    # Heatmap visualization
    plt.figure(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
    plt.title("Correlation Heatmap of Numeric Variables")
    plt.tight_layout()
    plt.savefig("eda_outputs/05_correlation_matrix.png")
    plt.close()
    print("\nSaved correlation matrix plot to 'eda_outputs/' directory.\n")


# ==========================================
# 7. EXECUTABLE WORKFLOW
# ==========================================
if __name__ == "__main__":
    # Run pipeline
    data = load_data()
    profile_data(data)
    summarize_statistics(data)
    run_univariate_plots(data)
    run_multivariate_plots(data)
    analyze_correlations(data)

    print("=====================================================")
    print("EDA PIPELINE COMPLETE: Visual outputs are saved inside 'eda_outputs/'")
    print("=====================================================")