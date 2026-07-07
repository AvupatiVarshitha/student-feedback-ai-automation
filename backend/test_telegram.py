from backend.services.telegram_service import send_message

from backend.config import GOOGLE_FORM_LINK


message = f"""
📢 <b>Student Tribe Weekly Feedback</b>

Hello Everyone 👋

Please fill this week's feedback form.

🔗 {GOOGLE_FORM_LINK}

Thank you 😊
"""

response = send_message(message)

print(response)