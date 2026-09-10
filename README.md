# Notification Reader

A Python-based Windows notification reader using the Windows Runtime notification management APIs.

## Current features

- Requests Windows notification access.
- Reads existing Windows toast notifications.
- Prints notification ID.
- Prints the source application name.
- Extracts text elements from the notification.

## Requirements

- Windows 10/11
- Python 3.x
- Windows Runtime (`winrt`) packages listed in `requirements.txt`

## Setup

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run

```bash
python index.py
```

On first run, Windows may ask for notification access. Allow access so the reader can query notifications.

## Roadmap

- Live notification monitoring
- Notification change events
- Deduplication and history
- SQLite storage
- Filtering and search
- Text-to-speech
