import math
import time
import tkinter as tk
from tkinter import ttk

BG = "#05070a"
PANEL = "#0a0f15"
PANEL_2 = "#0e151d"
RED = "#ff2938"
RED_DIM = "#8f1722"
CYAN = "#43d9ff"
GREEN = "#39e58c"
WHITE = "#e8edf2"
MUTED = "#71808d"
BORDER = "#26313b"


class NotificationDashboard(tk.Tk):
    """ULTRON-inspired futuristic dashboard for the notification engine."""

    def __init__(self):
        super().__init__()
        self.title("ULTRON | Notification Intelligence")
        self.geometry("1280x820")
        self.minsize(1050, 700)
        self.configure(bg=BG)
        self.attributes("-alpha", 0.99)

        self.received = 0
        self.important = 0
        self.spoken = 0
        self.ignored = 0
        self.notifications = []
        self.voice_enabled = tk.BooleanVar(value=True)
        self.phone_link_enabled = tk.BooleanVar(value=True)
        self.threshold = tk.IntVar(value=5)
        self.status_text = tk.StringVar(value="SYSTEM ONLINE")
        self.core_phase = 0.0

        self._build()
        self._animate_core()

    def _build(self):
        self._topbar()
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=(8, 14))

        self._sidebar(body)
        center = tk.Frame(body, bg=BG)
        center.pack(side="left", fill="both", expand=True, padx=10)
        self._hero(center)
        self._feed(center)
        self._activity(center)
        self._right_panel(body)
        self._bottom_status()

    def _topbar(self):
        bar = tk.Frame(self, bg="#080b0f", height=42, highlightbackground=BORDER, highlightthickness=1)
        bar.pack(fill="x")
        tk.Label(bar, text="◉  ULTRON v1.0", bg="#080b0f", fg=RED, font=("Consolas", 11, "bold")).pack(side="left", padx=15)
        tk.Label(bar, text="NOTIFICATION INTELLIGENCE  //  A SMARTER TOMORROW", bg="#080b0f", fg=MUTED, font=("Consolas", 8)).pack(side="left")
        tk.Label(bar, text="HUMAN NOTIFICATIONS. MACHINE PRIORITIES.", bg="#080b0f", fg=MUTED, font=("Consolas", 8)).pack(side="right", padx=15)

    def _sidebar(self, parent):
        side = tk.Frame(parent, bg="#070a0e", width=190, highlightbackground=BORDER, highlightthickness=1)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        tk.Label(side, text="ULTRON", bg="#070a0e", fg=RED, font=("Segoe UI", 27, "bold")).pack(pady=(26, 0))
        tk.Label(side, text="NOTIFICATION AI", bg="#070a0e", fg=MUTED, font=("Consolas", 8)).pack(pady=(0, 28))
        for name in ["⌂  DASHBOARD", "◉  NOTIFICATIONS", "◷  HISTORY", "▥  ANALYTICS", "⚙  SETTINGS", "♩  VOICE", "▣  PHONE LINK", "◇  PRIVACY", "ⓘ  ABOUT"]:
            active = name.startswith("⌂")
            tk.Label(side, text=name, anchor="w", bg="#19090c" if active else "#070a0e", fg=RED if active else "#9aa7b2", font=("Consolas", 9, "bold" if active else "normal"), padx=18, pady=12).pack(fill="x", pady=1)
        tk.Label(side, text="\n\"INFORMATION IS THE\nFIRST STEP TOWARDS\nA BETTER WORLD.\"", bg="#070a0e", fg="#7f3440", justify="left", font=("Consolas", 8)).pack(side="bottom", anchor="w", padx=18, pady=25)

    def _hero(self, parent):
        hero = tk.Frame(parent, bg=PANEL, height=250, highlightbackground=RED_DIM, highlightthickness=1)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        self.core = tk.Canvas(hero, width=360, height=245, bg=PANEL, highlightthickness=0)
        self.core.pack(side="left", padx=15)
        self._draw_core()

        info = tk.Frame(hero, bg=PANEL)
        info.pack(side="left", fill="both", expand=True, pady=25)
        tk.Label(info, text="AI CORE", bg=PANEL, fg=WHITE, font=("Consolas", 14, "bold")).pack(anchor="w")
        tk.Label(info, textvariable=self.status_text, bg=PANEL, fg=RED, font=("Consolas", 20, "bold")).pack(anchor="w", pady=(2, 14))
        for item in ["LISTENING", "NOTIFICATION API", "PHONE LINK", "TTS ENGINE", "PRIORITY ENGINE"]:
            tk.Label(info, text="●  " + item, bg=PANEL, fg=GREEN, font=("Consolas", 9)).pack(anchor="w", pady=3)

        clock = tk.Frame(hero, bg=PANEL_2, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=12)
        clock.place(relx=0.72, rely=0.08, relwidth=0.25)
        self.clock_label = tk.Label(clock, bg=PANEL_2, fg=CYAN, font=("Consolas", 17, "bold"))
        self.clock_label.pack(anchor="w")
        tk.Label(clock, text="SYSTEM UPTIME  •  ONLINE", bg=PANEL_2, fg=MUTED, font=("Consolas", 7)).pack(anchor="w", pady=(4, 0))
        self._tick_clock()

    def _draw_core(self):
        self.core.delete("all")
        cx, cy = 180, 122
        phase = self.core_phase
        for i in range(7):
            r = 100 - i * 13 + math.sin(phase + i) * 3
            self.core.create_oval(cx-r, cy-r, cx+r, cy+r, outline=RED_DIM if i else RED, width=2 if i < 2 else 1)
        for angle in range(0, 360, 30):
            a = math.radians(angle + phase * 35)
            x1, y1 = cx + 45*math.cos(a), cy + 45*math.sin(a)
            x2, y2 = cx + 100*math.cos(a), cy + 100*math.sin(a)
            self.core.create_line(x1, y1, x2, y2, fill=RED_DIM, width=1)
        self.core.create_oval(cx-37, cy-37, cx+37, cy+37, fill="#1b080b", outline=RED, width=3)
        self.core.create_oval(cx-17, cy-17, cx+17, cy+17, fill=RED, outline=RED)
        self.core.create_text(cx, cy+57, text="AI CORE", fill=WHITE, font=("Consolas", 10, "bold"))

    def _animate_core(self):
        self.core_phase += 0.08
        self._draw_core()
        self.after(60, self._animate_core)

    def _feed(self, parent):
        head = tk.Frame(parent, bg=BG)
        head.pack(fill="x", pady=(13, 7))
        tk.Label(head, text="LIVE NOTIFICATIONS", bg=BG, fg=RED, font=("Consolas", 12, "bold")).pack(side="left")
        tk.Label(head, text="● LIVE FEED", bg=BG, fg=GREEN, font=("Consolas", 8)).pack(side="right")

        box = tk.Frame(parent, bg=PANEL, highlightbackground=RED_DIM, highlightthickness=1)
        box.pack(fill="both", expand=True)
        self.feed = tk.Listbox(box, bg=PANEL, fg=WHITE, selectbackground="#241015", selectforeground=WHITE, bd=0, highlightthickness=0, activestyle="none", font=("Consolas", 9), height=9)
        self.feed.pack(fill="both", expand=True, padx=8, pady=8)
        self.feed.insert(0, "  SYSTEM    Waiting for live notifications...")

    def _activity(self, parent):
        frame = tk.Frame(parent, bg=PANEL, height=105, highlightbackground=BORDER, highlightthickness=1)
        frame.pack(fill="x", pady=(10, 0))
        frame.pack_propagate(False)
        tk.Label(frame, text="RECENT ACTIVITY", bg=PANEL, fg=RED, font=("Consolas", 9, "bold")).pack(anchor="w", padx=12, pady=(9, 3))
        self.activity = tk.Text(frame, bg="#070b10", fg="#7f909e", bd=0, highlightthickness=0, font=("Consolas", 8), height=4)
        self.activity.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        self.activity.insert("end", "[SYSTEM] Listening for notifications...\n")
        self.activity.configure(state="disabled")

    def _right_panel(self, parent):
        right = tk.Frame(parent, bg=BG, width=255)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._panel_title(right, "SYSTEM METRICS")
        metrics = tk.Frame(right, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=10)
        metrics.pack(fill="x")
        self.metric_labels = {}
        for key in ["TOTAL", "IMPORTANT", "SPOKEN", "IGNORED"]:
            row = tk.Frame(metrics, bg=PANEL)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=key, bg=PANEL, fg=MUTED, font=("Consolas", 8, "bold")).pack(side="left")
            label = tk.Label(row, text="0", bg=PANEL, fg=WHITE, font=("Consolas", 13, "bold"))
            label.pack(side="right")
            self.metric_labels[key] = label

        self._panel_title(right, "THREAT / IMPORTANCE")
        threat = tk.Frame(right, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, padx=12, pady=14)
        threat.pack(fill="x")
        self.threat_label = tk.Label(threat, text="0%", bg=PANEL, fg=RED, font=("Consolas", 27, "bold"))
        self.threat_label.pack(anchor="w")
        self.progress = ttk.Progressbar(threat, maximum=100, length=205, mode="determinate")
        self.progress.pack(fill="x", pady=9)
        tk.Label(threat, text="SECURITY     ████████", bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack(anchor="w")
        tk.Label(threat, text="COMMUNICATION ██████", bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack(anchor="w")
        tk.Label(threat, text="PROMOTIONS   ██", bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack(anchor="w")

        self._panel_title(right, "QUICK CONTROLS")
        controls = tk.Frame(right, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, padx=10, pady=10)
        controls.pack(fill="x")
        self._toggle(controls, "VOICE / TTS", self.voice_enabled)
        self._toggle(controls, "PHONE LINK", self.phone_link_enabled)
        tk.Label(controls, text="IMPORTANCE THRESHOLD", bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack(anchor="w", pady=(12, 2))
        tk.Scale(controls, from_=1, to=15, orient="horizontal", variable=self.threshold, bg=PANEL, fg=WHITE, troughcolor="#291016", activebackground=RED, highlightthickness=0, bd=0, length=210).pack()

    def _panel_title(self, parent, text):
        tk.Label(parent, text=text, bg=BG, fg=RED, font=("Consolas", 9, "bold")).pack(anchor="w", pady=(13, 6))

    def _toggle(self, parent, text, variable):
        tk.Checkbutton(parent, text="●  " + text, variable=variable, bg=PANEL, fg=WHITE, selectcolor="#270d12", activebackground=PANEL, activeforeground=WHITE, bd=0, highlightthickness=0, font=("Consolas", 8, "bold")).pack(anchor="w", pady=3)

    def _bottom_status(self):
        bar = tk.Frame(self, bg="#080b0f", height=30, highlightbackground=BORDER, highlightthickness=1)
        bar.pack(fill="x")
        tk.Label(bar, text="●  ALL SYSTEMS NOMINAL", bg="#080b0f", fg=GREEN, font=("Consolas", 8, "bold")).pack(side="left", padx=15)
        tk.Label(bar, text="PYTHON  •  WINDOWS NOTIFICATION API  •  TTS", bg="#080b0f", fg=MUTED, font=("Consolas", 7)).pack(side="right", padx=15)

    def _tick_clock(self):
        self.clock_label.configure(text=time.strftime("%H:%M:%S"))
        self.after(1000, self._tick_clock)

    def settings(self):
        return {"threshold": self.threshold.get(), "voice_enabled": self.voice_enabled.get(), "phone_link_enabled": self.phone_link_enabled.get()}

    def on_notification(self, event):
        self.after(0, self._apply_notification, event)

    def _apply_notification(self, event):
        self.received += 1
        if event["important"]:
            self.important += 1
        else:
            self.ignored += 1
        if event["spoken"]:
            self.spoken += 1
        self.notifications.insert(0, event)
        self.notifications = self.notifications[:50]

        icon = "[!!]" if event["important"] else "[--]"
        source = "PHONE LINK" if event["phone_link"] else event["app"].upper()
        state = "SPOKEN" if event["spoken"] else ("IMPORTANT" if event["important"] else "IGNORED")
        line = f"{icon}  {source:<16}  {event['message'][:52]:<52}  P{event['score']:<2}  {state}"
        self.feed.insert(0, line)
        if self.feed.size() > 40:
            self.feed.delete(40, "end")
        self._activity_line(f"[{time.strftime('%H:%M:%S')}] {source}: {state} / priority {event['score']}")
        self._refresh_metrics()

    def _activity_line(self, text):
        self.activity.configure(state="normal")
        self.activity.insert("end", text + "\n")
        self.activity.see("end")
        self.activity.configure(state="disabled")

    def _refresh_metrics(self):
        self.metric_labels["TOTAL"].configure(text=str(self.received))
        self.metric_labels["IMPORTANT"].configure(text=str(self.important))
        self.metric_labels["SPOKEN"].configure(text=str(self.spoken))
        self.metric_labels["IGNORED"].configure(text=str(self.ignored))
        ratio = round((self.important / self.received) * 100) if self.received else 0
        self.threat_label.configure(text=f"{ratio}%")
        self.progress["value"] = ratio


if __name__ == "__main__":
    NotificationDashboard().mainloop()
