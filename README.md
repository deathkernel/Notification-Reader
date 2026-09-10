# Notification Reader

A Python-based Windows notification reader with a futuristic **ULTRON-inspired** desktop dashboard. It speaks **only important notifications**, including notifications surfaced through **Phone Link**.

## Current features

- Windows toast notification access.
- Continuous notification monitoring.
- Notification deduplication.
- App and message extraction.
- Transparent, configurable importance scoring.
- Phone Link / Link to Windows support.
- Local Windows text-to-speech through `pyttsx3`.
- Futuristic red/black HUD-style desktop dashboard built with Tkinter.
- Animated AI core and live system clock.
- Live notification feed connected to the real notification engine.
- Real-time Received / Important / Spoken / Ignored counters.
- Voice and Phone Link controls.
- Live importance threshold control.
- Recent activity log.

## Run the dashboard

```bash
python app.py
```

The dashboard and notification engine start together. The engine runs in a background thread, while Tkinter stays responsive and receives live notification events.

## Run engine only

```bash
python index.py
```

## Phone Link

If Android notifications are mirrored to Windows through Phone Link, the reader evaluates the notification exposed by Windows. It does not connect directly to the phone.

Examples:

```text
Phone Link + missed call
→ HIGH PRIORITY → read aloud

Phone Link + OTP / payment / security alert
→ HIGH PRIORITY → read aloud

Phone Link + ordinary chat
→ usually silent

Phone Link + promotion
→ silent
```

## Importance scoring

The classifier is intentionally local and explainable. App priorities, strong keywords, context keywords and noise keywords contribute to the final score. The dashboard threshold controls the minimum score required for speech.

Rules live in **`config.py`**.

## Project structure

```text
Notification-Reader/
├── app.py           # Desktop launcher and engine/UI bridge
├── ui.py            # ULTRON-inspired Tkinter dashboard
├── index.py         # Windows listener, scoring pipeline and TTS
├── config.py        # App priorities and scoring rules
├── requirements.txt
└── README.md
```

## Requirements

- Windows 10/11
- Python 3.x
- Windows Runtime (`winrt`) packages listed in `requirements.txt`
- `pyttsx3`
- Tkinter (normally included with standard Windows Python)

## Setup

```bash
python -m venv venv
venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

## Privacy

Notification content can contain sensitive information such as OTPs and banking details. The current system runs locally, but TTS can be audible to people nearby. A privacy/masking mode is planned.

## Roadmap

- SQLite notification history.
- Privacy/masking mode for sensitive notifications.
- Per-contact priority profiles.
- Better natural-language importance scoring.
- Windows startup/background mode.
- Custom themes and additional HUD panels.
