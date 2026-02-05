from pdfminer.high_level import extract_text


def extract_text_from_pdf(path: str) -> str:
    try:
        return extract_text(path)
    except Exception:
        return ''
