import json
import argparse
import sys

def analyze_kicad_drc_report(report_json):
    # Parse the JSON data
    report = json.loads(report_json)

    # Initialize lists to store error messages
    errors = []

    # Analyze unconnected items errors
    if report.get("unconnected_items"):
        for item in report["unconnected_items"]:
            description = item["description"]
            positions = [(i["pos"]["x"], i["pos"]["y"]) for i in item["items"]]
            error_message = f"Error: {description} at positions {positions}"
            errors.append(error_message)

    # Analyze violations errors
    if report.get("violations"):
        for violation in report["violations"]:
            description = violation["description"]
            positions = [(i["pos"]["x"], i["pos"]["y"]) for i in violation["items"]]
            error_message = f"Error: {description} at positions {positions}"
            errors.append(error_message)

    # Check if there were any errors found
    if errors:
        # If errors are found, print them and return an error code
        print("\n".join(errors))
        return 1  # Non-zero return code indicates failure in CI pipeline
    else:
        print("No errors found.")
        return 0  # Zero return code indicates success in CI pipeline

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Analyze KiCad DRC report for CI pipeline.")
    parser.add_argument("report_file", help="Path to the KiCad DRC report file in JSON format")

    # Parse the arguments
    args = parser.parse_args()

    # Read the report file
    try:
        with open(args.report_file, 'r') as file:
            report_json = file.read()
    except FileNotFoundError:
        print(f"Error: File '{args.report_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Analyze the report and exit with appropriate code
    exit_code = analyze_kicad_drc_report(report_json)
    sys.exit(exit_code)
