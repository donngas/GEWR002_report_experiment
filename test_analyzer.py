import pytest
import pandas as pd
import os

FPATH = "movies.csv"

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

@pytest.mark.describe("Test __init__ method (25 points)")
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
        original_df = pd.read_csv(FPATH)
        # Check only if there were missing ratings in the original file
        if original_df['Rating'].isnull().any():
            assert not analyzer.df['Rating'].isnull().any(), "Missing 'Rating' values were not handled"

@pytest.mark.describe("Test get_top_genres method (25 points)")
def test_get_top_genres(analyzer):
    """
    Tests if get_top_genres returns the correct top 3 genres based on movies.csv.
    Handles ties in genre counts.
    """
    top_3_genres = analyzer.get_top_genres(top_n=3)

    assert isinstance(top_3_genres, list), "Return type should be a list"
    assert len(top_3_genres) == 3, "List should contain top 3 genres"

    # Expected from movies.csv: Comedy (4), Action (4), Sci-Fi (3), Thriller (3)
    # Check counts
    counts = [item[1] for item in top_3_genres]
    assert counts == [4, 4, 3], f"Expected counts [4, 4, 3], but got {counts}"

    # Check genres
    # A valid top 3 must contain 'Comedy' and 'Action', and one of 'Sci-Fi' or 'Thriller'.
    genres = {item[0] for item in top_3_genres}
    assert 'Comedy' in genres, "Top genres should include 'Comedy'"
    assert 'Action' in genres, "Top genres should include 'Action'"
    assert 'Sci-Fi' in genres or 'Thriller' in genres, "Top 3 genres should include 'Sci-Fi' or 'Thriller'"

@pytest.mark.describe("Test calculate_average_by_year method (25 points)")
def test_calculate_average_by_year(analyzer):
    """
    Tests the calculation of average ratings for a specific year range.
    """
    avg_ratings = analyzer.calculate_average_by_year(start_year=2020, end_year=2021)

    assert isinstance(avg_ratings, dict), "Return type should be a dictionary"
    
    # Expected values based on movies.csv with median (8.0) imputation
    # 2020: (8.5+8.8+8.0+8.9+8.6+7.3)/6 = 8.35
    # 2021: (7.9+7.5+6.5+8.1+6.4)/5 = 7.28
    expected = {2020: 8.35, 2021: 7.28}

    assert 2020 in avg_ratings, "Average for 2020 is missing"
    assert 2021 in avg_ratings, "Average for 2021 is missing"
    assert abs(avg_ratings[2020] - expected[2020]) < 0.01, f"Average for 2020 is incorrect. Expected ~{expected[2020]}"
    assert abs(avg_ratings[2021] - expected[2021]) < 0.01, f"Average for 2021 is incorrect. Expected ~{expected[2021]}"

@pytest.mark.describe("Test visualize_yearly_rating_trend method (25 points)")
def test_visualize_yearly_rating_trend(analyzer):
    """
    Tests if the visualization file 'rating_trend.png' is created.
    """
    # Clean up previous file if it exists
    if os.path.exists("rating_trend.png"):
        os.remove("rating_trend.png")

    analyzer.visualize_yearly_rating_trend()

    assert os.path.exists("rating_trend.png"), "'rating_trend.png' was not created"
    
    # Clean up the created file
    if os.path.exists("rating_trend.png"):
        os.remove("rating_trend.png")