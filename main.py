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

def extract_leads_from_text(text):
    """
    Extracts lead information (name and email) from a block of text.
    """
    leads = []
    # Regex to find email addresses
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    lines = text.split('\n')
    for line in lines:
        emails = re.findall(email_regex, line)
        if emails:
            # For simplicity, we'll assume the name is on the same line as the email.
            # This is a basic heuristic and can be improved.
            name = line.replace(emails[0], '').strip()
            # Clean up potential extra characters or words
            name = re.sub(r'Email:?', '', name, flags=re.IGNORECASE).strip()
            name = re.sub(r'Contact:?', '', name, flags=re.IGNORECASE).strip()
            name = ' '.join(name.split()[:3]) # Assume name is at most 3 words

            for email in emails:
                leads.append({
                    "name": name if name else "N/A",
                    "email": email,
                    "company": "N/A",
                    "title": "N/A",
                    "phone": "N/A",
                    "location": "N/A"
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
