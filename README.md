# Notification Reader

A Python-based Windows notification reader that speaks **only important notifications**.

## Current features

- Requests Windows notification access.
- Reads existing Windows toast notifications.
- Monitors for new notifications continuously.
- Deduplicates notifications by notification ID.
- Extracts source application and notification text.
- Uses a transparent keyword-based importance classifier.
- Speaks important notifications using Windows text-to-speech through `pyttsx3`.
- Keeps non-important notifications completely silent.

## How importance works

The first version intentionally uses a simple, explainable rule-based classifier instead of an external AI service.

Strong signals such as OTP/security codes, fraud warnings, payments/transactions, emergencies, urgent alerts, and missed calls are immediately treated as important. Other notifications need multiple importance signals before they are spoken.

You can customize `IMPORTANT_KEYWORDS` in `index.py` for your own definition of important.

## Requirements

- Windows 10/11
- Python 3.x
- Windows Runtime (`winrt`) packages listed in `requirements.txt`

## Setup

```bash
python -m venv venv
venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

## Run

```bash
python index.py
```

On first run, Windows may ask for notification access. Allow access so the reader can query notifications.

The reader ignores notifications that already exist when it starts. Only newly detected notifications are evaluated and spoken.

Press `Ctrl+C` to stop the reader.

## Example

```text
🔔 NEW NOTIFICATION
APP: WhatsApp
TEXT: Meeting at 7 PM
🚨 IMPORTANT
🔊 SPEAKING: Important notification from WhatsApp. Meeting at 7 PM
```

For an ordinary notification:

```text
🔔 NEW NOTIFICATION
APP: Chrome
TEXT: Download complete
ℹ️ Not important — silent
```

## Roadmap

- SQLite notification history
- Configurable importance rules
- Per-app priority settings
- Better natural-language importance scoring
- Background startup with Windows
- Optional desktop UI
