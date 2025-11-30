import pytest
import pandas as pd
import numpy as np
import os

FPATH = "movies.csv"
FPATH = os.path.join(os.path.dirname(__file__), '..', 'movies.csv')

@pytest.fixture(scope="module")
def analyzer(module_to_test):
    """
    Pytest fixture to initialize the MovieAnalyzer from the specified module.
    This runs once per test session and is shared among all tests.
    """
    try:
        MovieAnalyzer = module_to_test.MovieAnalyzer
        instance = MovieAnalyzer(filepath=FPATH)
        return instance
    except Exception as e:
        pytest.fail(f"Failed to initialize MovieAnalyzer: {e}")

@pytest.mark.describe("Test __init__ method")
class TestInit:
    def test_df_creation(self, analyzer):
        """__init__ test 1: Data loaded into pandas DataFrame. (10 pts)"""
        assert isinstance(analyzer.df, pd.DataFrame), "analyzer.df is not a pandas DataFrame"
        assert not analyzer.df.empty, "DataFrame is empty after loading"

    def test_release_date_conversion(self, analyzer):
        """__init__ test 2: 'Release_Date' column converted to datetime. (10 pts)"""
        assert pd.api.types.is_datetime64_any_dtype(analyzer.df['Release_Date']), "'Release_Date' column is not datetime type"

    def test_rating_imputation(self, analyzer):
        """__init__ test 3: Missing 'Rating' values handled. (5 pts)"""
        original_df = pd.read_csv(FPATH) # Load original data to find what was imputed
        expected_median = original_df['Rating'].median()
        
        # Check that there are no more NaNs in the 'Rating' column
        assert not analyzer.df['Rating'].isnull().any(), "Missing 'Rating' values were not handled"
        # Check that the imputed values match the median of the original non-missing ratings
        imputed_mask = original_df['Rating'].isnull()
        assert (analyzer.df.loc[imputed_mask, 'Rating'] == expected_median).all(), f"Missing 'Rating' values should have been imputed with the median ({expected_median})"

@pytest.mark.describe("Test get_top_genres method")
class TestGetTopGenres:
    def test_get_top_genres_return_type_and_shape(self, analyzer):
        """get_top_genres test 1: Correct return type and shape. (10 pts)"""
        top_3_genres = analyzer.get_top_genres(top_n=3)
        assert isinstance(top_3_genres, list), "Return type should be a list"
        assert len(top_3_genres) == 3, "List should contain top 3 genres"
        assert all(isinstance(item, list) for item in top_3_genres), "Each item in the list should be a list (e.g., ['Genre', count])"

    def test_get_top_genres_correctness(self, analyzer):
        """get_top_genres test 2: Correct genres and counts. (15 pts)"""
        top_3_genres = analyzer.get_top_genres(top_n=3)
        # Expected from movies.csv: Comedy (4), Action (4), Sci-Fi (3), Thriller (3)
        # Check counts. The top 2 are fixed, the 3rd can be Sci-Fi or Thriller.
        counts = [item[1] for item in top_3_genres]
        assert counts == [4, 4, 3], f"Expected counts [4, 4, 3], but got {counts}"

        # Check genres
        genres = {item[0] for item in top_3_genres}
        top_2_genres = {top_3_genres[0][0], top_3_genres[1][0]}
        # Check that the top 2 genres are correct and in the correct order
        assert top_2_genres == {'Action', 'Comedy'}, "Top 2 genres should be 'Action' and 'Comedy'"
        assert top_3_genres[2][0] in ['Sci-Fi', 'Thriller'], "Third top genre should be 'Sci-Fi' or 'Thriller'"

@pytest.mark.describe("Test calculate_average_by_year method")
class TestCalculateAverageByYear:
    def test_calculate_average_by_year_return_type(self, analyzer):
        """calculate_average_by_year test 1: Correct return type. (10 pts)"""
        avg_ratings = analyzer.calculate_average_by_year(start_year=2020, end_year=2021)
        assert isinstance(avg_ratings, dict), "Return type should be a dictionary"
        assert all(isinstance(k, (int, np.integer)) for k in avg_ratings.keys()), "Dictionary keys (years) should be integers"

    def test_calculate_average_by_year_correctness(self, analyzer):
        """calculate_average_by_year test 2: Correct average calculations. (15 pts)"""
        avg_ratings = analyzer.calculate_average_by_year(start_year=2020, end_year=2021)
        # Expected values based on movies.csv with median (7.9) imputation
        # 2020: (8.5+8.8+7.9+8.9+8.6+7.3)/6 = 8.333...
        # 2021: (7.9+7.5+6.5+8.1+6.4)/5 = 7.28
        expected = {2020: 8.333333333333334, 2021: 7.28}

        assert 2020 in avg_ratings, "Average for 2020 is missing"
        assert 2021 in avg_ratings, "Average for 2021 is missing"
        assert abs(avg_ratings[2020] - expected[2020]) < 0.01, f"Average for 2020 is incorrect. Expected ~{expected[2020]}"
        assert abs(avg_ratings[2021] - expected[2021]) < 0.01, f"Average for 2021 is incorrect. Expected ~{expected[2021]}"

@pytest.mark.describe("Test visualize_yearly_rating_trend method")
def test_visualize_yearly_rating_trend(analyzer):
    """
    Tests if the visualization file 'rating_trend.png' is created. (25 pts)
    """
    # Clean up previous file if it exists
    if os.path.exists("rating_trend.png"):
        os.remove("rating_trend.png")

    analyzer.visualize_yearly_rating_trend()

    assert os.path.exists("rating_trend.png"), "'rating_trend.png' was not created"
    
    # Clean up the created file
    if os.path.exists("rating_trend.png"):
        os.remove("rating_trend.png")