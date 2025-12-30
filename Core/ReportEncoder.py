#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report Encoder/Decoder Module
Encodes and decodes reports for security
"""

import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import os

class ReportEncoder:
    """Encode and decode reports"""
    
    def __init__(self, password=None):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "Reports"
        self.password = password or "default_password_change_me"
        self.key = self._derive_key(self.password)
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password):
        """Derive encryption key from password"""
        password_bytes = password.encode()
        salt = b'appleosint_salt_2024'  # In production, use random salt
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encode_report(self, report_file_path, output_path=None):
        """Encode a report file"""
        report_path = Path(report_file_path)
        
        if not report_path.exists():
            raise FileNotFoundError(f"Report file not found: {report_file_path}")
        
        # Read report
        with open(report_path, 'rb') as f:
            report_data = f.read()
        
        # Encrypt
        encrypted_data = self.cipher.encrypt(report_data)
        
        # Save encoded report
        if output_path is None:
            output_path = report_path.with_suffix('.enc')
        else:
            output_path = Path(output_path)
        
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        
        return output_path
    
    def decode_report(self, encoded_file_path, output_path=None, password=None):
        """Decode an encoded report file"""
        encoded_path = Path(encoded_file_path)
        
        if not encoded_path.exists():
            raise FileNotFoundError(f"Encoded file not found: {encoded_file_path}")
        
        # Use provided password or default
        if password:
            key = self._derive_key(password)
            cipher = Fernet(key)
        else:
            cipher = self.cipher
        
        # Read encoded file
        with open(encoded_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
        except Exception as e:
            raise ValueError(f"Decryption failed. Wrong password? Error: {str(e)}")
        
        # Save decoded report
        if output_path is None:
            output_path = encoded_path.with_suffix('.json')
        else:
            output_path = Path(output_path)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        return output_path



