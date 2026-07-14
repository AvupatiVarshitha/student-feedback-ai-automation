from backend.config import BATCHES
from backend.services.telegram_service import send_message

for batch in BATCHES:

    print(f"\nSending to {batch['name']}")

    result = send_message(
        batch["chat_id"],
        f"✅ Testing {batch['name']}"
    )

    print(result)