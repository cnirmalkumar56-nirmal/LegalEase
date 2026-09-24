import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.model = None
        self.config_error = None

        if not self.api_key:
            self.config_error = (
                "GEMINI_API_KEY is missing. Add it to your .env file or use the local demo mode."
            )
            return

        if genai is None:
            self.config_error = (
                "google-generativeai is not installed. Run pip install -r requirements.txt."
            )
            return

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as exc:  # pragma: no cover - defensive
            self.config_error = str(exc)

    def _fallback_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        clauses = [part.strip() for part in terms.split(";") if part.strip()]
        if not clauses:
            clauses = [terms.strip()]

        sections = [
            f"{document_type.title()} Draft",
            "",
            "This draft was generated in local demo mode because no Gemini API key was configured.",
            "",
            f"Effective Date: {effective_date}",
            "",
            "Parties:",
            parties,
            "",
            "Clauses:",
        ]

        for i, clause in enumerate(clauses, start=1):
            sections.append(f"{i}. {clause}")

        sections.extend([
            "",
            "Signature Blocks:",
            "Party 1: ______________________________",
            "Party 2: ______________________________",
            "",
            "This is a draft for review and should be checked by a qualified legal professional before use.",
        ])

        return "\n".join(sections).strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        if self.model is not None:
            prompt = f'''
You are the document-generation component of LegalEase.

Create a clear, professional LEGAL DOCUMENT DRAFT.

Document type:
{document_type}

Parties:
{parties}

Effective date:
{effective_date}

Terms and conditions:
{terms}

Instructions:
1. Use only the information supplied above. Do not invent names, addresses,
   money amounts, dates, laws, courts, registration numbers or other facts.
2. If important information is missing, use [TO BE COMPLETED] rather than
   inventing it.
3. Use a professional structure with a title, parties, effective date,
   numbered clauses, signatures and a short notice that this is a draft.
4. Preserve the supplied terms while improving organization and wording.
5. Do not claim that the document has been reviewed or approved by a lawyer.
6. Produce plain text suitable for editing and later export to DOCX/PDF.
'''

            response = self.model.generate_content(prompt)
            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text.strip()

        return self._fallback_document(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
        )
