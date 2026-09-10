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
    app = normalized_name(app_name)
    content = " ".join(texts).lower()
    combined = f"{app} {content}"
    score = APP_PRIORITIES.get(app, 0)
    if any(k in combined for k in STRONG_KEYWORDS):
        score += 6
    score += min(sum(k in combined for k in IMPORTANT_KEYWORDS), 3) * 2
    score -= min(sum(k in combined for k in IGNORE_KEYWORDS), 2) * 4
    return max(score, 0)


def is_important(app_name, texts, threshold=IMPORTANCE_THRESHOLD):
    return importance_score(app_name, texts) >= threshold


def speak(engine, app_name, texts):
    message = " ".join(texts)
    speech = f"Important notification from {app_name}. {message}"
    print(f"🔊 SPEAKING: {speech}")
    engine.say(speech)
    engine.runAndWait()


async def read_notifications(listener):
    return await listener.get_notifications_async(1)  # 1 = Toast


async def main(on_notification=None, get_settings=None):
    """Run the Windows notification pipeline.

    `on_notification` receives each new notification as a dictionary so a UI
    can display the same event without coupling the engine to Tkinter.
    `get_settings` may return live UI settings such as threshold and TTS state.
    """
    listener = UserNotificationListener.current
    access = await listener.request_access_async()
    print("Access status:", access)

    if access != UserNotificationListenerAccessStatus.ALLOWED:
        print("❌ Notification access denied.")
        return

    print("✅ Notification access granted!")
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    existing = await read_notifications(listener)
    seen_ids = {notification.id for notification in existing}
    print(f"🎧 Listening. Ignoring {len(seen_ids)} existing notification(s).")

    while True:
        try:
            notifications = await read_notifications(listener)
            settings = get_settings() if get_settings else {}
            threshold = settings.get("threshold", IMPORTANCE_THRESHOLD)
            voice_enabled = settings.get("voice_enabled", True)
            phone_link_enabled = settings.get("phone_link_enabled", True)

            for notification in notifications:
                if notification.id in seen_ids:
                    continue
                seen_ids.add(notification.id)

                app_name = notification.app_info.display_info.display_name
                texts = extract_text(notification)
                if not texts:
                    continue

                app_normalized = normalized_name(app_name)
                is_phone_link = app_normalized in {"phone link", "link to windows", "your phone"}
                score = importance_score(app_name, texts)
                important = score >= threshold
                if is_phone_link and not phone_link_enabled:
                    important = False

                event = {
                    "id": notification.id,
                    "app": app_name,
                    "texts": texts,
                    "message": " | ".join(texts),
                    "score": score,
                    "important": important,
                    "phone_link": is_phone_link,
                    "spoken": False,
                }

                print("\n" + "=" * 60)
                print("🔔 NEW NOTIFICATION")
                print("APP:", app_name)
                print("TEXT:", event["message"])
                print("SCORE:", score)

                if important:
                    print("🚨 IMPORTANT")
                    if voice_enabled:
                        speak(engine, app_name, texts)
                        event["spoken"] = True
                else:
                    print("ℹ️ Not important — silent")

                if on_notification:
                    on_notification(event)
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
