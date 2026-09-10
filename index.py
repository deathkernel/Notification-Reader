import asyncio

from winrt.windows.ui.notifications.management import (
    UserNotificationListener,
    UserNotificationListenerAccessStatus,
)


async def main():
    listener = UserNotificationListener.current

    access = await listener.request_access_async()

    print("Access status:", access)

    if access != UserNotificationListenerAccessStatus.ALLOWED:
        print("❌ Notification access denied.")
        return

    print("✅ Notification access granted!\n")

    # 1 = Toast notifications
    notifications = await listener.get_notifications_async(1)

    print(f"Found {len(notifications)} notification(s)\n")

    for notification in notifications:
        print("=" * 60)
        print("ID:", notification.id)

        app_info = notification.app_info
        print("APP:", app_info.display_info.display_name)

        toast = notification.notification
        binding = toast.visual.get_binding("ToastGeneric")

        if binding:
            texts = binding.get_text_elements()
            for text in texts:
                print("TEXT:", text.text)

        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
