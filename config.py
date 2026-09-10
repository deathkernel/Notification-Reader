"""Configuration for the notification reader."""

# Minimum score required before text is spoken.
IMPORTANCE_THRESHOLD = 5

# How often Windows notification history is checked.
POLL_SECONDS = 2

# Apps with useful personal communication notifications.
APP_PRIORITIES = {
    "phone": 5,
    "phone link": 4,
    "link to windows": 4,
    "your phone": 4,
    "whatsapp": 3,
    "telegram": 3,
    "messages": 3,
    "google messages": 3,
    "messenger": 2,
    "gmail": 2,
    "outlook": 2,
    "calendar": 4,
    "google calendar": 4,
}

# Strong signals: one occurrence is enough to make a notification important.
STRONG_KEYWORDS = {
    "otp", "one-time password", "verification code", "security code",
    "fraud", "suspicious", "emergency", "critical", "urgent",
    "payment", "transaction", "debited", "credited", "bank", "upi",
    "missed call", "incoming call",
}

# Useful context signals. Multiple signals can combine into a high score.
IMPORTANT_KEYWORDS = {
    "important", "alert", "warning", "login", "sign in", "password",
    "security", "blocked", "due", "deadline", "appointment", "interview",
    "meeting", "exam", "assignment", "job", "offer", "delivery", "call",
    "call me", "reminder", "schedule", "flight", "ticket", "booking",
    "तुरंत", "जरूरी", "महत्वपूर्ण", "ओटीपी", "पेमेंट", "लेनदेन",
}

# Promotional/noise signals. These subtract points instead of being an
# absolute block, so a genuine security warning containing "promotion" is
# still allowed to win on stronger signals.
IGNORE_KEYWORDS = {
    "download complete", "update available", "suggested for you",
    "people you may know", "new follower", "friend suggestion", "promotion",
    "promoted", "sale", "discount", "advertisement", "recommended for you",
}
