# Phase 3 – Project Design

## Architecture

User
  |
  v
Streamlit Frontend
  |
  | HTTP POST /generate
  v
FastAPI Backend
  |
  v
GeminiDocumentGenerator
  |
  v
Google Gemini
  |
  v
Generated Document
  |
  +--> Editable Preview
  +--> TXT
  +--> DOCX
  +--> PDF

## Modules
- `frontend/app.py` – user interface
- `backend/main.py` – FastAPI application
- `backend/routes.py` – API route and validation
- `ai_core/gemini_generator.py` – Gemini integration
- `document_utils/formatters.py` – TXT/DOCX/PDF and preview formatting
