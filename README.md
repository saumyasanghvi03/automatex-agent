# AutomateX Agent

AutomateX is an AI-powered agent that processes documents to extract, qualify, and store lead information. This project provides the initial implementation for parsing documents and extracting basic lead data.

## Features

- Extracts text from `.pdf`, `.docx`, and `.csv` files.
- Identifies potential leads by extracting names and email addresses from the text.
- Outputs the extracted leads in a structured JSON format.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd automatex-agent
    ```

2.  **Install dependencies:**
    Ensure you have Python 3 installed. Then, install the required libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The agent can be run from the command line. It is currently configured to process a sample document located in the `documents/` directory.

1.  **Run the agent:**
    ```bash
    python3 main.py
    ```

2.  **Output:**
    The script will print the extracted text from the sample document and a list of extracted leads in JSON format to the console.

## Next Steps

This is the foundational version of the agent. Future development will include:
- Advanced lead qualification and scoring.
- Integration with CRM systems and databases like Google Sheets or Airtable.
- Personalized email outreach generation.
