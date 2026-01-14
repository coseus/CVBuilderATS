# Streamlit CV Builder (Modern ATS + Europass)

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-red)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

Two-tab CV builder built with **Streamlit**:
- **Modern (ATS-friendly)**: short, single-column layout, keyword-dense, recruiter-friendly.
- **Europass**: full Europass-style form with all fields.

## Features
### Modern (ATS-friendly)
- One-column structure (better for ATS parsing)
- **Professional Summary** with bullet support
- **Skills (ATS-friendly)**: headline + tools + certifications + extra keywords
- **Projects / Experience** with:
  - period, role/title, bullets (impact), tools/tech, optional link
  - reorder (move up/down) + delete
- **ATS Optimizer**:
  - paste a Job Description
  - see matched vs missing keywords
  - one-click add missing keywords into “Extra keywords”
- **ATS Profiles (editable YAML)**:
  - select profile (Cyber Security / System Admin / Network Admin)
  - preview + edit + save-as from the UI
- **ATS Score Dashboard**:
  - profile keyword coverage, JD match, metrics coverage, verb variety, completeness
- **Auto-rewrite bullets** (deterministic):
  - suggests better verbs + adds metric prompts
  - can insert bullet templates from the selected profile
- Exports:
  - **PDF Modern**
  - **Word Modern**
  - **ATS plain-text (.txt)**

> Tip: Photo is **off by default** for Modern export (recommended for ATS).

### Europass
- Personal info, photo, experience, education, languages, competences
- Exports:
  - **PDF Europass**
  - **Word Europass**

---

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## ATS Profiles
Profiles live in `./ats_profiles/*.yaml` and are user-editable.

Default profiles included:
- `cyber_security`
- `system_administrator`
- `network_administrator`

## Data model (in session)
All data is stored in `st.session_state.cv` as a dictionary.

Experience/Projects items (`cv['experienta']`) look like:
```json
{
  "perioada": "2024–2025",
  "functie": "Pentest Report Automation",
  "activitati": "Built ...\nReduced time ...",
  "angajator": "Freelance",
  "sector": "",
  "tehnologii": "Python, ReportLab, Streamlit",
  "link": "https://github.com/..."
}
```

---

## ATS tips (quick checklist)
- Use **standard headings**: Summary, Skills, Experience, Education
- Avoid tables/columns/icons in the Modern version
- Put important keywords in:
  - Summary
  - Skills tools list
  - Project bullets (impact)
- Add metrics where possible (time saved, users, %, volume, etc.)

---

## Project structure
```
.
├─ app.py
├─ ats_profiles/
│  ├─ cyber_security.yaml
│  ├─ system_administrator.yaml
│  └─ network_administrator.yaml
├─ components/
│  ├─ ats_optimizer.py
│  ├─ ats_dashboard.py
│  ├─ ats_rewrite.py
│  ├─ profile_manager.py
│  ├─ modern_skills.py
│  ├─ personal_info.py
│  ├─ photo_upload.py
│  ├─ work_experience.py
│  ├─ education.py
│  ├─ languages.py
│  └─ skills.py
├─ exporters/
│  ├─ pdf_generator.py
│  └─ docx_generator.py
└─ utils/
   ├─ session.py
   ├─ profiles.py
   └─ ats_scoring.py
```

## Contributing / License
- See `CONTRIBUTING.md`
- MIT License (`LICENSE`)
