import threading
import tkinter as tk

from index import main as notification_main
from ui import NotificationDashboard


def run_reader():
    """Run the existing notification engine without blocking the UI."""
    import asyncio
    asyncio.run(notification_main())


if __name__ == "__main__":
    app = NotificationDashboard()
    threading.Thread(target=run_reader, daemon=True).start()
    app.mainloop()
