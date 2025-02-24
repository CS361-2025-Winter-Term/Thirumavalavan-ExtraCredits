# UserProfile.py

from NotificationPreferences import NotificationPreferences

class UserProfile:
    def __init__(self, username: str, email: str, notification_preferences: NotificationPreferences):
        self.username = username
        self.email = email
        self.notification_preferences = notification_preferences

    def __repr__(self):
        return (f"UserProfile(username='{self.username}', email='{self.email}', "
                f"notification_preferences={self.notification_preferences})")
