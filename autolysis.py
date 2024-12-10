import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from tabulate import tabulate

# Set the AI Proxy token
os.environ["AIPROXY_TOKEN"] = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDAyMzdAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.efA4RgOA0zV-WTF8lxfwGqMYrIPD02PjkCEWIyE7CNQ"  # Replace with actual token
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"  # Ensure the correct API base
openai.api_key = os.environ["AIPROXY_TOKEN"]

def analyze_and_generate_report(csv_filename):
    # Load the dataset
    try:
        df = pd.read_csv(csv_filename, encoding='ISO-8859-1')
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return

    # Display basic dataset info
    print("Dataset Info:")
    print(df.info())
    print("\nSample Data:")
    print(df.head())

    # Handle numeric columns (conversion and cleaning)
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    print(f"\nNumeric Columns: {list(numeric_cols)}")

    # Compute summary statistics
    summary_stats = df[numeric_cols].describe()
    print("\nSummary Statistics:")
    print(summary_stats)

    # Create correlation matrix
    heatmap_file = None
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()

        # Save the correlation matrix heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Matrix Heatmap")
        heatmap_file = "correlation_heatmap.png"
        plt.savefig(heatmap_file)
        plt.close()
        print(f"Saved correlation heatmap as {heatmap_file}")
    else:
        print("Not enough numeric columns for correlation analysis.")

    # Outlier detection visualization
    boxplot_file = "boxplot.png"
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df[numeric_cols], orient="h")
    plt.title("Box Plot for Numeric Columns")
    plt.savefig(boxplot_file)
    plt.close()
    print(f"Saved box plot as {boxplot_file}")

    # Cluster analysis visualization
    cluster_file = None
    if len(numeric_cols) > 1:
        # Perform clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        cluster_data = df[numeric_cols].dropna()
        clusters = kmeans.fit_predict(cluster_data)

        # Dimensionality reduction for visualization
        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(cluster_data)
        cluster_df = pd.DataFrame(reduced_data, columns=["PCA1", "PCA2"])
        cluster_df["Cluster"] = clusters

        # Scatter plot of clusters
        plt.figure(figsize=(10, 8))
        sns.scatterplot(x="PCA1", y="PCA2", hue="Cluster", data=cluster_df, palette="viridis")
        plt.title("Cluster Analysis (PCA Reduced)")
        cluster_file = "cluster_analysis.png"
        plt.savefig(cluster_file)
        plt.close()
        print(f"Saved cluster analysis plot as {cluster_file}")

    # Prepare data for LLM narrative
    dataset_overview = {
        "Number of rows": df.shape[0],
        "Number of columns": df.shape[1],
        "Numeric Columns": list(numeric_cols),
    }

    summary_stats_table = tabulate(summary_stats, headers='keys', tablefmt='pipe')

    # Generate LLM-based narrative
    narrative = generate_llm_narrative(dataset_overview, summary_stats_table, heatmap_file)

    # Generate Markdown report
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

    markdown_content += f"## Box Plot\n![Box Plot]({boxplot_file})\n"

    if cluster_file:
        markdown_content += f"## Cluster Analysis\n![Cluster Analysis]({cluster_file})\n"

    markdown_content += "\n## Narrative Analysis\n"
    markdown_content += narrative

    # Save Markdown report
    with open("README.md", "w") as md_file:
        md_file.write(markdown_content)
    print("Generated README.md report.")

def generate_llm_narrative(overview, summary_stats, heatmap_file):
    try:
        # Prepare the prompt for the LLM
        prompt = (
            "You are a data analyst. Write a clear, insightful narrative based on the following analysis:\n\n"
            f"### Dataset Overview\n{overview}\n\n"
            f"### Summary Statistics\n{summary_stats}\n\n"
        )

        if heatmap_file:
            prompt += (
                "### Correlation Matrix\n"
                "A correlation heatmap was generated. Mention its importance in finding relationships between numeric variables.\n"
            )

        prompt += "\nDiscuss key findings, potential implications, and recommendations based on this data."

        # Call the LLM
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use the supported model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

       # Extract the response text
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating narrative: {e}")
        return "An error occurred while generating the narrative."


# Run the analysis on the uploaded CSV file
csv_filename = "happiness.csv"  # Replace with the actual filename if necessary
analyze_and_generate_report(csv_filename)
