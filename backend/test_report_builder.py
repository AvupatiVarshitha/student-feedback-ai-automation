import json

from backend.services.sheets_service import get_feedback_data
from backend.services.report_builder import ReportBuilder


def main():

    print("Loading Feedback...")

    feedback = get_feedback_data()

    builder = ReportBuilder(feedback)

    report = builder.build_report()

    print("=" * 60)
    print("STUDENT TRIBE WEEKLY REPORT")
    print("=" * 60)

    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()