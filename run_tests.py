import os
import sys
import pandas as pd
import importlib
from typing import cast, Protocol, Optional
from loguru import logger

FPATH = "movies.csv"

# Defines the expected structure of the MovieAnalyzer class for type checking.
class MovieAnalyzerProtocol(Protocol):
    def __init__(self, filepath): ...
    def get_top_genres(self, top_n): ...
    def calculate_average_by_year(self, start_year, end_year):...
    def visualize_yearly_rating_trend(self): ...

# Defines the expected structure of the dynamically imported module.
class SolveModuleProtocol(Protocol):
    MovieAnalyzer: type[MovieAnalyzerProtocol]

# Dynamically imports a module by its string name.
def import_by_arg(module: str) -> Optional[SolveModuleProtocol]:
    try:
        # Attempt to import the module.
        solve_module = importlib.import_module(module)
        return cast(SolveModuleProtocol, solve_module)
    except ModuleNotFoundError:
        logger.error(f"Module {module} not found.")
    except Exception as e:
        logger.error(f"Error while importing: {e}")
    return None # Return None on failure.

if __name__ == "__main__":
    if len(sys.argv) > 1:
        module_name = sys.argv[1]
    else:
        module_name = input("Enter the module name to test (e.g., mock_solve): ")

    # Import the specified module.
    solve_module = import_by_arg(module_name)

    if not solve_module:
        logger.error("Could not import the specified module. Exiting.")
        sys.exit(1)

    # Get the MovieAnalyzer class from the imported module.
    MovieAnalyzer = solve_module.MovieAnalyzer

    total_score = 0
    max_score = 100
    
    logger.info("--- Starting MovieAnalyzer Test ---")

    # Test __init__ method (25 points)
    logger.info("\n[Testing __init__]")
    try:
        analyzer = MovieAnalyzer(filepath=FPATH)
        init_score = 0
        
        # Check if data is loaded into a DataFrame.
        if isinstance(analyzer.df, pd.DataFrame) and not analyzer.df.empty:
            init_score += 10
            logger.success("  - [PASS] Data loaded into pandas DataFrame. (+10 pts)")
        else:
            logger.error("  - [FAIL] Data not loaded correctly.")

        # Check if 'Release_Date' column is converted to datetime.
        if pd.api.types.is_datetime64_any_dtype(analyzer.df['Release_Date']):
            init_score += 10
            logger.success("  - [PASS] 'Release_Date' column converted to datetime. (+10 pts)")
        else:
            logger.error("  - [FAIL] 'Release_Date' column is not datetime type.")

        # Check if missing 'Rating' values are handled.
        original_df = pd.read_csv(FPATH)
        if original_df['Rating'].isnull().any() and not analyzer.df['Rating'].isnull().any():
            init_score += 5
            logger.success("  - [PASS] Missing 'Rating' values handled. (+5 pts)")
        else:
            logger.warning("  - [WARN] Missing 'Rating' values not handled or no missing values to handle.")
        
        total_score += init_score
        logger.info(f"__init__ Score: {init_score}/25")

    except Exception as e:
        logger.error(f"  - [FAIL] Error during __init__: {e}")
        logger.info("__init__ Score: 0/25")
        analyzer = None # Cannot proceed if initialization fails.

    if analyzer:
        # Test get_top_genres method (25 points)
        get_top_genres_score = 0
        logger.info("\n[Testing get_top_genres]")
        try:
            top_3_genres = analyzer.get_top_genres(top_n=3)
            # Expected from movies.csv: Comedy (4), Action (4), Sci-Fi (3), Thriller (3)
            # The top 2 have a count of 4, the next 2 have a count of 3.
            # The test should check if the top 3 genres returned match this distribution.
            if (isinstance(top_3_genres, list) and len(top_3_genres) == 3):
                # Check counts
                counts_correct = (top_3_genres[0][1] == 4 and 
                                  top_3_genres[1][1] == 4 and 
                                  top_3_genres[2][1] == 3)
                # Check genres
                genres = {item[0] for item in top_3_genres}
                genres_correct = genres.issubset({'Comedy', 'Action', 'Sci-Fi', 'Thriller'})
                if counts_correct and genres_correct:
                    get_top_genres_score = 25
                    logger.success("  - [PASS] Correctly returned top 3 genres. (+25 pts)")
                else:
                    logger.error(f"  - [FAIL] Unexpected output for top 3 genres: {top_3_genres}")
            else: # Handle cases where the return type or length is incorrect
                logger.error(f"  - [FAIL] Output is not a list of 3 items: {top_3_genres}")
        except Exception as e:
            logger.error(f"  - [FAIL] Error during get_top_genres: {e}")
        total_score += get_top_genres_score
        logger.info(f"get_top_genres Score: {get_top_genres_score}/25")

        # Test calculate_average_by_year method (25 points)
        calc_avg_score = 0
        logger.info("\n[Testing calculate_average_by_year]")
        try:
            avg_ratings = analyzer.calculate_average_by_year(start_year=2020, end_year=2021)
            # Note: These expected values depend on the median imputation
            # Median of non-null ratings is 8.0.
            # 2020: (8.5+8.8+8.0+8.9+8.6+7.3)/6 = 8.35
            # 2021: (7.9+7.5+6.5+8.1+6.4)/5 = 7.28
            if (isinstance(avg_ratings, dict) and 
                2020 in avg_ratings and 2021 in avg_ratings and
                abs(avg_ratings[2020] - 8.35) < 0.01 and
                abs(avg_ratings[2021] - 7.28) < 0.01):
                calc_avg_score = 25
                logger.success("  - [PASS] Correctly calculated average ratings for 2020-2021. (+25 pts)")
            else:
                logger.error(f"  - [FAIL] Incorrect average ratings calculation: {avg_ratings}")
        except Exception as e:
            logger.error(f"  - [FAIL] Error during calculate_average_by_year: {e}")
        total_score += calc_avg_score
        logger.info(f"calculate_average_by_year Score: {calc_avg_score}/25")

        # Test visualize_yearly_rating_trend method (25 points)
        visualize_score = 0
        logger.info("\n[Testing visualize_yearly_rating_trend]")
        try:
            analyzer.visualize_yearly_rating_trend()
            if os.path.exists("rating_trend.png"):
                visualize_score = 25
                logger.success("  - [PASS] 'rating_trend.png' created successfully. (+25 pts)")
                os.remove("rating_trend.png") # Clean up
            else:
                logger.error("  - [FAIL] 'rating_trend.png' was not created.")
        except Exception as e:
            logger.error(f"  - [FAIL] Error during visualize_yearly_rating_trend: {e}")
        total_score += visualize_score
        logger.info(f"visualize_yearly_rating_trend Score: {visualize_score}/25")

    logger.info("\n--- Test Finished ---")
    logger.info(f"Final Score: {total_score}/{max_score}")
