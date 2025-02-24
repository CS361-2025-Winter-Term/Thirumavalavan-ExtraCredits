from UserProfile import UserProfile

class UserStorageManager:
    def __init__(self):
        self._users = {}

    def findUserByUsername(self, username: str):
        return self._users.get(username)

    def saveNewUser(self, user_profile: UserProfile, hashed_password: str) -> bool:
        if self.findUserByUsername(user_profile.username):
            return False
        # Save the user with the hashed password
        self._users[user_profile.username] = {
            "user_profile": user_profile,
            "hashed_password": hashed_password
        }
        return True

    def saveUserToDatabase(self, user_profile: UserProfile):
        return self.saveNewUser(user_profile, "")
