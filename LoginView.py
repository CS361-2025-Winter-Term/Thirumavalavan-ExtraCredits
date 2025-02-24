from UserProfile import UserProfile
from AuthenticationManager import AuthenticationManager
from NotificationPreferences import NotificationPreferences, NotificationFrequency

class LoginView:
    def __init__(self):
        self.auth_manager = AuthenticationManager()
    
    def readUsernameTextbox(self) -> str:
        return input("Enter username: ")
    
    def readPasswordTextbox(self) -> str:
        return input("Enter password: ")
    
    def readEmailTextbox(self) -> str:
        return input("Enter email: ")
    
    def readNotificationPreferences(self):
        # Reading notification preferences from user input
        frequency = input("Enter notification frequency (daily/weekly/monthly): ").strip().lower()
        is_enabled = input("Enable notifications? (yes/no): ").strip().lower() == "yes"
        freq_enum = NotificationFrequency.DAILY  # Default
        if frequency == "weekly":
            freq_enum = NotificationFrequency.WEEKLY
        elif frequency == "monthly":
            freq_enum = NotificationFrequency.MONTHLY
        return NotificationPreferences(freq_enum, is_enabled)
    
    def displayError(self, message: str):
        print("ERROR:", message)
    
    def transitionToHomeView(self, user_profile: UserProfile):
        print("Registration successful. Transitioning to home view for:", user_profile)
    
    def registerUser(self):
        # Begin activity flow
        print("Registration button clicked")
        username = self.readUsernameTextbox()
        password = self.readPasswordTextbox()
        email = self.readEmailTextbox()
        notification_preferences = self.readNotificationPreferences()
        
        # Create objects
        user_profile = UserProfile(username, email, notification_preferences)
        
        # Delegate registration to AuthenticationManager
        registration_status = self.auth_manager.registerUser(user_profile, password)
        
        if registration_status == self.auth_manager.RegistrationStatus.SUCCESS:
            self.transitionToHomeView(user_profile)
        else:
            if registration_status == self.auth_manager.RegistrationStatus.USER_ALREADY_EXISTS:
                self.displayError("Username already exists")
            elif registration_status == self.auth_manager.RegistrationStatus.UNKNOWN_ERROR:
                self.displayError("Registration failed. Internal error")
            elif registration_status == self.auth_manager.RegistrationStatus.INVALID_USERNAME:
                self.displayError("Username must use only letters")
            elif registration_status == self.auth_manager.RegistrationStatus.INVALID_PASSWORD:
                self.displayError("Password must be at least 8 characters long")
            elif registration_status == self.auth_manager.RegistrationStatus.INVALID_EMAIL:
                self.displayError("Invalid email address")
