import fitz  # PyMuPDF
import docx
import pandas as pd
import os
import re
import json

def _extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error processing PDF {file_path}: {e}"

def _extract_text_from_docx(file_path):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error processing DOCX {file_path}: {e}"

def _extract_text_from_csv(file_path):
    """Extracts text content from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        return f"Error processing CSV {file_path}: {e}"

def _score_lead(line_text):
    """
    Scores a lead based on keywords found in the text.
    Returns a score (0-100) and a category ('Hot', 'Warm', 'Cold').
    """
    score = 50  # Base score
    category = 'Warm'

    hot_keywords = ['ceo', 'head of', 'founder', 'cto', 'president']
    cold_keywords = ['general inquiries', 'contact@', 'info@']

    line_lower = line_text.lower()

    if any(keyword in line_lower for keyword in hot_keywords):
        score = 90
        category = 'Hot'
    elif any(keyword in line_lower for keyword in cold_keywords):
        score = 20
        category = 'Cold'

    return score, category

def extract_leads_from_text(text):
    """
    Extracts lead information (name, email, title, company) from a block of text.
    """
    leads = []
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    lines = text.split('\n')
    for line in lines:
        emails = re.findall(email_regex, line)
        if emails:
            email = emails[0]

            # Final regex attempt
            pattern = re.compile(r'([\w\s]+),\s(.*?)\s(?:at|of)\s(.*?)(?:\.|\sContact|$)', re.IGNORECASE)
            match = pattern.search(line)

            if match:
                name = match.group(1).replace('-', '').strip()
                title = match.group(2).strip()
                company = match.group(3).strip()
            else:
                # Fallback for simple cases
                name = line.split(',')[0].replace('-', '').strip()
                title = "N/A"
                company = "N/A"

            # Cleanup for general inquiries
            if "general inquiries" in line.lower():
                name = "General Inquiry"
                company = "N/A"
                title = "N/A"


            score, category = _score_lead(line)

            leads.append({
                "name": name if name else "N/A",
                "email": email,
                "company": company,
                "title": title,
                "phone": "N/A",
                "location": "N/A",
                "score": score,
                "category": category
            })
    return leads

def extract_text_from_document(file_path):
    """
    Extracts text from a document based on its file extension.
    """
    if not os.path.exists(file_path):
        return "Error: File not found."

    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.pdf':
        return _extract_text_from_pdf(file_path)
    elif file_extension.lower() == '.docx':
        return _extract_text_from_docx(file_path)
    elif file_extension.lower() == '.csv':
        return _extract_text_from_csv(file_path)
    else:
        return "Error: Unsupported file type."

if __name__ == "__main__":
    file_path = 'documents/sample_document.docx'

    if os.path.exists(file_path):
        print(f"Processing file: {file_path}")
        text = extract_text_from_document(file_path)

        print("\n--- Extracted Text ---")
        print(text)
        print("----------------------\n")

        leads = extract_leads_from_text(text)

        print("--- Extracted Leads ---")
        print(json.dumps(leads, indent=2))
        print("-----------------------")
    else:
        print(f"Error: Sample file not found at {file_path}")
