# Notification Reader

A Python-based Windows notification reader that speaks **only important notifications** — including notifications surfaced through **Phone Link**.

## Current features

- Requests Windows notification access.
- Reads Windows toast notifications.
- Monitors for new notifications continuously.
- Deduplicates notifications by notification ID.
- Extracts source application and notification text.
- Uses a transparent rule-based importance score.
- Recognizes Phone Link / Link to Windows as a notification source.
- Gives communication apps a small priority boost without automatically reading every message.
- Speaks important notifications using local text-to-speech through `pyttsx3`.
- Keeps non-important and promotional notifications silent.

## Phone Link support

If Android notifications are mirrored to Windows through **Phone Link**, the reader evaluates the notification that Windows exposes.

Examples:

```text
Phone Link + missed call
→ IMPORTANT → read aloud

Phone Link + OTP / payment / security alert
→ IMPORTANT → read aloud

Phone Link + ordinary chat message
→ usually silent unless it contains an importance signal

Phone Link + promotional notification
→ silent
```

The project does not directly connect to the phone. It reads notifications that are already available to the Windows notification system.

## How importance works

The classifier is intentionally transparent and local — no external AI/API is required.

- Strong signals such as OTP/security codes, fraud warnings, payments/transactions, emergencies, urgent alerts and missed calls get a high score.
- Important words such as meeting, deadline, interview, job, delivery or reminder add score.
- Communication apps such as WhatsApp, Telegram, Messages and Phone Link receive a small priority boost.
- Promotional/noise phrases such as sales, discounts, suggested friends and download-complete messages are penalized.
- A notification is spoken only when its final score reaches the configured threshold.

You can customize the rules in `index.py` using:

- `COMMUNICATION_APPS`
- `PHONE_LINK_APPS`
- `IMPORTANT_KEYWORDS`
- `STRONG_KEYWORDS`
- `IGNORE_KEYWORDS`
- `IMPORTANCE_THRESHOLD`

## Requirements

- Windows 10/11
- Python 3.x
- Windows Runtime (`winrt`) packages listed in `requirements.txt`
- `pyttsx3`

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
APP: Phone Link
TEXT: Missed call from Rahul
SCORE: 8
🚨 IMPORTANT
🔊 SPEAKING: Important notification from Phone Link. Missed call from Rahul
```

For an ordinary notification:

```text
🔔 NEW NOTIFICATION
APP: Chrome
TEXT: Download complete
SCORE: -5
ℹ️ Not important — silent
```

## Roadmap

- SQLite notification history
- Per-app priority profiles
- Better natural-language importance scoring
- Background startup with Windows
- Optional desktop UI
- Optional allow-list for specific contacts
