import pytest
import importlib
import re
import os

def pytest_addoption(parser):
    """Adds a custom command-line option to pytest."""
    parser.addoption("--module-name", action="store", default="mock_solve",
                     help="Specify the module to test (e.g., mock_solve, analyzer)")

@pytest.fixture(scope="session")
def module_to_test(request):
    """A session-scoped fixture that imports the module specified on the command line."""
    module_name = request.config.getoption("--module-name")
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pytest.fail(f"Module '{module_name}' not found.", pytrace=False)

def pytest_sessionstart(session):
    """Initialize a dictionary to store test results before tests run."""
    session.results = {}

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results."""
    outcome = yield
    result = outcome.get_result()
    
    if result.when == 'call':
        item.session.results[item] = result

def pytest_sessionfinish(session):
    """
    Calculate and print the total score at the end of the test session.
    Saves the score to a file.
    """
    total_score = 0
    max_score = 0
    results_summary = []

    for item, result in session.results.items():
        # Extract points from the test's describe marker or docstring
        points_str = None
        # Prioritize docstring for points, as it's more specific to the test function
        if item.obj and item.obj.__doc__:
            points_str = item.obj.__doc__
        else:
            describe_marker = item.get_closest_marker("describe")
            if describe_marker:
                points_str = describe_marker.args[0]
        
        points = 0
        if points_str:
            match = re.search(r'\((\d+)\s*p(?:oin)?ts\)', points_str, re.IGNORECASE)
            if match:
                points = int(match.group(1))
        max_score += points

        if result.passed:
            total_score += points

    module_name = session.config.getoption("--module-name")
    output_filename = os.path.join(session.config.rootdir, f"{module_name}_score.txt")

    report_content = f"Total Score for {module_name}: {total_score} / {max_score}" # For console display

    print(f"\n\n{'='*20} SCORE REPORT {'='*20}")
    print(report_content)
    print(f"{'='*54}\n")

    with open(output_filename, "w") as f:
        f.write(str(total_score))