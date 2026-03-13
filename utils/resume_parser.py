import os
from pdfminer.high_level import extract_text
import docx
import re

def extract_text_from_pdf(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_text_from_doc(doc_path):
    try:
        doc = docx.Document(doc_path)
        return " ".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""

def extract_text_from_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.doc', '.docx']:
        return extract_text_from_doc(file_path)
    return ""

def extract_name(text):
    # Grab the first non-empty line as the name
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        line_clean = re.sub(r'[^a-zA-Z\s]', '', line).strip()
        # Ignore obvious resume headers
        if line_clean.lower() in ['resume', 'curriculum vitae', 'cv', 'profile']:
            continue
        
        # Check if length is reasonable for a name (1-4 words)
        words = line_clean.split()
        if 0 < len(words) <= 4:
            return line_clean.title()
            
    return "Candidate Name"

def extract_education(text):
    education_keywords = [
        "b.tech", "btech", "b.sc", "bsc", "bachelor", "master", 
        "m.tech", "mtech", "m.sc", "msc", "phd", "ph.d", 
        "degree", "diploma", "b.e", "b.e.", "bca", "mca",
        "university", "institute", "college"
    ]
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        line_lower = line.lower()
        if len(line) < 150: 
            for keyword in education_keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', line_lower):
                    return line.title()
                    
    return "Not Specified"

def extract_experience(text):
    text_lower = text.lower()
    
    # Check for direct year callouts
    match = re.search(r'(\d+)\+?\s*(years?|yrs?)(?:\s+of)?\s+experience', text_lower)
    if match:
        return match.group(0).title()
        
    if "intern" in text_lower or "internship" in text_lower:
        return "Internship Experience"
        
    # Check if a professional history section exists
    if "experience" in text_lower or "employment" in text_lower:
        return "Professional Experience"
            
    return "Entry Level"

def extract_structured_info(text):
    """
    Real extraction logic based on structural cues and Regex
    """
    return {
        "name": extract_name(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "certifications": [],
        "projects": []
    }
