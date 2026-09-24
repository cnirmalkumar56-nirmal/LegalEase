# LegalEase – AI-Powered Legal Document Generator

LegalEase is a student project that uses Streamlit, FastAPI and Google Gemini to generate editable legal-document drafts from user inputs.

## Features
- Document types: Agreement, Contract, NDA, Lease Agreement, Employment Offer Letter and custom types
- Parties, terms and effective date inputs
- Gemini-powered document generation
- Editable preview
- TXT, DOCX and PDF downloads
- DOCX/PDF branding with an optional logo
- FastAPI `/generate` endpoint
- Health-check endpoint
- Local deployment

## Important
LegalEase generates drafts for educational/general informational use. It is not a substitute for advice from a qualified lawyer. Users should have generated documents reviewed where legally appropriate.

## Setup

### 1. Create a virtual environment
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Gemini
Copy `.env.example` to `.env` and put your API key in `GEMINI_API_KEY`.

### 4. Start FastAPI
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start Streamlit in another terminal
```bash
streamlit run frontend/app.py
```

Open the Streamlit URL shown in the terminal.

## API
POST `/generate`

Example JSON:
```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Confidentiality must be maintained; Payment within 30 days",
  "effective_date": "2026-09-22"
}
```

## Project structure
```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── routes.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── document_utils/
│   ├── __init__.py
│   └── formatters.py
├── frontend/
│   └── app.py
├── assets/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```
