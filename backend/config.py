from dotenv import load_dotenv
import os

# ---------------------------------
# Load Environment Variables
# ---------------------------------

load_dotenv()

# ---------------------------------
# Google Credentials
# ---------------------------------

GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

# ---------------------------------
# Telegram Bot
# ---------------------------------

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ---------------------------------
# Email
# ---------------------------------

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
REPORT_EMAIL = os.getenv("REPORT_EMAIL")

# ---------------------------------
# Batch Configuration
# ---------------------------------

BATCHES = [

    {
        "name": "Batch 1",
        "sheet_name": os.getenv("BATCH1_SHEET_NAME"),
        "form_link": os.getenv("BATCH1_FORM_LINK"),
        "chat_id": os.getenv("BATCH1_CHAT_ID")
    },

    {
        "name": "Batch 2",
        "sheet_name": os.getenv("BATCH2_SHEET_NAME"),
        "form_link": os.getenv("BATCH2_FORM_LINK"),
        "chat_id": os.getenv("BATCH2_CHAT_ID")
    },

    {
        "name": "Batch 3",
        "sheet_name": os.getenv("BATCH3_SHEET_NAME"),
        "form_link": os.getenv("BATCH3_FORM_LINK"),
        "chat_id": os.getenv("BATCH3_CHAT_ID")
    }

]