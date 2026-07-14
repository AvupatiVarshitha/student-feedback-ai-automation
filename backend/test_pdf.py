from backend.services.sheets_service import get_feedback_data
from backend.services.report_builder import ReportBuilder
from backend.services.charts_service import ChartService
from backend.services.pdf_service import PDFService

feedback = get_feedback_data()

builder = ReportBuilder(feedback)

report = builder.build_report()

charts = ChartService()

for batch in report["batches"]:
    charts.generate_all_charts(
        batch["statistics"],
        batch["name"]
    )

pdf = PDFService()

pdf.build_pdf(
    report,
    "backend/reports/test_report.pdf"
)

print("\n✅ PDF Generated Successfully!")