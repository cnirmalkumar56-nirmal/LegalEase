# Phase 2 – Requirement Analysis

## Functional Requirements
1. Accept document type.
2. Accept parties.
3. Accept terms and conditions.
4. Accept effective date.
5. Generate document using Gemini.
6. Display editable output.
7. Export TXT.
8. Export DOCX.
9. Export PDF.
10. Support optional branding/logo.

## Non-Functional Requirements
- Simple user interface.
- Reasonable response time.
- Input validation.
- Secure API-key storage using `.env`.
- Maintainable modular code.

## Software
- Python 3.10+
- FastAPI
- Uvicorn
- Streamlit
- Google Gemini API
- python-docx
- FPDF
- Pillow
- Requests
- python-dotenv
