import pdfplumber

def extract_text_from_pdf(path) :
    full_text = ""

    with pdfplumber.open(path) as pdf :
        for page in pdf.pages :
            full_text += page.extract_text() or ""
    return full_text