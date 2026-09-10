import asyncio

import pyttsx3
from winrt.windows.ui.notifications.management import (
    UserNotificationListener,
    UserNotificationListenerAccessStatus,
)

POLL_SECONDS = 2
IMPORTANCE_THRESHOLD = 3

# Apps that commonly carry personal communication notifications.
COMMUNICATION_APPS = {
    "whatsapp",
    "telegram",
    "messenger",
    "messages",
    "google messages",
    "phone",
    "phone link",
    "link to windows",
    "your phone",
}

# Phone Link can expose Android notifications through Windows.
PHONE_LINK_APPS = {
    "phone link",
    "link to windows",
    "your phone",
}

IMPORTANT_KEYWORDS = {
    "urgent", "important", "emergency", "alert", "warning", "critical",
    "otp", "verification code", "security code", "login", "sign in",
    "password", "security", "fraud", "suspicious", "blocked",
    "payment", "transaction", "debited", "credited", "bank", "upi",
    "due", "deadline", "appointment", "interview", "meeting", "exam",
    "assignment", "job", "offer", "delivery", "call", "missed call",
    "call me", "reminder", "schedule", "flight", "ticket", "booking",
    "तुरंत", "जरूरी", "महत्वपूर्ण", "ओटीपी", "पेमेंट", "लेनदेन",
}

STRONG_KEYWORDS = {
    "otp", "verification code", "security code", "fraud", "suspicious",
    "emergency", "critical", "urgent", "payment", "transaction",
    "debited", "credited", "bank", "upi", "missed call", "incoming call",
}

IGNORE_KEYWORDS = {
    "download complete",
    "update available",
    "suggested for you",
    "people you may know",
    "new follower",
    "new friend suggestion",
    "promotion",
    "promoted",
    "sale",
    "discount",
    "advertisement",
}


def extract_text(notification):
    """Return notification text as a list of non-empty strings."""
    toast = notification.notification
    binding = toast.visual.get_binding("ToastGeneric")

    if not binding:
        return []

    return [
        text.text.strip()
        for text in binding.get_text_elements()
        if text.text and text.text.strip()
    ]


def normalized_name(name):
    return " ".join(name.lower().split())


def importance_score(app_name, texts):
    """Return a transparent importance score; no external AI/API required."""
    app = normalized_name(app_name)
    content = " ".join(texts).lower()
    combined = f"{app} {content}"
    score = 0

    if any(keyword in combined for keyword in IGNORE_KEYWORDS):
        score -= 5

    if any(keyword in combined for keyword in STRONG_KEYWORDS):
        score += 5

    score += sum(2 for keyword in IMPORTANT_KEYWORDS if keyword in combined)

    if app in COMMUNICATION_APPS:
        score += 1

    # Phone Link itself is not automatically important. The mirrored
    # notification content still has to contain a meaningful signal.
    if app in PHONE_LINK_APPS:
        score += 1

    return score


def is_important(app_name, texts):
    return importance_score(app_name, texts) >= IMPORTANCE_THRESHOLD


def speak(engine, app_name, texts):
    message = " ".join(texts)
    speech = f"Important notification from {app_name}. {message}"
    print(f"🔊 SPEAKING: {speech}")
    engine.say(speech)
    engine.runAndWait()


async def read_notifications(listener):
    """Fetch the current Windows toast notifications."""
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

    # Existing notifications are seeded into the seen set so they are never
    # spoken immediately after startup.
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

                score = importance_score(app_name, texts)

                print("\n" + "=" * 60)
                print("🔔 NEW NOTIFICATION")
                print("APP:", app_name)
                print("TEXT:", " | ".join(texts))
                print("SCORE:", score)

                if score >= IMPORTANCE_THRESHOLD:
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
