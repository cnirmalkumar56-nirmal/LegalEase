import os
import requests
import streamlit as st
from dotenv import load_dotenv

from document_utils.formatters import (
    format_docx,
    format_pdf,
    format_html_preview,
)

load_dotenv()

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("⚖️ LegalEase")
st.caption("AI-Powered Legal Document Generator")

with st.sidebar:
    st.header("About LegalEase")
    st.write(
        "Generate structured legal-document drafts from your document type, "
        "parties, terms and effective date."
    )
    st.warning(
        "Educational/general informational tool. Generated content should be "
        "reviewed by a qualified legal professional when appropriate."
    )

st.subheader("1. Document Information")

document_type = st.selectbox(
    "Document Type",
    [
        "Agreement",
        "Contract",
        "Non-Disclosure Agreement (NDA)",
        "Lease Agreement",
        "Employment Offer Letter",
        "Freelance Work Contract",
        "Custom Legal Document",
    ],
)

if document_type == "Custom Legal Document":
    document_type = st.text_input("Enter document type")

parties = st.text_area(
    "Parties Involved",
    placeholder="Example: Jane Doe (Service Provider), TechNova Inc. (Client)",
    height=100,
)

terms = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Enter each clause separated by a semicolon; "
        "Payment within 30 days; Confidentiality must be maintained; "
        "Either party may terminate with 15 days notice"
    ),
    height=160,
)

effective_date = st.text_input(
    "Effective Date",
    placeholder="Example: 22/09/2026",
)

uploaded_logo = st.file_uploader(
    "Optional Logo for DOCX/PDF",
    type=["png", "jpg", "jpeg"],
)

if uploaded_logo:
    os.makedirs("assets", exist_ok=True)
    logo_path = os.path.join("assets", "uploaded_logo.png")
    with open(logo_path, "wb") as f:
        f.write(uploaded_logo.getbuffer())
else:
    logo_path = None

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

if st.button("Generate Document", type="primary", use_container_width=True):
    if not all([document_type, parties, terms, effective_date]):
        st.error("Please complete all required fields.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
        }

        try:
            with st.spinner("Generating your document..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )
            if response.ok:
                data = response.json()
                st.session_state.generated_text = data["content"]
                st.success("Document generated successfully.")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(f"Backend error: {detail}")
        except requests.RequestException as exc:
            st.error(
                "Could not connect to FastAPI. Make sure the backend is running "
                f"at {BACKEND_URL}. Error: {exc}"
            )

if st.session_state.generated_text:
    st.divider()
    st.subheader("2. Document Preview & Editing")

    edited = st.text_area(
        "Edit Document",
        value=st.session_state.generated_text,
        height=500,
    )
    st.session_state.generated_text = edited

    st.markdown("### Preview")
    st.markdown(
        format_html_preview(st.session_state.generated_text),
        unsafe_allow_html=True,
    )

    st.markdown("### 3. Download")
    col1, col2, col3 = st.columns(3)

    clean_type = "".join(
        c if c.isalnum() else "_" for c in document_type.lower()
    ).strip("_")

    with col1:
        st.download_button(
            "Download TXT",
            data=st.session_state.generated_text,
            file_name=f"{clean_type}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        docx_data = format_docx(
            st.session_state.generated_text,
            document_type,
            logo_path,
        )
        st.download_button(
            "Download DOCX",
            data=docx_data,
            file_name=f"{clean_type}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

    with col3:
        pdf_data = format_pdf(
            st.session_state.generated_text,
            document_type,
            logo_path,
        )
        st.download_button(
            "Download PDF",
            data=pdf_data,
            file_name=f"{clean_type}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
