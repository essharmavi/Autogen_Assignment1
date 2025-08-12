import fitz
import docx


def parse_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF file and return resume as a string."""
    try:
        pdf_bytes = uploaded_file.getvalue()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def parse_docx(uploaded_file) -> str:
    """Extract text from an uploaded docx/doc file and return resume as a string."""
    try:
        document = docx.Document(uploaded_file)
        text = []
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX file: {str(e)}"


def parse_textfile(uploaded_file) -> str:
    """Extract text from an uploaded text file and return resume as a string."""
    try:
        text = "\n".join(line.decode("utf-8") for line in uploaded_file)
        return text.strip()
    except Exception as e:
        return f"Error reading text file: {str(e)}"
