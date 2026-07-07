from datetime import datetime
import time

from apscheduler.schedulers.background import BackgroundScheduler

from backend.config import GOOGLE_FORM_LINK
from backend.services.telegram_service import send_message

from backend.services.sheets_service import get_feedback_data
from backend.services.data_processor import DataProcessor
from backend.services.report_builder import ReportBuilder
from backend.services.charts_service import ChartService
from backend.services.pdf_service import PDFService
from backend.services.email_service import EmailService

# -------------------------------------------------------
# JOB 1 : SEND GOOGLE FORM
# -------------------------------------------------------

def send_feedback_form():

    message = f"""
📢 <b>Student Tribe Weekly Feedback</b>

Hello Everyone 👋

Please fill this week's feedback form.

🔗 {GOOGLE_FORM_LINK}

Thank you 😊
"""

    send_message(message)

    print("\n✅ Google Form Link Sent Successfully!")


# -------------------------------------------------------
# JOB 2 : GENERATE REPORT
# -------------------------------------------------------

def generate_report():

    try:

        print("\nGenerating Weekly Report...")

        # Read Google Sheet
        feedback = get_feedback_data()

        # Build Report
        builder = ReportBuilder(feedback)

        report = builder.build_report()

        # Generate Charts
        charts = ChartService()

        charts.generate_all_charts(
            report["statistics"]
        )

        # Generate PDF
        pdf = PDFService()

        pdf.build_pdf(
            report,
            "backend/reports/weekly_report.pdf"
        )

        # Send Email
        email = EmailService()

        email.send_report(
            "backend/reports/weekly_report.pdf"
        )

        print("\n✅ Weekly Report Generated Successfully!")
        print("✅ PDF Sent To Email Successfully!")

    except Exception as e:

        print(f"\n❌ Report Generation Failed : {e}")

# -------------------------------------------------------
# MAIN
# -------------------------------------------------------

def main():

    print("=" * 60)
    print("      STUDENT TRIBE AUTOMATION SCHEDULER")
    print("=" * 60)

    # -----------------------------
    # FORM SCHEDULE
    # -----------------------------

    form_date = input("\nEnter Form Send Date (DD-MM-YYYY): ")

    form_time = input("Enter Form Send Time (HH:MM): ")

    # -----------------------------
    # REPORT SCHEDULE
    # -----------------------------

    report_date = input("\nEnter Report Generation Date (DD-MM-YYYY): ")

    report_time = input("Enter Report Generation Time (HH:MM): ")

    # -----------------------------

    form_datetime = datetime.strptime(
        f"{form_date} {form_time}",
        "%d-%m-%Y %H:%M"
    )

    report_datetime = datetime.strptime(
        f"{report_date} {report_time}",
        "%d-%m-%Y %H:%M"
    )

    scheduler = BackgroundScheduler()

    # Job 1
    scheduler.add_job(
        send_feedback_form,
        trigger="date",
        run_date=form_datetime
    )

    # Job 2
    scheduler.add_job(
        generate_report,
        trigger="date",
        run_date=report_datetime
    )

    scheduler.start()

    print("\n" + "=" * 60)
    print("✅ Scheduler Started Successfully")
    print("=" * 60)

    print(f"\n📢 Form will be sent on     : {form_datetime}")

    print(f"📄 Report will be generated : {report_datetime}")

    print("\nWaiting for scheduled jobs...\n")

    try:

        while True:

            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):

        scheduler.shutdown()

        print("\nScheduler Stopped.")


if __name__ == "__main__":

    main()