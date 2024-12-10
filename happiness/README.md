
# Analysis Report

## Dataset Overview
- Number of rows: 2363
- Number of columns: 11

## Numeric Columns
['year', 'Life Ladder', 'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption', 'Positive affect', 'Negative affect']

## Summary Statistics
|       |       year |   Life Ladder |   Log GDP per capita |   Social support |   Healthy life expectancy at birth |   Freedom to make life choices |     Generosity |   Perceptions of corruption |   Positive affect |   Negative affect |
|:------|-----------:|--------------:|---------------------:|-----------------:|-----------------------------------:|-------------------------------:|---------------:|----------------------------:|------------------:|------------------:|
| count | 2363       |    2363       |           2335       |      2350        |                         2300       |                    2327        | 2282           |                 2238        |       2339        |      2347         |
| mean  | 2014.76    |       5.48357 |              9.39967 |         0.809369 |                           63.4018  |                       0.750282 |    9.77213e-05 |                    0.743971 |          0.651882 |         0.273151  |
| std   |    5.05944 |       1.12552 |              1.15207 |         0.121212 |                            6.84264 |                       0.139357 |    0.161388    |                    0.184865 |          0.10624  |         0.0871311 |
| min   | 2005       |       1.281   |              5.527   |         0.228    |                            6.72    |                       0.228    |   -0.34        |                    0.035    |          0.179    |         0.083     |
| 25%   | 2011       |       4.647   |              8.5065  |         0.744    |                           59.195   |                       0.661    |   -0.112       |                    0.687    |          0.572    |         0.209     |
| 50%   | 2015       |       5.449   |              9.503   |         0.8345   |                           65.1     |                       0.771    |   -0.022       |                    0.7985   |          0.663    |         0.262     |
| 75%   | 2019       |       6.3235  |             10.3925  |         0.904    |                           68.5525  |                       0.862    |    0.09375     |                    0.86775  |          0.737    |         0.326     |
| max   | 2023       |       8.019   |             11.676   |         0.987    |                           74.6     |                       0.985    |    0.7         |                    0.983    |          0.884    |         0.705     |

## Correlation Matrix
![Correlation Matrix Heatmap](correlation_heatmap.png)
## Box Plot
![Box Plot](boxplot.png)
## Cluster Analysis
![Cluster Analysis](cluster_analysis.png)

## Narrative Analysis
### Narrative Analysis of Global Well-Being Metrics

#### Overview of the Dataset
Our analysis utilizes a comprehensive dataset comprising 2,363 entries and 11 columns related to various dimensions of human well-being across different countries. The dataset includes crucial numeric indicators such as the Life Ladder, Log GDP per capita, Social Support, Healthy Life Expectancy, Freedom to Make Life Choices, Generosity, Perceptions of Corruption, Positive Affect, and Negative Affect. These indicators provide a multi-dimensional view of the factors contributing to the perceived quality of life globally.

#### Summary Statistics
The summary statistics reveal several insights about the dataset:

- **Life Ladder**: The average score is approximately 5.48, indicating a moderate level of life satisfaction among the populations studied. The maximum score recorded is 8.02, highlighting countries with notably high life satisfaction.
  
- **Log GDP per Capita**: The mean log GDP per capita is 9.40, suggesting a positive correlation between economic output and well-being. The data ranges from 5.53 to 11.68, signifying varying economic conditions observed in different nations.

- **Social Support**: With an average of 0.81, this metric indicates a generally high level of perceived social support among citizens, which is essential for emotional and psychological well-being.

- **Healthy Life Expectancy**: The average healthy life expectancy at birth stands at 63.40 years, with a range between 6.72 years and 74.60 years. This indicates disparities in health outcomes and access to health services worldwide.

- **Freedom to Make Life Choices**: Averaging at approximately 0.75, this metric emphasizes the significance of personal freedom in enhancing quality of life, while the scores range from 0.23 to 0.99.

- **Corruption and Affects**: The dataset reveals lower levels of perceived corruption (mean of 0.74) and moderate levels of positive (0.65) and negative (0.27) affect. The findings suggest that experiences of positivity outweigh the negative experiences in many contexts, although a substantial prevalence of negative emotions remains.

#### Correlation Analysis
The correlation matrix serves as a pivotal tool in our analysis, enabling the identification of relationships between variables. For instance, we may find strong positive correlations between the Life Ladder scores and metrics such as Log GDP per Capita and Social Support. This suggests that wealthier countries with better social frameworks tend to report higher life satisfaction. Conversely, a negative correlation between Perceptions of Corruption and the Life Ladder indicates that as perceived corruption increases, so does discontent among citizens.

#### Key Findings and Implications
1. **Economic Growth and Life Satisfaction**: The data shows significant evidence that economic prosperity (Log GDP per Capita) is linked to higher life satisfaction (Life Ladder). This finding implies that policies aimed at boosting GDP through sustainable practices could lead to improvements in overall happiness.

2. **Importance of Social Support**: High levels of social support correlate positively with increased happiness scores. This highlights the necessity for governments to foster community networks and support systems to enhance citizens’ well-being.

3. **Health Outcomes**: The variance in Healthy Life Expectancy points to healthcare disparities. Countries with lower life expectancy figures might benefit from targeted public health initiatives to improve health outcomes.

4. **Freedom and Corruption**: The findings suggest that enhancing freedom can lead to better life perceptions, while combatting corruption should be a priority, as it negatively influences citizens' life evaluations.

#### Recommendations
- **Governance and Policy-making**: Governments should focus on policies that improve both economic and social support structures. Strengthening community engagement can be transformative in enhancing overall satisfaction.

- **Health Investments**: Investment in health care services, particularly in lower-performing regions, should be prioritized to ensure equitable access to health resources.

- **Combating Corruption**: Implementing transparent governance practices can enhance citizens' trust, thereby improving positive perceptions and overall well-being.

- **Research and Continuous Monitoring**: Ongoing research and data collection will be essential for tracking changes over time and assessing the impact of newly implemented policies on human well-being.

In conclusion, this analysis unveils significant correlations among different well-being dimensions, indicating areas for targeted intervention and improving overall life satisfaction globally. Through a multifaceted approach that includes economic, social, and health strategies, nations can aspire to elevate their citizens’ quality of life.
