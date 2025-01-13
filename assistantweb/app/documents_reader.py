# app/document_reader.py
from typing import Dict, Optional
import PyPDF2
import docx
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

class DocumentReader:
    def __init__(self):
        load_dotenv()

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
        
        if file_extension not in readers:
            raise ValueError(f"Unsupported file type: {file_extension}")
            
        return readers[file_extension](filepath)

    def read_pdf(self, filepath: str) -> Dict[str, str]:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ' '.join(page.extract_text() for page in reader.pages)
        return self._create_document_dict(filepath, content, 'pdf')

    def read_word(self, filepath: str) -> Dict[str, str]:
        doc = docx.Document(filepath)
        content = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        return self._create_document_dict(filepath, content, 'word')

    def read_excel(self, filepath: str) -> Dict[str, str]:
        try:
            df = pd.read_excel(filepath)
            content = df.to_string()
            return self._create_document_dict(filepath, content, 'excel')
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")

    def read_csv(self, filepath: str) -> Dict[str, str]:
        try:
            df = pd.read_csv(filepath)
            content = df.to_string()
            return self._create_document_dict(filepath, content, 'csv')
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")

    def read_text(self, filepath: str) -> Dict[str, str]:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return self._create_document_dict(filepath, content, 'text')

    def _create_document_dict(self, filepath: str, content: str, doc_type: str) -> Dict[str, str]:
        return {
            "title": Path(filepath).name,
            "content": content,
            "source": str(filepath),
            "type": doc_type,
            "summary": content[:500] if content else ""
        }