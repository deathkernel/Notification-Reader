import asyncio
import threading

from index import main as notification_main
from ui import NotificationDashboard


def run_reader(app):
    """Run the notification engine without blocking Tkinter."""
    asyncio.run(
        notification_main(
            on_notification=app.on_notification,
            get_settings=app.settings,
        )
    )


if __name__ == "__main__":
    app = NotificationDashboard()
    reader_thread = threading.Thread(target=run_reader, args=(app,), daemon=True)
    reader_thread.start()
    app.mainloop()
