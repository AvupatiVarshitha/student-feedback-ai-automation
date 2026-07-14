from backend.services.sheets_service import get_feedback_data
from backend.services.report_builder import ReportBuilder

feedback = get_feedback_data()

builder = ReportBuilder(feedback)

report = builder.build_report()

print(report.keys())

print()

for batch in report["batches"]:
    print(batch["name"])
    print(batch["statistics"]["total_responses"])