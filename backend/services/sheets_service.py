import gspread
from google.oauth2.service_account import Credentials
import os
import json
from backend.config import (
    GOOGLE_CREDENTIALS,
    BATCHES
)

# -----------------------------------------
# Google API Permissions
# -----------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]


def get_feedback_data():
    """
    Reads feedback from all batch sheets.

    Returns:

    {
        "Batch 1": [...],
        "Batch 2": [...],
        "Batch 3": [...]
    }
    """

    credentials_info = json.loads(
        os.getenv("GOOGLE_CREDENTIALS_JSON")
    )

    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    all_feedback = {}

    for batch in BATCHES:

        spreadsheet = client.open(
            batch["sheet_name"]
        )

        print(f"\nReading {batch['name']}")
        print("Sheet :", spreadsheet.title)
        print("URL   :", spreadsheet.url)

        worksheet = spreadsheet.sheet1

        records = worksheet.get_all_records()

        all_feedback[batch["name"]] = records

    return all_feedback