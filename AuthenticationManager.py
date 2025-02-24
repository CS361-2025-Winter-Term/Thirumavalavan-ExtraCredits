import re
from enum import Enum
from UserStorageManager import UserStorageManager
from UserProfile import UserProfile

class AuthenticationManager:
    class RegistrationStatus(Enum):
        SUCCESS = 0
        USER_ALREADY_EXISTS = 1
        INVALID_USERNAME = 2
        INVALID_PASSWORD = 3
        INVALID_EMAIL = 4
        UNKNOWN_ERROR = 5

    def __init__(self):
        self.user_storage = UserStorageManager()

    def validateUsername(self, username: str) -> bool:
        # Username must contain only letters
        return username.isalpha()

    def validatePassword(self, password: str) -> bool:
        # Password must be at least 8 characters long
        return len(password) >= 8

    def validateEmail(self, email: str) -> bool:
        # A simple regex for email validation
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def hashPassword(self, password: str) -> str:
        # Implement hashing (for now, just using a dummy hash)
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def registerUser(self, user_profile: UserProfile, password: str) -> Enum:
        # Validate username
        if not self.validateUsername(user_profile.username):
            return self.RegistrationStatus.INVALID_USERNAME

        # Validate password
        if not self.validatePassword(password):
            return self.RegistrationStatus.INVALID_PASSWORD

        # Validate email
        if not self.validateEmail(user_profile.email):
            return self.RegistrationStatus.INVALID_EMAIL

        # Check if user already exists
        if self.user_storage.findUserByUsername(user_profile.username):
            return self.RegistrationStatus.USER_ALREADY_EXISTS

        # Hash the password and save the new user
        hashed_password = self.hashPassword(password)
        saved = self.user_storage.saveNewUser(user_profile, hashed_password)
        if saved:
            return self.RegistrationStatus.SUCCESS
        else:
            return self.RegistrationStatus.UNKNOWN_ERROR
