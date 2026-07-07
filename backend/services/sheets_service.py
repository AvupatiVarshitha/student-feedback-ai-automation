import gspread
from google.oauth2.service_account import Credentials

from backend.config import GOOGLE_CREDENTIALS, GOOGLE_SHEET_NAME

# Google API permissions
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]


def get_feedback_data():
    """
    Reads all responses from the Google Sheet
    and returns them as a list of dictionaries.
    """

    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS,
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open(GOOGLE_SHEET_NAME)
    print("Reading Sheet:", spreadsheet.title)
    print("Sheet URL:", spreadsheet.url)

    worksheet = spreadsheet.sheet1

    records = worksheet.get_all_records()

    return records