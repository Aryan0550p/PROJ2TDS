# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "chardet",
#     "matplotlib",
#     "pandas",
#     "python-dotenv",
#     "requests",
#     "openai==0.28.0",
#     "scikit-learn",
#     "tabulate",
#     "fastapi",
#     "uvicorn",
#     "seaborn",
# ]
# ///
import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_selection import mutual_info_regression
from scipy.stats import ttest_ind, ttest_1samp
from tabulate import tabulate

load_dotenv()

if "AIPROXY_TOKEN" not in os.environ:
    raise EnvironmentError("The environment variable 'AIPROXY_TOKEN' must be set.")

openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
openai.api_key = os.environ["AIPROXY_TOKEN"]

def detect_outliers(df, cols):
    """Detect outliers using the IQR method."""
    outliers = {}
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers[col] = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)].shape[0]
    return outliers

def hypothesis_testing(df, cols):
    """Perform t-tests between numeric columns."""
    results = {}
    for i, col1 in enumerate(cols):
        for col2 in cols[i + 1:]:
            stat, p_value = ttest_ind(df[col1].dropna(), df[col2].dropna())
            results[f"{col1} vs {col2}"] = p_value
    return results

def one_sample_ttest(df, cols, population_mean):
    """Perform one-sample t-tests comparing each column's mean to a population mean."""
    results = {}
    for col in cols:
        stat, p_value = ttest_1samp(df[col].dropna(), population_mean)
        results[col] = p_value
    return results

def feature_importance(df, target_col):
    """Calculate feature importance using mutual information regression."""
    if target_col not in df.columns:
        print(f"Target column '{target_col}' not found in the dataset.")
        return {}

    features = df.drop(columns=[target_col]).select_dtypes(include=['float64', 'int64'])
    target = df[target_col]
    if features.empty:
        print("No numeric features found for mutual information calculation.")
        return {}

    mi_scores = mutual_info_regression(features, target, discrete_features=False)
    importance = {col: score for col, score in zip(features.columns, mi_scores)}
    return importance

def save_plot(file_name, plot_func, *args, **kwargs):
    """Generic function to save a plot."""
    try:
        plot_func(*args, **kwargs)
        plt.savefig(file_name)
        plt.close()
        print(f"Saved plot as {file_name}")
        return file_name
    except Exception as e:
        print(f"Error saving plot {file_name}: {e}")
        return None

def generate_section_narrative(section_title, data):
    """Generate a narrative for a specific section using the LLM."""
    try:
        prompt = f"Discuss the following {section_title} in detail:\n\n{data}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful data analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating narrative for {section_title}: {e}")
        return "Error in generating narrative."

def analyze_and_generate_report(csv_filename):
    try:
        df = pd.read_csv(csv_filename, encoding='ISO-8859-1')
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return

    print("Dataset Info:")
    print(df.info())
    print("\nSample Data:")
    print(df.head())

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    print(f"\nNumeric Columns: {list(numeric_cols)}")

    summary_stats = df[numeric_cols].describe()
    print("\nSummary Statistics:")
    print(summary_stats)

    outliers = detect_outliers(df, numeric_cols)
    print("\nOutliers Detected:")
    print(outliers)

    t_test_results = hypothesis_testing(df, numeric_cols)
    print("\nHypothesis Testing Results:")
    print(t_test_results)

    one_sample_results = one_sample_ttest(df, numeric_cols, population_mean=0)
    print("\nOne-Sample T-Test Results (Population Mean = 0):")
    print(one_sample_results)

    feature_imp = feature_importance(df, target_col=numeric_cols[0])
    print("\nFeature Importance:")
    print(feature_imp)

    heatmap_file = None
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        heatmap_file = save_plot("correlation_heatmap.png", sns.heatmap, corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")

    histograms_file = save_plot("histograms.png", lambda: [sns.histplot(df[col].dropna(), kde=True, bins=20, color='blue') or plt.title(f"Distribution of {col}") or plt.xlabel(col) or plt.ylabel("Frequency") for col in numeric_cols])

    cluster_file = None
    if len(numeric_cols) > 1:
        kmeans = KMeans(n_clusters=3, random_state=42)
        cluster_data = df[numeric_cols].dropna()
        clusters = kmeans.fit_predict(cluster_data)

        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(cluster_data)
        cluster_df = pd.DataFrame(reduced_data, columns=["PCA1", "PCA2"])
        cluster_df["Cluster"] = clusters

        cluster_file = save_plot("cluster_analysis.png", sns.scatterplot, x="PCA1", y="PCA2", hue="Cluster", data=cluster_df, palette="viridis")

    dataset_overview = {
        "Number of rows": df.shape[0],
        "Number of columns": df.shape[1],
        "Numeric Columns": list(numeric_cols),
    }

    summary_stats_table = tabulate(summary_stats, headers='keys', tablefmt='pipe')

    narrative = ""
    narrative += generate_section_narrative("Dataset Overview", dataset_overview)
    narrative += generate_section_narrative("Summary Statistics", summary_stats_table)
    narrative += generate_section_narrative("Outliers", outliers)
    narrative += generate_section_narrative("Hypothesis Testing", t_test_results)

    markdown_content = f"""
# Analysis Report

## Dataset Overview
- Number of rows: {df.shape[0]}
- Number of columns: {df.shape[1]}

## Numeric Columns
{list(numeric_cols)}

## Summary Statistics
{summary_stats_table}

"""

    if heatmap_file:
        markdown_content += "## Correlation Matrix\n"
        markdown_content += f"![Correlation Matrix Heatmap]({heatmap_file})\n"

    markdown_content += f"## Histograms\n![Histograms]({histograms_file})\n"

    if cluster_file:
        markdown_content += f"## Cluster Analysis\n![Cluster Analysis]({cluster_file})\n"

    markdown_content += "\n## Narrative Analysis\n"
    markdown_content += narrative

    with open("README.md", "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)
    print("Generated README.md report.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <csv_filename>")
    else:
        csv_filename = sys.argv[1]
        analyze_and_generate_report(csv_filename)
