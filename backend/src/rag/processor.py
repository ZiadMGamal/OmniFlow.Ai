import io
from typing import Dict, Any, List
import pandas as pd
from pypdf import PdfReader
from docx import Document


class FileProcessor:
    """Extracts raw text and basic metadata from various file formats"""
    
    @staticmethod
    def process_txt(file_content: bytes) -> Dict[str, Any]:
        text = file_content.decode("utf-8", errors="ignore")
        return {"text": text, "metadata": {"file_type": "txt"}}

    @staticmethod
    def process_pdf(file_content: bytes) -> Dict[str, Any]:
        reader = PdfReader(io.BytesIO(file_content))
        text_parts = []
        for i, page in enumerate(reader.pages):
            text_parts.append(f"--- Page {i+1} ---\n{page.extract_text()}")
        return {"text": "\n".join(text_parts), "metadata": {"file_type": "pdf", "pages": len(reader.pages)}}

    @staticmethod
    def process_docx(file_content: bytes) -> Dict[str, Any]:
        doc = Document(io.BytesIO(file_content))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return {"text": text, "metadata": {"file_type": "docx"}}

    @staticmethod
    def process_csv(file_content: bytes) -> Dict[str, Any]:
        df = pd.read_csv(io.BytesIO(file_content))
        text = df.to_string()
        return {"text": text, "metadata": {"file_type": "csv", "rows": len(df)}}

    @staticmethod
    def process_xlsx(file_content: bytes) -> Dict[str, Any]:
        df = pd.read_excel(io.BytesIO(file_content))
        text = df.to_string()
        return {"text": text, "metadata": {"file_type": "xlsx", "rows": len(df)}}

    @classmethod
    def process(cls, file_content: bytes, filename: str) -> Dict[str, Any]:
        ext = filename.split(".")[-1].lower()
        
        if ext == "txt":
            return cls.process_txt(file_content)
        elif ext == "pdf":
            return cls.process_pdf(file_content)
        elif ext == "docx":
            return cls.process_docx(file_content)
        elif ext == "csv":
            return cls.process_csv(file_content)
        elif ext == "xlsx":
            return cls.process_xlsx(file_content)
        else:
            # Fallback to pure text extraction attempt
            return cls.process_txt(file_content)
