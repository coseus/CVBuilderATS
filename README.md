# CV Builder – Modern (ATS-Friendly) & Europass

🚀 **CV Builder** is a **desktop, offline-first CV generator** focused on **ATS (Applicant Tracking System) optimization**. Is a Streamlit-based web application that helps you **create, optimize, import, and export CVs** in two professional formats:

- **Modern (ATS-Friendly)** – optimized for Applicant Tracking Systems and recruiters
- **Europass (Complete)** – compliant with the official Europass structure

The app supports **PDF & DOCX autofill**, **offline ATS optimization**, **job-specific keyword matching**, and export to **PDF, Word, TXT, and JSON**.

---

## ✨ Key Features

- ✅ **ATS-friendly CV builder (Modern format)**
- ✅ **Europass full editor**
- ✅ **Offline Job Description Analyzer**
- ✅ **Keyword coverage & missing keyword detection**
- ✅ **Auto-apply keywords into CV**
- ✅ **Domain-based ATS profiles (IT & Non-IT)**
- ✅ **EN / RO bilingual support**
- ✅ **No cloud, no tracking, no login**
- ✅ **Standalone executables (no Python required)**
  
### 🧩 CV Editing

- Full CRUD support (Add / Edit / Delete) for:
    - Personal Information
    - Professional Summary (bullet-based, ATS-friendly)
    - Professional Experience / Projects
    - Education
    - Skills (structured for ATS)
    - Languages
    - Europass personal competencies
- **Short profile line under name**
    
    Example:
    
    `Senior System Administrator | Cloud & Security | 17+ years experience`
    

---

### 📄 CV Import (Autofill)

- Import CVs from:
    - **PDF** (eJobs, Europass, classic CV layouts)
    - **DOCX**
- Smart autofill engine:
    - fixes duplicated characters from PDFs
    - ignores platform footers (e.g. `www.ejobs.ro`)
    - safe merge (never overwrites manually filled fields)

---

## 🧠 ATS Intelligence

CVBuilder uses:

- **Core libraries** (common verbs, metrics, templates)
- **Domain libraries** (Cyber Security, System Admin, Accounting, HR, Marketing, etc.)
- **Profile YAMLs** that automatically merge:
    
    ```
    Core Library
      + Domain Library
        + Selected Profile
    
    ```
    
This ensures:

- Relevant keywords
- ATS-safe phrasing
- Consistent structure
---

### 📤 Export Options

- PDF – Modern
- PDF – Europass
- Word – Modern
- Word – Europass
- ATS `.txt` (plain text, copy-paste friendly)
- Import / Export full CV as **JSON**

---

### 🔄 Reset & Persistence

- **Reset Everything**
- **Reset ATS / Job Description only**
- Persistent ATS profile per job

---

## 🧩 Supported Domains (Examples)

### IT

- Cyber Security
- SOC Analyst
- System Administrator
- Network Administrator
- Cloud Security
- AppSec
- DFIR / Incident Response
- Data Analyst

### Non-IT

- Accounting / Finance
- Project Management
- HR / Recruiting
- Marketing / Growth
- Sales (B2B)
- Customer Support
- Operations / Supply Chain

All profiles support **English & Romanian**.

---

## 🗂️ Project Structure

```
cvbuilderats/
├── app.py
├── components/
│   ├── personal_info_shared.py
│   ├── work_experience.py
│   ├── education.py
│   ├── skills.py
│   ├── ats_optimizer.py
│   ├── ats_dashboard.py
│   └── profile_manager.py
├── exporters/
│   ├── pdf_generator.py
│   └── docx_generator.py
├── utils/
│   ├──session.py
│   ├── json_io.py
│   ├── profiles.py
│   └── pdf_autofill.py
├── ats_profiles/
├── requirements.txt
└── README.md

```
---

## 🔒 Privacy & Security

- ✔ Runs **100% locally**
- ✔ No data leaves your machine
- ✔ No telemetry
- ✔ No API calls
- ✔ Safe for confidential CVs

---

## ▶️ Run Locally

### 1️⃣ Clone the repository

```bash
gitclone https://github.com/your-username/cvbuilderats.git
cd cvbuilderats

```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt

```

### 3️⃣ Start the app

```bash
streamlit run app.py

```

---

## ☁️ Deploy on Streamlit Cloud

1. Push the repository to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Select the repo and `app.py`
4. Deploy 🚀

   ### Demo ###: https://cvbuilder-v2.streamlit.app/

✅ Fully compatible with Streamlit Cloud.

---

## 📥 JSON Import / Export

- Stable and forward-compatible schema
- Supports:
    - full CV export
    - optional photo (base64)
- Ideal for:
    - backups
    - versioning
    - migration between devices

---

## 🔐 Privacy & Security

- No external services or APIs
- ATS analysis is **100% offline**
- No data leaves the app
- Safe for real CVs and sensitive data

---

## 🧪 Known Limitations

- PDF parsing depends on text-layer quality
- Scanned PDFs (images) are not supported (no OCR yet)
- ATS scoring is heuristic (not ML-based)

---

## 🛣️ Roadmap

- [ ]  OCR support for scanned PDFs
- [ ]  Skill gap suggestions
- [ ]  Multiple CV variants per job
- [ ]  Cover Letter generator
- [ ]  LaTeX export
- [ ]  Desktop builds (Windows / Linux)

## Build commands
### Windows
``` bash
python -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m pip install -r requirements-build.txt
py -m PyInstaller .\cvbuilderats_windows.spec --noconfirm --clean
```
### Linux
``` bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-build.txt
python3 -m PyInstaller ./cvbuilderats_linux.spec --noconfirm --clean
chmod +x dist/cvbuilder
```

### The results are found in: 
``` bash
dist/cvbulder/
```

## 🖥 Desktop Executables

Download the latest **ready-to-run executables** here:

🔗 **Windows & Linux builds (Mega.nz)**

👉 [https://mega.nz/folder/zxYx3Dqa#X85rmbOzS_Oy_aUEdwUg4A](https://mega.nz/folder/zxYx3Dqa#X85rmbOzS_Oy_aUEdwUg4A)

### Available files

- **Windows**: `CVBuilder.exe`
- **Linux**: `CVBuilder` (AppImage / binary)

⚠️ No Python installation required.

---

## 🚀 How to Use

1. Download the executable for your OS
2. Run it (double-click)
3. Paste **Job Description once**
4. Select **ATS Profile** (IT / Non-IT)
5. Optimize CV automatically
6. Export as:
    - PDF (Modern / Europass)
    - DOCX
    - ATS-friendly `.txt`

---

## 📌 Notes

- Antivirus software may warn on unsigned executables (false positive).
- If blocked on Windows, click **“More info → Run anyway”**.
- Linux: `chmod +x CVBuilder` if needed.
