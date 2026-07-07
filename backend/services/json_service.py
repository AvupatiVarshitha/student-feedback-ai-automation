import json
import os


def save_report(report):

    os.makedirs("backend/reports", exist_ok=True)

    with open(
        "backend/reports/weekly_report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(report, file, indent=4)

    print("\n✅ JSON Report Saved Successfully!")