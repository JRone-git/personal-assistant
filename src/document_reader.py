from typing import Dict, Optional
import PyPDF2
import docx
import pandas as pd
import os
import openpyxl
import csv
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class DocumentReader:
    def __init__(self):
        self.salt = b'some_fixed_salt' # Keep this secret and consistent

    def _generate_key_from_password(self, password: str) -> bytes:
        password_bytes = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key

    def encrypt_file(self, filepath: str, password: str) -> bytes:
        key = self._generate_key_from_password(password)
        f = Fernet(key)
        with open(filepath, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        return encrypted_data

    def decrypt_file(self, encrypted_data: bytes, password: str) -> bytes:
        key = self._generate_key_from_password(password)
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data

    def read_file(self, filepath: str, password: str = None, encrypted: bool = False) -> Dict[str, str]:
        file_extension = Path(filepath).suffix.lower()
        readers = {
            '.pdf': self.read_pdf,
            '.docx': self.read_word,
            '.doc': self.read_word,
            '.xlsx': self.read_excel,
            '.xls': self.read_excel,
            '.csv': self.read_csv,
            '.txt': self.read_text
        }
        
        if file_extension in readers:
            if encrypted and password:
                with open(filepath, 'rb') as file:
                    encrypted_data = file.read()
                decrypted_data = self.decrypt_file(encrypted_data, password)
                temp_filepath = filepath + ".temp"
                with open(temp_filepath, 'wb') as temp_file:
                    temp_file.write(decrypted_data)
                content = readers[file_extension](temp_filepath)
                os.remove(temp_filepath)
                return content
            else:
                return readers[file_extension](filepath)
        else:
            supported = ', '.join(readers.keys())
            raise ValueError(f"Supported formats are: {supported}")

    def read_pdf(self, filepath: str) -> Dict[str, str]:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ''
            for page in reader.pages:
                content += page.extract_text()
        
        return {
            "title": Path(filepath).name,
            "content": content,
            "source": filepath,
            "type": "pdf"
        }

    def read_word(self, filepath: str) -> Dict[str, str]:
        doc = docx.Document(filepath)
        content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        
        return {
            "title": Path(filepath).name,
            "content": content,
            "source": filepath,
            "type": "word"
        }

    def read_excel(self, filepath: str) -> Dict[str, str]:
        df = pd.read_excel(filepath)
        content = df.to_string()
        
        return {
            "title": Path(filepath).name,
            "content": content,
            "source": filepath,
            "type": "excel"
        }

    def read_csv(self, filepath: str) -> Dict[str, str]:
        df = pd.read_csv(filepath)
        content = df.to_string()
        
        return {
            "title": Path(filepath).name,
            "content": content,
            "source": filepath,
            "type": "csv"
        }

    def read_text(self, filepath: str) -> Dict[str, str]:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        return {
            "title": Path(filepath).name,
            "content": content,
            "source": filepath,
            "type": "text"
        }
