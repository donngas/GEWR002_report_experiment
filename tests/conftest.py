import pytest
import importlib

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