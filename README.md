# AI Resume Analyzer

![Resume Analyzer](https://img.shields.io/badge/status-Complete-green) ![Python](https://img.shields.io/badge/python-3.13-blue) ![React](https://img.shields.io/badge/react-18-blue) ![FastAPI](https://img.shields.io/badge/fastapi-0.111-green)

---

## Overview

**AI Resume Analyzer** is a web-based application that evaluates resumes against a job description (JD) using AI and NLP techniques.  
It provides a **score, skill match analysis, experience relevance, achievements, and format suggestions** to help candidates improve their resumes.  

The tool is **interactive, user-friendly, and designed for modern, professional UI/UX**. It can be used for **preparing for job applications** or as a **portfolio project** for developers interested in AI + web development.

---

## Features

- Upload resumes in **PDF or DOCX format**.
- Optional: Paste a **Job Description (JD)** for tailored analysis.
- **Overall Resume Score**: Aggregated score based on skills, experience, achievements, and format.
- **Detailed Metrics**:
  - Skills Match (%)
  - Experience Relevance (%)
  - Achievements (% of measurable achievements)
  - Resume Format Quality (%)
- **Suggestions** to improve resume, tailored based on missing skills or low metrics.
- **Detected Skills** vs **Skills required in JD**
- Detect if the uploaded file is **not a valid resume**.
- **Polished, responsive UI** with hover effects, progress bars, and modern design.

---

## Tech Stack

- **Frontend**: React.js, CSS (modern design with gradients, cards, responsive layout)
- **Backend**: FastAPI, Python
- **AI & NLP**:
  - `transformers` for semantic similarity
  - Custom heuristic scoring for achievements, format, and experience
- **File Parsing**: `pdfplumber`, `python-docx`
- **Others**: CORS middleware for cross-origin requests

---

## Folder Structure
resume-analyzer/
│
├── backend/ # FastAPI backend
│ ├── main.py # API entry point
│ ├── parse_utils.py # Resume parsing utilities
│ ├── skills.py # Skill extraction logic
│ ├── semantic.py # Semantic similarity functions
│ ├── scoring.py # Score computation
│ └── venv/ # Python virtual environment
│
├── frontend/ # React frontend
│ ├── public/
│ ├── src/
│ │ ├── components/ # React components
│ │ │ └── Analyzer.jsx
│ │ ├── index.css # Styling
│ │ ├── App.jsx
│ │ └── main.jsx
│ ├── package.json
│ └── vite.config.js
│
└── README.md # Project documentation


---

## ⚙️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** React, HTML, CSS (modern, responsive)
- **AI/ML:** HuggingFace Transformers, spaCy, NLP
- **Other:** Semantic similarity, skill extraction, PDF/DOCX parsing

---

## 🚀 Setup & Installation

### Backend

1. Navigate to the backend folder:
   ```bash
   cd backend


Create a virtual environment:

python -m venv venv


Activate the virtual environment:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Start the backend server:

uvicorn main:app --reload

Frontend

Navigate to the frontend folder:

cd frontend


Install dependencies:

npm install


Start the frontend server:

npm run dev


Open the app in your browser (default: http://localhost:5173)

📝 Usage

Open the web app.

Upload your resume file.

Paste the job description (optional but recommended).

Click Analyze.

Review the scores, detected skills, missing skills, and personalized suggestions.

📌 Notes

Supports PDF and DOCX resume formats.

Suggestions are tailored to the uploaded resume and JD.

If the file is invalid (not a resume), the system will alert the user.

🎯 Goal

This project is designed to help candidates improve their resumes based on AI analysis and make them stand out in interviews.
