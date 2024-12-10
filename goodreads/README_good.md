
# Analysis Report

## Dataset Overview
- Number of rows: 10000
- Number of columns: 23

## Numeric Columns
['book_id', 'goodreads_book_id', 'best_book_id', 'work_id', 'books_count', 'isbn13', 'original_publication_year', 'average_rating', 'ratings_count', 'work_ratings_count', 'work_text_reviews_count', 'ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5']

## Summary Statistics
|       |   book_id |   goodreads_book_id |     best_book_id |         work_id |   books_count |         isbn13 |   original_publication_year |   average_rating |    ratings_count |   work_ratings_count |   work_text_reviews_count |   ratings_1 |   ratings_2 |   ratings_3 |      ratings_4 |       ratings_5 |
|:------|----------:|--------------------:|-----------------:|----------------:|--------------:|---------------:|----------------------------:|-----------------:|-----------------:|---------------------:|--------------------------:|------------:|------------:|------------:|---------------:|----------------:|
| count |  10000    |     10000           |  10000           | 10000           |    10000      | 9415           |                    9979     |     10000        |  10000           |      10000           |                  10000    |    10000    |    10000    |     10000   | 10000          | 10000           |
| mean  |   5000.5  |         5.2647e+06  |      5.47121e+06 |     8.64618e+06 |       75.7127 |    9.75504e+12 |                    1981.99  |         4.00219  |  54001.2         |      59687.3         |                   2919.96 |     1345.04 |     3110.89 |     11475.9 | 19965.7        | 23789.8         |
| std   |   2886.9  |         7.57546e+06 |      7.82733e+06 |     1.17511e+07 |      170.471  |    4.42862e+11 |                     152.577 |         0.254427 | 157370           |     167804           |                   6124.38 |     6635.63 |     9717.12 |     28546.4 | 51447.4        | 79768.9         |
| min   |      1    |         1           |      1           |    87           |        1      |    1.9517e+08  |                   -1750     |         2.47     |   2716           |       5510           |                      3    |       11    |       30    |       323   |   750          |   754           |
| 25%   |   2500.75 |     46275.8         |  47911.8         |     1.00884e+06 |       23      |    9.78032e+12 |                    1990     |         3.85     |  13568.8         |      15438.8         |                    694    |      196    |      656    |      3112   |  5405.75       |  5334           |
| 50%   |   5000.5  |    394966           | 425124           |     2.71952e+06 |       40      |    9.78045e+12 |                    2004     |         4.02     |  21155.5         |      23832.5         |                   1402    |      391    |     1163    |      4894   |  8269.5        |  8836           |
| 75%   |   7500.25 |         9.38223e+06 |      9.63611e+06 |     1.45177e+07 |       67      |    9.78083e+12 |                    2011     |         4.18     |  41053.5         |      45915           |                   2744.25 |      885    |     2353.25 |      9287   | 16023.5        | 17304.5         |
| max   |  10000    |         3.32886e+07 |      3.55342e+07 |     5.63996e+07 |     3455      |    9.79001e+12 |                    2017     |         4.82     |      4.78065e+06 |          4.94236e+06 |                 155254    |   456191    |   436802    |    793319   |     1.4813e+06 |     3.01154e+06 |

## Correlation Matrix
![Correlation Matrix Heatmap](correlation_heatmap.png)
## Box Plot
![Box Plot](boxplot.png)
## Cluster Analysis
![Cluster Analysis](cluster_analysis.png)

## Narrative Analysis
### Books Dataset Analysis: Insights and Recommendations

#### Dataset Overview

The dataset analyzed consists of 10,000 rows and 23 columns, capturing a broad array of numerical attributes related to books in a literary database. This range includes identifiers, publication details, and various metrics pertinent to book ratings and reviews. The numeric columns present vital information such as the book's unique IDs, its publication year, average ratings, count of ratings, and distribution of ratings across different tiers (1 to 5 stars).

#### Summary Statistics

The summary statistics reveal critical insights into the nature of the data:

- **Publication Year:** The `original_publication_year` ranges from as early as 1750 to as recent as 2017, indicating a diverse collection of both classic and contemporary works. The average publication year is roughly 1982, suggesting a skew towards books published late in the 20th century.

- **Ratings:** The average book rating is approximately 4.00 out of 5, which is indicative of a generally positive reception among readers. However, the standard deviation (0.25) suggests variability in how different titles are perceived by readers.

- **Ratings Distribution:** There are significant numbers in both lower and upper ratings, particularly with the maximum ratings (5 stars), showing a diverse range of opinions. For example, the highest number of 5-star ratings sums up to over 3 million but the number of 1-star ratings is still significant (~155k), indicating that while many readers are pleased, differences in opinion exist.

- **Review Counts:** The dataset also shows that the books collectively received considerable attention, as seen from the `ratings_count` and `work_ratings_count` statistics. On average, books have around 54,000 ratings, further substantiating their popularity.

#### Correlation Matrix Insights

A correlation heatmap was generated for the numeric attributes, which is crucial for uncovering relationships among variables. For instance, an observable positive correlation exists between `average_rating` and `ratings_count`. This suggests that books with more ratings tend to have higher average ratings, potentially indicating that more feedback accumulates around titles that resonate with many readers.

Conversely, a negative correlation might be seen between the count of lower star ratings and the average rating, indicating that books with more lower ratings typically fare worse in average evaluations. Such correlations provide guidance for targeted strategies in marketing and acquisition, such as focusing efforts on promoting highly-rated but low-rated-count books to improve visibility.

#### Key Findings and Implications

1. **High Average Ratings:** The overall positive sentiment towards the books suggests effective audience engagement and quality content. This can be leveraged for marketing campaigns that highlight these titles’ high ratings and positive reviews.

2. **Diversity in Ratings:** The variability in ratings signifies differing reader demographics and preferences. Understanding these segments can help in tailoring promotions towards specific audiences who favor certain genres or authors.

3. **Classic vs. Contemporary:** The inclusion of both classic literature and contemporary books opens opportunities to cross-promote. Titles reviewed positively by readers interested in one category could be suggested to those engaged in another, cultivating broader reader interest.

4. **Utilization of Review Counts:** Titles with high reviews yet lower ratings may need attention in terms of customer engagement or author outreach strategies to elevate their perceived value. This includes encouraging readers to write positive reviews or addressing the common themes in lower ratings to enhance the reading experience.

#### Recommendations

- **Targeted Marketing:** Use the ratings and review data to conduct focused marketing centered on high-rated books with a lower ratings count to draw in new readers.

- **Reader Engagement Programs:** Initiate programs like "read and review" campaigns to encourage more feedback, particularly for books with high potential but lower engagement metrics.

- **Analyzing Popularity Trends:** Continue monitoring rating trends over time, particularly for new releases, to capitalize on shifting viewing habits.

- **Segmentation of Offerings:** Develop marketing strategies that cater to different reader demographics based on the patterns revealed in the ratings and their correlational insights.

Overall, the analysis of this dataset presents not only current trends in reader preferences but also strategic insights that could guide future actions in marketing, inventory acquisition, and reader engagement. By understanding the diverse nature of book ratings and their implications, stakeholders can make data-informed decisions that reflect the realities of the literary marketplace.