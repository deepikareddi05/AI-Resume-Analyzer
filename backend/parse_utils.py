# parse_utils.py
import tempfile
from pathlib import Path
from pdfminer.high_level import extract_text
import docx2txt
import re

def extract_text_from_upload(uploaded_file):
    suffix = Path(uploaded_file.filename).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.file.read())
        tmp.flush()
        tmp_path = tmp.name

    if suffix == ".pdf":
        text = extract_text(tmp_path)
    elif suffix == ".docx":
        text = docx2txt.process(tmp_path)
    else:
        with open(tmp_path, "r", errors="ignore") as f:
            text = f.read()
    # normalize whitespace
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text

def split_sections(text):
    """
    Simple heuristic based section splitter. Returns dict of lowercased section name -> text.
    """
    headings = [
        "summary", "objective", "profile", "experience", "work experience", "professional experience",
        "projects", "education", "skills", "technical skills", "certifications", "achievements"
    ]
    # find headings positions
    pattern = r"(?im)^(?:{0})\s*:?\s*$".format("|".join(re.escape(h) for h in headings))
    matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
    if not matches:
        return {"full": text}

    sections = {}
    for i, m in enumerate(matches):
        header = m.group(0).strip().lower().strip(":").strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        # normalize header name
        header_norm = header.split()[0]
        sections[header_norm] = body
    # include leading text if present
    first_start = matches[0].start()
    if first_start > 0:
        sections.setdefault("top", text[:first_start].strip())
    return sections
