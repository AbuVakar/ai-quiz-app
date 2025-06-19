# PDF Extraction utility (migrated from old mcq_env)
# Migrated the PDF extraction utility from the old mcq_env project to the new backend utils folder. This enables extracting text from PDF files for MCQ generation.

from PyPDF2 import PdfReader
import re
import spacy
from typing import List, Dict

# Load spaCy model for text processing
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract and clean text from a PDF file.
    """
    try:
        reader = PdfReader(file_path)
        text_chunks = []
        
        for page in reader.pages:
            text = page.extract_text()
            # Clean the text
            text = clean_text(text)
            if text.strip():
                text_chunks.append(text)
        
        return "\n".join(text_chunks)
    except Exception as e:
        raise Exception(f"Failed to process PDF: {str(e)}")

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.
    """
    # Replace multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters while preserving important punctuation
    text = re.sub(r'[^\w\s.,!?;:()\-\'\"]+', ' ', text)
    
    # Fix common OCR errors
    text = fix_ocr_errors(text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text

def fix_ocr_errors(text: str) -> str:
    """
    Fix common OCR errors in the text.
    """
    # Fix broken sentences
    text = re.sub(r'(?<=[a-z])[\.\s]+(?=[A-Z])', '. ', text)
    
    # Fix hyphenated words
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # Fix common character confusions
    replacements = {
        'l1': 'h',
        'rn': 'm',
        '0': 'o',
        '1': 'l'
    }
    for error, fix in replacements.items():
        text = text.replace(error, fix)
    
    return text

def extract_sections(text: str) -> List[Dict[str, str]]:
    """
    Extract sections from the text using NLP.
    """
    doc = nlp(text)
    sections = []
    current_section = ""
    current_title = "Introduction"
    
    for sent in doc.sents:
        # Heuristic for section detection
        if len(sent.text.strip()) < 50 and sent.text.isupper():
            # This might be a section title
            if current_section:
                sections.append({
                    "title": current_title,
                    "content": current_section.strip()
                })
            current_title = sent.text.strip()
            current_section = ""
        else:
            current_section += " " + sent.text
    
    # Add the last section
    if current_section:
        sections.append({
            "title": current_title,
            "content": current_section.strip()
        })
    
    return sections
