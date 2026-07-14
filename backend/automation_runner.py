from backend.services.telegram_service import send_message
from backend.services.email_service import EmailService
from backend.services.sheets_service import get_feedback_data
from backend.services.report_builder import ReportBuilder
from backend.services.charts_service import ChartService
from backend.services.pdf_service import PDFService
from backend.config import BATCHES


class AutomationRunner:

    def send_forms(self):
        print("\n========== Sending Google Forms ==========\n")
        for batch in BATCHES:
            message = f"""
📢 <b>Weekly Feedback Form</b>

Batch : {batch["name"]}

Please submit your weekly feedback.

📝 {batch["form_link"]}

Thank you!
"""

            response = send_message(
                batch["chat_id"],
                message
            )

            print(
                batch["name"],
                response
            )
    def analyze_feedback(self):
        print("\n========== Reading Google Sheets ==========\n")

        feedback = get_feedback_data()

        builder = ReportBuilder(
            feedback
        )

        report = builder.build_report()

        self.report = report

        print("✅ Analysis Completed")

    def generate_pdf(self):
        print("\n========== Generating PDF ==========\n")

        charts = ChartService()
        for batch in self.report["batches"]:
            charts.generate_all_charts(
                batch["statistics"],
                batch["name"]
            )

        pdf = PDFService()

        pdf.build_pdf(
            self.report,

            "backend/reports/weekly_report.pdf"

        )

        print("✅ PDF Generated")

    def send_email(self):
        print("\n========== Sending Email ==========\n")
        email = EmailService()
        email.send_report(
            "backend/reports/weekly_report.pdf"

        )

    def run(self):
        self.analyze_feedback()
        self.generate_pdf()
        self.send_email()
        print("\n🎉 Automation Completed Successfully!")

    def run_report_pipeline(self):
        self.analyze_feedback()

        self.generate_pdf()

        self.send_email()

        print("\n🎉 Report Pipeline Completed!")

if __name__ == "__main__":

    runner = AutomationRunner()

    runner.run()