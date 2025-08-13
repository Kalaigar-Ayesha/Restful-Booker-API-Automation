"""
Simple test runner script for API automation tests.
"""

import subprocess
import sys
import argparse

def run_tests(verbose=False, html_report=False, allure=False):
    """Run the test suite with specified options."""
    cmd = ["python", "-m", "pytest", "tests/"]
    
    if verbose:
        cmd.append("-v")
    
    if html_report:
        cmd.extend(["--html=reports/report.html", "--self-contained-html"])
    
    if allure:
        cmd.extend(["--alluredir=reports/allure-results"])
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n All tests passed! Exit code: {result.returncode}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n Tests failed! Exit code: {e.returncode}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run API automation tests")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--allure", action="store_true", help="Generate Allure report")
    
    args = parser.parse_args()
    
    print("Starting API automation tests...")
    success = run_tests(
        verbose=args.verbose,
        html_report=args.html,
        allure=args.allure
    )
    
    if success:
        print("\n Test execution completed successfully!")
        if args.html:
            print(" HTML report generated: reports/report.html")
        if args.allure:
            print(" Allure results generated: reports/allure-results/")
    else:
        print("\n Test execution failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
