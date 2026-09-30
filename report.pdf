import pdfplumber
import io

def extract_text(file):
    text = ""

    pdf = pdfplumber.open(io.BytesIO(file.read()))

    for page in pdf.pages:
        content = page.extract_text()
        if content:
            text += content

    return text