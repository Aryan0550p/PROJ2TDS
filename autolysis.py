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
from scipy.stats import ttest_ind
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

    heatmap_file = None
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Matrix Heatmap")
        heatmap_file = "correlation_heatmap.png"
        plt.savefig(heatmap_file)
        plt.close()
        print(f"Saved correlation heatmap as {heatmap_file}")

    histograms_file = "histograms.png"
    plt.figure(figsize=(15, len(numeric_cols) * 4))
    for i, col in enumerate(numeric_cols):
        plt.subplot(len(numeric_cols), 1, i + 1)
        sns.histplot(df[col].dropna(), kde=True, bins=20, color='blue')
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(histograms_file)
    plt.close()
    print(f"Saved histograms as {histograms_file}")

    cluster_file = None
    if len(numeric_cols) > 1:
        kmeans = KMeans(n_clusters=3, random_state=42)
        cluster_data = df[numeric_cols].dropna()
        clusters = kmeans.fit_predict(cluster_data)

        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(cluster_data)
        cluster_df = pd.DataFrame(reduced_data, columns=["PCA1", "PCA2"])
        cluster_df["Cluster"] = clusters

        plt.figure(figsize=(10, 8))
        sns.scatterplot(x="PCA1", y="PCA2", hue="Cluster", data=cluster_df, palette="viridis")
        plt.title("Cluster Analysis (PCA Reduced)")
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")
        cluster_file = "cluster_analysis.png"
        plt.savefig(cluster_file)
        plt.close()
        print(f"Saved cluster analysis plot as {cluster_file}")

    dataset_overview = {
        "Number of rows": df.shape[0],
        "Number of columns": df.shape[1],
        "Numeric Columns": list(numeric_cols),
    }

    summary_stats_table = tabulate(summary_stats, headers='keys', tablefmt='pipe')

    narrative = generate_llm_narrative(dataset_overview, summary_stats_table, heatmap_file, outliers, t_test_results)

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

def generate_llm_narrative(overview, summary_stats, heatmap_file, outliers, t_tests):
    try:
        prompt = (
            "You are a data analyst. Write a clear, insightful narrative based on the following analysis:\n\n"
            f"### Dataset Overview\n{overview}\n\n"
            f"### Summary Statistics\n{summary_stats}\n\n"
            f"### Outliers\n{outliers}\n\n"
            f"### Hypothesis Testing\n{t_tests}\n\n"
        )

        if heatmap_file:
            prompt += (
                "### Correlation Matrix\n"
                "A correlation heatmap was generated. Discuss its importance in finding relationships between numeric variables.\n"
            )

        prompt += "\nDiscuss key findings, potential implications, and recommendations based on this data."

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
        print(f"Error generating narrative: {e}")
        return "An error occurred while generating the narrative."

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <csv_filename>")
    else:
        csv_filename = sys.argv[1]
        analyze_and_generate_report(csv_filename)
