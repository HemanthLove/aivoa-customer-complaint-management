from io import BytesIO

from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_file = BytesIO(file_bytes)
    reader = PdfReader(pdf_file)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    extracted_text = "\n\n".join(pages).strip()

    if not extracted_text:
        raise ValueError(
            "No readable text was found in the PDF."
        )

    return extracted_text