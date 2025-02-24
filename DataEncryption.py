# -*- coding: utf-8 -*-
"""
Handles encryption and decryption of data using AES.
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib
import base64

class DataEncryption:
    """
    Handles encryption and decryption of data using AES.
    """

    def __init__(self, key: bytes):
        """
        Initialize encryption service with a security key.
        """
        self._key = self._derive_key(key)

    def _derive_key(self, key: bytes) -> bytes:
        """
        Derive a 32-byte key using SHA-256 to ensure a fixed-length key for AES encryption.
        """
        return hashlib.sha256(key).digest()

    def encrypt(self, data: str) -> bytes:
        """
        Encrypts data using AES encryption (CBC mode).
        """
        try:
            iv = get_random_bytes(16)
            cipher = AES.new(self._key, AES.MODE_CBC, iv)
            padded_data = pad(data.encode('utf-8'), AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            return base64.b64encode(iv + encrypted_data)
        except Exception as e:
            raise RuntimeError(f"Encryption failed: {e}")

    def decrypt(self, encryptedData: bytes) -> str:
        """
        Decrypts data using AES decryption (CBC mode).
        """
        try:
            encrypted_data = base64.b64decode(encryptedData)
            iv = encrypted_data[:16]
            encrypted_data = encrypted_data[16:]
            cipher = AES.new(self._key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Decryption failed: {e}")

    def generate_sha256_hash(self, data: str) -> str:
        """
        Generates SHA-256 hash for the given data.
        """
        sha256 = hashlib.sha256()
        sha256.update(data.encode('utf-8'))
        return sha256.hexdigest()

    def verify_integrity(self, data: str, expected_hash: str) -> bool:
        """
        Verifies the integrity of the data by comparing the calculated hash with the expected hash.
        """
        calculated_hash = self.generate_sha256_hash(data)
        return calculated_hash == expected_hash
