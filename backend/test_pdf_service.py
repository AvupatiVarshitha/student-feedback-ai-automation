from backend.services.sheets_service import get_feedback_data
from backend.services.report_builder import ReportBuilder
from backend.services.pdf_service import PDFService


def main():

    feedback = get_feedback_data()

    builder = ReportBuilder(feedback)

    report = builder.build_report()

    pdf = PDFService()

    pdf.build_pdf(

        report,

        "backend/reports/weekly_report.pdf"

    )


if __name__ == "__main__":
    main()