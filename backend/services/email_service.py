import os
import smtplib
from email.message import EmailMessage

from backend.config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    REPORT_EMAIL
)


class EmailService:

    def send_report(self, pdf_path):

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"{pdf_path} not found."
            )

        message = EmailMessage()

        message["Subject"] = "Student Tribe Weekly Feedback Report"

        message["From"] = EMAIL_ADDRESS

        message["To"] = REPORT_EMAIL

        message.set_content(
            """
Hello,

Please find the attached Student Tribe Weekly Feedback Report.

Regards,
Student Tribe AI Automation System
"""
        )

        with open(pdf_path, "rb") as pdf:

            message.add_attachment(
                pdf.read(),
                maintype="application",
                subtype="pdf",
                filename="Weekly_Report.pdf"
            )

        try:

            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465
            ) as smtp:

                smtp.login(
                    EMAIL_ADDRESS,
                    EMAIL_PASSWORD
                )

                smtp.send_message(message)

            print("✅ Email Sent Successfully!")

        except Exception as e:

            print(f"❌ Email Failed : {e}")