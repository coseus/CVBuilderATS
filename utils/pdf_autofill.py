import re
from typing import Dict, List, Tuple, Optional

import pdfplumber


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def _find_first(pattern: str, text: str, flags=re.IGNORECASE) -> Optional[str]:
    m = re.search(pattern, text, flags)
    return _clean(m.group(1)) if m else None


def _extract_blocks(text: str) -> Dict[str, str]:
    """
    Works well for the eJobs CV layout visible in your PDFs:
    - Contact details / Date contact
    - About me / Despre mine
    - Work experience blocks with date ranges
    - Education line
    - Skills, General skills, Foreign languages
    - Driving license
    """
    blocks = {}

    # Contact
    email = _find_first(r"Email:\s*([^\s]+)", text)
    tel = _find_first(r"(?:Tel|Telefon):\s*([+\d][\d\s]+)", text)
    city = _find_first(r"(?:City|Oraș):\s*([^\n]+)", text)
    name = _find_first(r"\n([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\n", "\n" + text + "\n")  # weak heuristic

    blocks["email"] = email or ""
    blocks["telefon"] = tel or ""
    blocks["oras"] = city or ""
    blocks["nume"] = name or ""

    # About me / Despre mine
    about = None
    for pat in [
        r"About me\s*(.+?)\s*Professional experience",
        r"Despre mine\s*(.+?)\s*Experiență profesională",
    ]:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            about = _clean(m.group(1))
            break
    blocks["about"] = about or ""

    # Education (single line in your PDFs)
    edu = None
    for pat in [
        r"(\d{4}\s*-\s*\d{4}\s+Bachelor's degree\s*-\s*.+?)\s*Education",
        r"(\d{4}\s*-\s*\d{4}\s+Facultate\s*-\s*.+?)\s*Educație",
        r"(\d{4}\s*-\s*\d{4}\s+Bachelor's degree\s*-\s*[^\n]+)",
        r"(\d{4}\s*-\s*\d{4}\s+Facultate\s*-\s*[^\n]+)",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            edu = _clean(m.group(1))
            break
    blocks["education_line"] = edu or ""

    # Foreign languages
    langs = []
    # EN: "Foreign languages\nEnglish: Intermediate\nItalian: Intermediate"
    # RO: "Limbi străine\nEngleză: Mediu\nItaliană: Mediu"
    lang_section = None
    for pat in [
        r"Foreign languages\s*(.+?)\s*(?:Other sections|www\.ejobs\.ro|$)",
        r"Limbi străine\s*(.+?)\s*(?:Alte informații|www\.ejobs\.ro|$)",
    ]:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            lang_section = m.group(1)
            break
    if lang_section:
        for line in lang_section.splitlines():
            line = _clean(line)
            if ":" in line:
                a, b = line.split(":", 1)
                a, b = _clean(a), _clean(b)
                if a and b and len(a) <= 30:
                    langs.append((a, b))
    blocks["languages"] = langs

    # Driving license
    # EN: "Driving license Category A ... Category B ... Category C"
    # RO: "Permis de conducere Categoria A ... Categoria B ... Categoria C"
    dl = []
    for pat in [
        r"Driving license\s*(.+?)(?:www\.ejobs\.ro|$)",
        r"Permis de conducere\s*(.+?)(?:www\.ejobs\.ro|$)",
    ]:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            seg = m.group(1)
            # categories like A/B/C
            for c in re.findall(r"\bCategory\s*([A-Z])\b|\bCategoria\s*([A-Z])\b", seg, re.IGNORECASE):
                cat = (c[0] or c[1] or "").upper()
                if cat and cat not in dl:
                    dl.append(cat)
            break
    blocks["driving"] = dl

    return blocks


def _extract_experience_items(text: str) -> List[Dict]:
    """
    Extracts experience entries based on patterns found in your PDFs.
    Example:
      Apr 2023 - present
      System Administrator - E-Infra SA
      ...
    """
    items = []

    # Normalize dash variants
    t = text.replace("–", "-").replace("—", "-")

    # Matches date range headers (EN/RO):
    # "Apr 2023 - present" / "Apr 2023 - prezent"
    # plus the next line: "Role - Company"
    rx = re.compile(
        r"(?P<range>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Ian|Feb|Mar|Apr|Mai|Iun|Iul|Aug|Sep|Oct|Noi|Dec)\s+\d{4}\s*-\s*(?:present|prezent|[A-Za-z]{3}\s+\d{4}))\s+.*?\n(?P<title>[^\n]+?)\n",
        re.IGNORECASE,
    )

    for m in rx.finditer(t):
        rng = _clean(m.group("range"))
        title_line = _clean(m.group("title"))

        # title_line often: "System Administrator - E-Infra SA"
        role, company = title_line, ""
        if " - " in title_line:
            role, company = title_line.split(" - ", 1)
            role, company = _clean(role), _clean(company)

        # Take a snippet after this match as description until next date header or footer
        start = m.end()
        end = t.find("\nwww.ejobs.ro", start)
        if end == -1:
            end = len(t)
        # stop at next match start
        nxt = rx.search(t, start)
        if nxt:
            end = min(end, nxt.start())
        desc = _clean(t[start:end])

        # Keep bullets from "Implement..." etc; remove “Acquired skills…” blocks
        desc = re.sub(r"Acquired skills and competencies:.*", "", desc, flags=re.IGNORECASE | re.DOTALL)
        desc = re.sub(r"Abilități și competențe dobândite:.*", "", desc, flags=re.IGNORECASE | re.DOTALL)

        # Build activities bullets (split by sentences / hyphen lines)
        bullets = []
        for line in desc.splitlines():
            line = _clean(line)
            if not line:
                continue
            if line.startswith("-"):
                bullets.append(_clean(line.lstrip("-")))
        if not bullets:
            # fallback: split sentences (limited)
            parts = re.split(r"\.\s+", desc)
            bullets = [p.strip().rstrip(".") for p in parts if len(p.strip()) > 25][:6]

        items.append({
            "titlu": company or role,
            "perioada": rng,
            "functie": role,
            "angajator": company,
            "locatie": "",  # can be enriched later
            "activitati": "\n".join([f"- {b}" for b in bullets if b]),
            "sector": "",
            "tehnologii": "",
            "link": "",
        })

    return items


def pdf_to_cv(pdf_path: str, lang_hint: str = "en") -> Dict:
    """
    Reads a PDF and returns a partial CV dict compatible with your app schema.
    """
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            pages_text.append(p.extract_text() or "")
    text = "\n".join(pages_text)

    blocks = _extract_blocks(text)
    exp = _extract_experience_items(text)

    # Summary bullets (from About me / Despre mine)
    summary = blocks.get("about", "")
    summary_bullets = []
    if summary:
        # split into 2-4 bullets
        parts = re.split(r"\.\s+", summary)
        for p in parts:
            p = _clean(p).rstrip(".")
            if len(p) >= 25:
                summary_bullets.append(p)
        summary_bullets = summary_bullets[:5]

    # Education parsing
    educatie = []
    edu_line = blocks.get("education_line", "")
    if edu_line:
        # EN: "2002 - 2005 Bachelor's degree - Universitatea de Nord IT Engineer | Baia Mare"
        # RO: "2002 - 2005 Facultate - Universitatea de Nord Inginer informatica Tehnica | Baia Mare"
        m = re.match(r"(\d{4}\s*-\s*\d{4})\s+(.*)", edu_line)
        perio = _clean(m.group(1)) if m else ""
        rest = _clean(m.group(2)) if m else _clean(edu_line)

        # try split institution after " - "
        titlu = rest
        org = ""
        if " - " in rest:
            left, right = rest.split(" - ", 1)
            titlu = _clean(left)
            org = _clean(right)

        educatie.append({
            "perioada": perio,
            "titlu": titlu,
            "organizatie": org,
            "locatie": "",
            "descriere": "",
        })

    # Languages
    limbi = []
    for name, level in blocks.get("languages", []):
        limbi.append({
            "limba": name,
            "nivel": level,
            "ascultare": level,
            "citire": level,
            "interactiune": level,
            "exprimare": level,
            "scriere": level,
        })

    driving = blocks.get("driving", [])

    # Build CV dict (partial)
    cv = {
        "nume_prenume": blocks.get("nume", ""),
        "email": blocks.get("email", ""),
        "telefon": blocks.get("telefon", ""),
        "adresa": blocks.get("oras", ""),
        "rezumat_bullets": summary_bullets,
        "experienta": exp,
        "educatie": educatie,
        "limbi_straine": limbi,
        "permis_conducere": ", ".join(driving),
        "personal_info_extra": [],
        "modern_skills_headline": "",
        "modern_tools": "",
        "modern_certs": "",
        "modern_keywords_extra": "",
        "ats_profile": "cyber_security",
    }
    return cv
