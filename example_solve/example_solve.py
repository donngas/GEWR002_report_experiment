import pandas as pd
import matplotlib.pyplot as plt

class MovieAnalyzer:
    """
    Analyzes and visualizes movie ratings data from a CSV file.
    """

    def __init__(self, filepath):
        """
        Initializes the MovieAnalyzer.

        - Reads data from the given CSV file.
        - Converts the 'Release_Date' column to datetime objects.
        - Fills missing 'Rating' values with the median of the column.
        """
        self.df = pd.read_csv(filepath)
        self.df['Release_Date'] = pd.to_datetime(self.df['Release_Date'])
        median_rating = self.df['Rating'].median()
        self.df['Rating'] = self.df['Rating'].fillna(median_rating)

    def get_top_genres(self, top_n):
        """
        Calculates the top N genres by movie frequency.

        - Excludes movies with missing genre information.
        - Returns a list of lists, e.g., [['Genre1', count1], ['Genre2', count2]].
        """
        genre_counts = self.df['Genre'].dropna().value_counts().head(top_n)
        top_genres_list = [[genre, int(count)] for genre, count in genre_counts.items()]
        return top_genres_list

    def calculate_average_by_year(self, start_year, end_year):
        """
        Calculates the average movie rating for each year within a specified range.

        - Filters movies released between start_year and end_year (inclusive).
        - Returns a dictionary, e.g., {year1: avg_rating1, year2: avg_rating2}.
        """
        # Drop rows where Release_Date is NaT before filtering by year
        df_with_dates = self.df.dropna(subset=['Release_Date'])
        
        mask = df_with_dates['Release_Date'].dt.year.between(start_year, end_year)
        filtered_df = df_with_dates[mask]

        avg_ratings = filtered_df.groupby(filtered_df['Release_Date'].dt.year)['Rating'].mean()
        return avg_ratings.to_dict()

    def visualize_yearly_rating_trend(self):
        """
        Creates and saves a line graph of the average rating trend by year.

        - Calculates the average rating for all years in the dataset.
        - Saves the plot as 'rating_trend.png'.
        - Does not return any value.
        """
        yearly_avg_rating = self.df.groupby(self.df['Release_Date'].dt.year)['Rating'].mean()
        
        plt.figure(figsize=(10, 6))
        yearly_avg_rating.plot(kind='line', marker='o')
        plt.title('Yearly Average Movie Rating Trend')
        plt.xlabel('Year')
        plt.ylabel('Average Rating')
        plt.grid(True)
        plt.savefig('rating_trend.png')
        plt.close()