#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QR Code Generator Module
Generates QR codes for file transfer
"""

import qrcode
from PIL import Image
from pathlib import Path
import json
import base64
from datetime import datetime

class QRCodeGenerator:
    """Generate QR codes for file transfer"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.qrcodes_path = self.base_path / "QRCodes"
        self.qrcodes_path.mkdir(exist_ok=True)
    
    def generate_file_qr(self, file_path, qr_size=10, border=4):
        """Generate QR code for a file (encodes file content)"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file and encode to base64
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        file_base64 = base64.b64encode(file_data).decode('utf-8')
        
        # Create data structure
        qr_data = {
            "filename": file_path.name,
            "data": file_base64,
            "timestamp": datetime.now().isoformat()
        }
        
        # Convert to JSON string
        qr_json = json.dumps(qr_data)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=qr_size,
            border=border,
        )
        qr.add_data(qr_json)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        qr_filename = f"qr_{file_path.stem}_{timestamp}.png"
        qr_path = self.qrcodes_path / qr_filename
        img.save(qr_path)
        
        return qr_path
    
    def generate_url_qr(self, url, qr_size=10, border=4):
        """Generate QR code for a URL"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=qr_size,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        qr_filename = f"qr_url_{timestamp}.png"
        qr_path = self.qrcodes_path / qr_filename
        img.save(qr_path)
        
        return qr_path
    
    def generate_text_qr(self, text, qr_size=10, border=4):
        """Generate QR code for text"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=qr_size,
            border=border,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        qr_filename = f"qr_text_{timestamp}.png"
        qr_path = self.qrcodes_path / qr_filename
        img.save(qr_path)
        
        return qr_path



