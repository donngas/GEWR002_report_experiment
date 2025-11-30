#from .analyzer import MovieAnalyzer
import os
import pandas as pd
from mock_solve import MovieAnalyzer
from loguru import logger

FPATH = "movies.csv"

if __name__ == "__main__":
    total_score = 0
    max_score = 100
    
    print("--- Starting MovieAnalyzer Test ---")

    # Test __init__ method (25 points)
    print("\n[Testing __init__]")
    try:
        analyzer = MovieAnalyzer(filepath=FPATH)
        init_score = 0
        
        # 1. Read data (10 points)
        if isinstance(analyzer.df, pd.DataFrame) and not analyzer.df.empty:
            init_score += 10
            print("  - [PASS] Data loaded into pandas DataFrame. (+10 pts)")
        else:
            print("  - [FAIL] Data not loaded correctly.")

        # 2. Convert Release_Date to datetime (10 points)
        if pd.api.types.is_datetime64_any_dtype(analyzer.df['Release_Date']):
            init_score += 10
            print("  - [PASS] 'Release_Date' column converted to datetime. (+10 pts)")
        else:
            print("  - [FAIL] 'Release_Date' column is not datetime type.")

        # 3. Handle missing Ratings (5 points)
        original_df = pd.read_csv(FPATH)
        if original_df['Rating'].isnull().any() and not analyzer.df['Rating'].isnull().any():
            init_score += 5
            print("  - [PASS] Missing 'Rating' values handled. (+5 pts)")
        else:
            print("  - [FAIL] Missing 'Rating' values not handled or no missing values to handle.")
        
        total_score += init_score
        print(f"__init__ Score: {init_score}/25")

    except Exception as e:
        print(f"  - [FAIL] Error during __init__: {e}")
        print("__init__ Score: 0/25")
        analyzer = None # Cannot proceed

    if analyzer:
        # Test get_top_genres method (25 points)
        print("\n[Testing get_top_genres]")
        try:
            top_3_genres = analyzer.get_top_genres(top_n=3)
            # Expected: Comedy (4), Sci-Fi (3), Action (3) or Thriller (3)
            expected_genres = ['Comedy', 'Sci-Fi', 'Action', 'Thriller']
            if (isinstance(top_3_genres, list) and len(top_3_genres) == 3 and
                top_3_genres[0][0] == 'Comedy' and top_3_genres[0][1] == 4 and
                top_3_genres[1][0] in expected_genres and top_3_genres[1][1] == 3 and
                top_3_genres[2][0] in expected_genres and top_3_genres[2][1] == 3):
                total_score += 25
                print("  - [PASS] Correctly returned top 3 genres. (+25 pts)")
            else:
                print(f"  - [FAIL] Unexpected output for top 3 genres: {top_3_genres}")
        except Exception as e:
            print(f"  - [FAIL] Error during get_top_genres: {e}")
        print("get_top_genres Score: .../25")

        # Test calculate_average_by_year method (25 points)
        print("\n[Testing calculate_average_by_year]")
        try:
            avg_ratings = analyzer.calculate_average_by_year(start_year=2020, end_year=2021)
            # Note: These expected values depend on the median imputation
            # Median of non-null ratings is 8.05.
            # 2020: (8.5+8.8+8.05+8.9+8.6+7.3)/6 = 8.3583...
            # 2021: (7.9+7.5+6.5+8.1+6.4)/5 = 7.28
            if (isinstance(avg_ratings, dict) and 
                2020 in avg_ratings and 2021 in avg_ratings and
                abs(avg_ratings[2020] - 8.3583) < 0.01 and
                abs(avg_ratings[2021] - 7.28) < 0.01):
                total_score += 25
                print("  - [PASS] Correctly calculated average ratings for 2020-2021. (+25 pts)")
            else:
                print(f"  - [FAIL] Incorrect average ratings calculation: {avg_ratings}")
        except Exception as e:
            print(f"  - [FAIL] Error during calculate_average_by_year: {e}")
        print("calculate_average_by_year Score: .../25")

        # Test visualize_yearly_rating_trend method (25 points)
        print("\n[Testing visualize_yearly_rating_trend]")
        try:
            analyzer.visualize_yearly_rating_trend()
            if os.path.exists("rating_trend.png"):
                total_score += 25
                print("  - [PASS] 'rating_trend.png' created successfully. (+25 pts)")
                os.remove("rating_trend.png") # Clean up
            else:
                print("  - [FAIL] 'rating_trend.png' was not created.")
        except Exception as e:
            print(f"  - [FAIL] Error during visualize_yearly_rating_trend: {e}")
        print("visualize_yearly_rating_trend Score: .../25")

    print("\n--- Test Finished ---")
    print(f"Final Score: {total_score}/{max_score}")
