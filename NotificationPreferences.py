from enum import Enum

class NotificationFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class NotificationPreferences:
    def __init__(self, frequency: NotificationFrequency, is_enabled: bool):
        self.frequency = frequency
        self.is_enabled = is_enabled

    def __repr__(self):
        return f"NotificationPreferences(frequency={self.frequency}, is_enabled={self.is_enabled})"
