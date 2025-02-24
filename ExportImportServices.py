# -*- coding: utf-8 -*-
"""
Provides a base for export and import services and handles encryption service dependency.
"""

from typing import Dict, Any
from DataEncryption import DataEncryption
from abc import ABC, abstractmethod

class ExportImportServices(ABC):
    """
    Base class for export and import services with encryption handling.
    """

    def __init__(self, encryptionService: DataEncryption, config: Dict):
        """
        Initialize encryption service and configuration settings.
        """
        self._encryptionService = encryptionService
        self._config = config

    @abstractmethod
    def exportData(self) -> bytes:
        """
        Exports data.
        """
        pass

    @abstractmethod
    def importData(self) -> None:
        """
        Imports data.
        """
        pass

    def _encrypt(self, data: str) -> bytes:
        """
        Encrypts data using the encryption service.
        """
        return self._encryptionService.encrypt(data)

    def _decrypt(self, encryptedData: bytes) -> str:
        """
        Decrypts data using the encryption service.
        """
        return self._encryptionService.decrypt(encryptedData)
