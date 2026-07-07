from backend.services.email_service import EmailService

def main():

    email = EmailService()

    email.send_report(
        "backend/reports/weekly_report.pdf"
    )

if __name__ == "__main__":
    main()