import fitz  # PyMuPDF
from typing import List, Optional

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
        
        Returns:
            str: Extracted text from the PDF
        """
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            return full_text
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks for better processing.
        
        Args:
            text (str): Input text
            chunk_size (int): Size of each text chunk
            overlap (int): Number of characters to overlap between chunks
        
        Returns:
            List[str]: List of text chunks
        """
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i+chunk_size])
        return chunks