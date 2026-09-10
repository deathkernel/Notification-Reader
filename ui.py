import tkinter as tk
from tkinter import ttk


BG = "#0f172a"
CARD = "#111c33"
CARD_2 = "#17233d"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"
ACCENT = "#38bdf8"
SUCCESS = "#22c55e"
DANGER = "#ef4444"


class NotificationDashboard(tk.Tk):
    """Modern lightweight dashboard for the notification reader."""

    def __init__(self):
        super().__init__()
        self.title("Notification Reader")
        self.geometry("980x680")
        self.minsize(850, 580)
        self.configure(bg=BG)

        self.received = tk.IntVar(value=0)
        self.important = tk.IntVar(value=0)
        self.spoken = tk.IntVar(value=0)
        self.voice_enabled = tk.BooleanVar(value=True)
        self.phone_link_enabled = tk.BooleanVar(value=True)
        self.threshold = tk.IntVar(value=5)

        self._build_style()
        self._build_header()
        self._build_stats()
        self._build_notifications()
        self._build_footer()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor=CARD_2,
            background=ACCENT,
            bordercolor=CARD_2,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
        )

    def _label(self, parent, text, size=11, color=TEXT, weight="normal"):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=("Segoe UI", size, weight),
        )

    def _build_header(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=28, pady=(24, 16))

        title_box = tk.Frame(header, bg=BG)
        title_box.pack(side="left")
        self._label(title_box, "🔔  Notification Reader", 22, TEXT, "bold").pack(anchor="w")
        self._label(title_box, "Smart Windows + Phone Link notification control", 10, MUTED).pack(anchor="w", pady=(4, 0))

        status = tk.Frame(header, bg=CARD, padx=14, pady=9)
        status.pack(side="right")
        tk.Label(status, text="●", bg=CARD, fg=SUCCESS, font=("Segoe UI", 12)).pack(side="left")
        tk.Label(status, text=" ACTIVE", bg=CARD, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(side="left")

    def _build_stats(self):
        stats = tk.Frame(self, bg=BG)
        stats.pack(fill="x", padx=28, pady=4)

        self._stat_card(stats, "Received", self.received, "today").pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._stat_card(stats, "Important", self.important, "spoken candidates").pack(side="left", fill="x", expand=True, padx=8)
        self._stat_card(stats, "Spoken", self.spoken, "voice alerts").pack(side="left", fill="x", expand=True, padx=(8, 0))

    def _stat_card(self, parent, title, variable, subtitle):
        card = tk.Frame(parent, bg=CARD, padx=18, pady=15)
        tk.Label(card, text=title.upper(), bg=CARD, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(card, textvariable=variable, bg=CARD, fg=TEXT, font=("Segoe UI", 25, "bold")).pack(anchor="w", pady=(3, 0))
        tk.Label(card, text=subtitle, bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w")
        return card

    def _build_notifications(self):
        section = tk.Frame(self, bg=BG)
        section.pack(fill="both", expand=True, padx=28, pady=(20, 10))

        top = tk.Frame(section, bg=BG)
        top.pack(fill="x", pady=(0, 9))
        self._label(top, "RECENT NOTIFICATIONS", 10, MUTED, "bold").pack(side="left")
        self._label(top, "Live feed", 9, SUCCESS).pack(side="right")

        outer = tk.Frame(section, bg=CARD, bd=0)
        outer.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(
            outer,
            bg=CARD,
            fg=TEXT,
            selectbackground=CARD_2,
            selectforeground=TEXT,
            highlightthickness=0,
            bd=0,
            activestyle="none",
            font=("Segoe UI", 10),
        )
        self.listbox.pack(fill="both", expand=True, padx=12, pady=12)

        self.add_notification("WhatsApp", "No new important notifications yet", 0, False)

    def add_notification(self, app, message, score, spoken=False):
        icon = "🔊" if spoken else ("🚨" if score >= self.threshold.get() else "○")
        line = f"{icon}  {app:<18} {message[:58]:<58}  {score}/10"
        self.listbox.insert(0, line)
        self.received.set(self.received.get() + 1)
        if score >= self.threshold.get():
            self.important.set(self.important.get() + 1)
        if spoken:
            self.spoken.set(self.spoken.get() + 1)

    def _build_footer(self):
        footer = tk.Frame(self, bg=CARD, padx=20, pady=12)
        footer.pack(fill="x", side="bottom")

        tk.Checkbutton(
            footer, text="🔊 Voice", variable=self.voice_enabled,
            bg=CARD, fg=TEXT, selectcolor=CARD_2,
            activebackground=CARD, activeforeground=TEXT,
            font=("Segoe UI", 9), bd=0,
        ).pack(side="left", padx=(0, 14))

        tk.Checkbutton(
            footer, text="📱 Phone Link", variable=self.phone_link_enabled,
            bg=CARD, fg=TEXT, selectcolor=CARD_2,
            activebackground=CARD, activeforeground=TEXT,
            font=("Segoe UI", 9), bd=0,
        ).pack(side="left")

        tk.Label(footer, text="Importance threshold", bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(side="left", padx=(35, 8))
        scale = tk.Scale(
            footer, from_=1, to=10, orient="horizontal", variable=self.threshold,
            bg=CARD, fg=TEXT, troughcolor=CARD_2, highlightthickness=0,
            activebackground=ACCENT, bd=0, length=150,
        )
        scale.pack(side="left")

        tk.Button(
            footer, text="⚙ Settings", command=self.show_settings,
            bg=CARD_2, fg=TEXT, activebackground="#223252", activeforeground=TEXT,
            relief="flat", bd=0, padx=12, pady=7, font=("Segoe UI", 9, "bold"),
        ).pack(side="right")

    def show_settings(self):
        dialog = tk.Toplevel(self)
        dialog.title("Settings")
        dialog.geometry("360x230")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        tk.Label(dialog, text="Settings", bg=BG, fg=TEXT, font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=22, pady=(20, 12))
        tk.Label(dialog, text="Speech and Phone Link controls are available from the dashboard.", wraplength=310, justify="left", bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", padx=22)
        tk.Button(dialog, text="Close", command=dialog.destroy, bg=CARD_2, fg=TEXT, relief="flat", bd=0, padx=18, pady=8).pack(anchor="e", padx=22, pady=25)


if __name__ == "__main__":
    app = NotificationDashboard()
    app.mainloop()
