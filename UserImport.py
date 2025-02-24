# -*- coding: utf-8 -*-
"""
Handles importing user profile data securely, including user habits.
"""

import sqlite3
import json
import bcrypt
from typing import Dict
from ExportImportServices import ExportImportServices
from DataEncryption import DataEncryption

class UserImport(ExportImportServices):
    """
    Handles importing user profile data securely.
    """

    def __init__(self, encryptionService: DataEncryption, config: Dict, db_path: str):
        """
        Initialize import service with encryption, config, and database path.
        """
        super().__init__(encryptionService, config)
        self._db_path = db_path

    def importData(self) -> None:
        """
        Verify password in a loop; then proceed with import process.
        """
        # Partition: ProfileSettings
        self.render_profile_settings()
        self.handle_import_data_button_click()

        # Loop: Verify password until successful
        while not self._verify_password():
            print("Invalid password. Try again.")
        # Proceed with import branch.
        # Partition: UserImport / Import Process
        exported_file = self.identify_file()
        if self.check_file_format(exported_file):
            integrity_verified = self.verify_file_integrity(exported_file)
            if integrity_verified:
                # Partition: DataEncryption
                decrypted_data = self._decrypt(exported_file)
                imported_data = self._deserializeData(decrypted_data)
                self._updateUserData(imported_data)
                print("Import successful.")
            else:
                print("File integrity verification failed.")
        else:
            print("Invalid file format.")

    def render_profile_settings(self):
        # Placeholder for rendering profile settings
        pass

    def handle_import_data_button_click(self):
        # Placeholder for handling import button click
        pass

    def _verify_password(self) -> bool:
        """Prompt and verify password using bcrypt."""
        password = input("Enter password for import: ")
        hashed_password = b"$2b$12$uI6Mzk5ixA3Mk8b/WdR4tuyR1/Lj1eVh0jJlPBzY8E4Skd5HuoBkW"  # Example hash for 'password123'
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def identify_file(self) -> bytes:
        """
        Identify and read the exported file.
        """
        # In a real scenario, you might allow user to choose a file.
        file_path = input("Enter the path of the export file: ")
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except IOError as e:
            print(f"Error reading file: {e}")
            return b""

    def check_file_format(self, exported_file: bytes) -> bool:
        """
        Check that the file format is valid.
        """
        # For demonstration, assume non-empty file is valid.
        return bool(exported_file)

    def verify_file_integrity(self, exported_file: bytes) -> bool:
        """
        Verify file integrity. In a full implementation, you might compare hashes.
        """
        # For now, we assume the file is always intact.
        return True

    def _deserializeData(self, data: str) -> Dict:
        """
        Converts structured data back to dictionary form.
        """
        return json.loads(data)

    def _updateUserData(self, importedData: Dict) -> None:
        """
        Updates user habits and statistics in the database.
        """
        try:
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            # Insert habits
            for habit in importedData.get("habits", []):
                cursor.execute("INSERT OR IGNORE INTO habits (habit_name) VALUES (?)", (habit,))
            # Update completion rates
            for habit, rate in importedData.get("completionRates", {}).items():
                cursor.execute(
                    "UPDATE habit_statistics SET completion_rate = ? WHERE habit_name = ?",
                    (rate, habit),
                )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
