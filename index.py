import asyncio
import time

import pyttsx3
from winrt.windows.ui.notifications.management import (
    UserNotificationListener,
    UserNotificationListenerAccessStatus,
)

POLL_SECONDS = 2

# Notifications containing these terms are treated as important.
IMPORTANT_KEYWORDS = {
    "urgent", "important", "emergency", "alert", "warning", "critical",
    "otp", "verification code", "security code", "login", "sign in",
    "password", "security", "fraud", "suspicious", "blocked",
    "payment", "transaction", "debited", "credited", "bank", "upi",
    "due", "deadline", "appointment", "interview", "meeting", "exam",
    "assignment", "job", "offer", "delivery", "call", "missed call",
    "reminder", "schedule", "flight", "ticket", "booking",
    "तुरंत", "जरूरी", "महत्वपूर्ण", "ओटीपी", "पेमेंट", "लेनदेन",
}


def extract_text(notification):
    """Return notification text as a list of strings."""
    toast = notification.notification
    binding = toast.visual.get_binding("ToastGeneric")

    if not binding:
        return []

    return [
        text.text.strip()
        for text in binding.get_text_elements()
        if text.text and text.text.strip()
    ]


def is_important(app_name, texts):
    """Simple transparent importance classifier; no external AI/API required."""
    content = f"{app_name} {' '.join(texts)}".lower()

    # Strong signals get priority.
    strong_keywords = {
        "otp", "verification code", "security code", "fraud", "suspicious",
        "emergency", "critical", "urgent", "payment", "transaction",
        "debited", "credited", "bank", "upi", "missed call",
    }
    if any(keyword in content for keyword in strong_keywords):
        return True

    matches = sum(keyword in content for keyword in IMPORTANT_KEYWORDS)
    return matches >= 2


def speak(engine, app_name, texts):
    message = " ".join(texts)
    speech = f"Important notification from {app_name}. {message}"
    print(f"🔊 SPEAKING: {speech}")
    engine.say(speech)
    engine.runAndWait()


async def read_notifications(listener):
    """Fetch the current toast notifications."""
    return await listener.get_notifications_async(1)  # 1 = Toast


async def main():
    listener = UserNotificationListener.current

    access = await listener.request_access_async()
    print("Access status:", access)

    if access != UserNotificationListenerAccessStatus.ALLOWED:
        print("❌ Notification access denied.")
        return

    print("✅ Notification access granted!")
    print("🎧 Listening for important notifications...")
    print(f"⏱️ Poll interval: {POLL_SECONDS}s")

    engine = pyttsx3.init()
    engine.setProperty("rate", 175)

    # Seed with existing notifications so old notifications are never spoken.
    existing = await read_notifications(listener)
    seen_ids = {notification.id for notification in existing}
    print(f"Ignoring {len(seen_ids)} existing notification(s).")

    while True:
        try:
            notifications = await read_notifications(listener)

            for notification in notifications:
                if notification.id in seen_ids:
                    continue

                seen_ids.add(notification.id)

                app_name = notification.app_info.display_info.display_name
                texts = extract_text(notification)

                if not texts:
                    continue

                print("\n" + "=" * 60)
                print("🔔 NEW NOTIFICATION")
                print("APP:", app_name)
                print("TEXT:", " | ".join(texts))

                if is_important(app_name, texts):
                    print("🚨 IMPORTANT")
                    speak(engine, app_name, texts)
                else:
                    print("ℹ️ Not important — silent")

                print("=" * 60)

            # Keep memory bounded if Windows notification history grows large.
            if len(seen_ids) > 5000:
                seen_ids = {notification.id for notification in notifications}

            await asyncio.sleep(POLL_SECONDS)

        except KeyboardInterrupt:
            print("\n🛑 Reader stopped.")
            break
        except Exception as exc:
            print(f"⚠️ Reader error: {exc}")
            await asyncio.sleep(POLL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
