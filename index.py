import asyncio

import pyttsx3
from winrt.windows.ui.notifications.management import (
    UserNotificationListener,
    UserNotificationListenerAccessStatus,
)

from config import (
    APP_PRIORITIES,
    IGNORE_KEYWORDS,
    IMPORTANT_KEYWORDS,
    IMPORTANCE_THRESHOLD,
    POLL_SECONDS,
    STRONG_KEYWORDS,
)


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
    """Calculate a transparent, explainable priority score."""
    app = normalized_name(app_name)
    content = " ".join(texts).lower()
    combined = f"{app} {content}"

    score = APP_PRIORITIES.get(app, 0)

    # Strong signals are deliberately powerful because they often indicate
    # security, financial, or call-related events.
    strong_matches = [k for k in STRONG_KEYWORDS if k in combined]
    score += 6 if strong_matches else 0

    useful_matches = [k for k in IMPORTANT_KEYWORDS if k in combined]
    score += min(len(useful_matches), 3) * 2

    noise_matches = [k for k in IGNORE_KEYWORDS if k in combined]
    score -= min(len(noise_matches), 2) * 4

    return max(score, 0)


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
    print(f"🎯 Importance threshold: {IMPORTANCE_THRESHOLD}")

    engine = pyttsx3.init()
    engine.setProperty("rate", 175)

    # Seed existing notifications so startup does not replay old alerts.
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
                important = score >= IMPORTANCE_THRESHOLD

                print("\n" + "=" * 60)
                print("🔔 NEW NOTIFICATION")
                print("APP:", app_name)
                print("TEXT:", " | ".join(texts))
                print("SCORE:", score)

                if important:
                    print("🚨 IMPORTANT")
                    speak(engine, app_name, texts)
                else:
                    print("ℹ️ Not important — silent")

                print("=" * 60)

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
