import pdfplumber

def extract_text_from_pdf(path) :
    full_text = ""

    with pdfplumber.open(path) as pdf :
        for page in pdf.pages :
            full_text += page.extract_text() or ""
    return full_text

def chunk_text(text, chunk_size=3000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]