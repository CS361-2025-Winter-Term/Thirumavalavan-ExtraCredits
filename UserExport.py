# -*- coding: utf-8 -*-
"""
Handles exporting user profile data securely, including user habits.
"""

import sqlite3
import json
import bcrypt
from typing import Dict
from ExportImportServices import ExportImportServices
from DataEncryption import DataEncryption

class UserExport(ExportImportServices):
    """
    Handles exporting user profile data securely.
    """

    def __init__(self, encryptionService: DataEncryption, config: Dict, db_path: str):
        """
        Initialize export service with encryption, config, and database path.
        """
        super().__init__(encryptionService, config)
        self._db_path = db_path

    def exportData(self) -> bytes:
        """
        Verify password in a loop until success; then serialize, encrypt, and generate export file.
        """
        # Partition: ProfileSettings
        self.render_profile_settings()
        self.handle_export_data_button_click()

        # Loop: Verify password until successful
        while not self._verify_password():
            print("Invalid password. Try again.")
        # When password verified (Yes branch), proceed with export.
        # Partition: UserExport / Export Process
        user_data = self._serializeData()
        # Partition: DataEncryption
        encrypted_data = self._encrypt(user_data)
        export_file = self.generate_export_file(encrypted_data)
        self.save_export_file(export_file)
        print("Export successful.")
        return encrypted_data  # or export_file as needed

    def render_profile_settings(self):
        # Placeholder for rendering profile settings
        pass

    def handle_export_data_button_click(self):
        # Placeholder for handling export button click
        pass

    def _verify_password(self) -> bool:
        """Prompt and verify password using bcrypt."""
        password = input("Enter password for export: ")
        hashed_password = b"$2b$12$uI6Mzk5ixA3Mk8b/WdR4tuyR1/Lj1eVh0jJlPBzY8E4Skd5HuoBkW"  # Example hash for 'password123'
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def _serializeData(self) -> str:
        """
        Retrieves user profile data from the database and structures it for export.
        """
        data = {
            "habits": self._get_habits(),
            "completionRates": self._get_completion_rates(),
            "correlationMatrix": self._generate_correlation_matrix(),
        }
        return json.dumps(data)

    def _get_habits(self):
        try:
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT habit_name FROM habits")
            habits = [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            habits = []
        finally:
            conn.close()
        return habits

    def _get_completion_rates(self):
        try:
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT habit_name, completion_rate FROM habit_statistics")
            completionRates = {row[0]: row[1] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            completionRates = {}
        finally:
            conn.close()
        return completionRates

    def _generate_correlation_matrix(self):
        # Placeholder for correlation matrix generation logic.
        return {}

    def generate_export_file(self, encrypted_data: bytes) -> str:
        """
        Generate an export file name or content.
        """
        # Return the filename
        return "user_export.dat"

    def save_export_file(self, export_file: str):
        """
        Save the export file to disk.
        """
        with open(export_file, "wb") as f:
            # Normally, you would save the encrypted data,
            # but since export_file is a filename here, this is a placeholder.
            f.write(b"Exported data placeholder")
