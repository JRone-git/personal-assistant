from typing import Dict, Optional
import PyPDF2
import docx
import pandas as pd
import os
import openpyxl
import csv
from pathlib import Path

class DocumentReader:
    def read_file(self, filepath: str) -> Dict[str, str]:
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
