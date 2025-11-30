import sys
import importlib
import pytest

def main():
    """
    Parses command-line arguments and runs pytest.
    This script acts as a convenient entry point for running tests against a specific module.
    """
    # Determine module name from command-line arguments or user input.
    if len(sys.argv) > 1:
        module_name = sys.argv[1]
    else:
        module_name = input("Enter the module name to test (e.g., mock_solve): ")

    # Dynamically import the module to make it available for pytest's collection.
    # A conftest.py file will pick up this module.
    try:
        importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Error: Module '{module_name}' not found. Please check the name and try again.")
        sys.exit(1)

    # Run pytest with the specified module. The --module-name is a custom option.
    # The -v flag is for verbose output.
    # The --describe-skip='Test' flag is for a plugin that prints the describe blocks as headers.
    pytest_args = ["-v", f"--module-name={module_name}", "tests/"]
    sys.exit(pytest.main(pytest_args))

if __name__ == "__main__":
    main()
