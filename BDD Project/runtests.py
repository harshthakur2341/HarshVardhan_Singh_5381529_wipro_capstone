import subprocess
import shutil
import os
import sys


def run_tests():
    print("--- Cleaning old reports ---")
    for folder in ["allure-results", "allure-report"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Deleted {folder}")

    print("--- Starting Test Execution ---")
    # This runs the specific tag we defined in the feature file
    behave_cmd = [
        "behave",
        "--tags=@e2e_train",
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", "allure-results"
    ]

    result = subprocess.run(behave_cmd)

    print("--- Generating Allure Report ---")
    try:
        subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"])
        print("\nSUCCESS: Report generated. Run 'allure serve allure-results' to view it.")
    except Exception as e:
        print(f"Failed to generate report: {e}")
        print("Ensure Allure Commandline is installed.")

    sys.exit(result.returncode)


if __name__ == "__main__":
    run_tests()