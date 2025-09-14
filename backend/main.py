# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from parse_utils import extract_text_from_upload, split_sections
from skills import extract_skills_from_text, extract_required_skills_from_jd, COMMON_SKILLS
from semantic import semantic_similarity
from scoring import compute_overall_score
import re

app = FastAPI(title="Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def compute_achievement_score(text):
    # heuristics: count bullets or sentences that contain numbers (years, %, digits)
    lines = [l.strip() for l in re.split(r"[\r\n]+", text) if l.strip()]
    if not lines:
        return 0.0
    numeric_lines = [l for l in lines if re.search(r"\d", l)]
    return min(1.0, len(numeric_lines) / max(1, len(lines)))

def compute_format_score(sections):
    expected = ["experience", "education", "skills", "projects"]
    found = sum(1 for s in expected if s in sections and sections[s].strip())
    return found / len(expected)

def generate_suggestions(resume_skills, jd_skills, resume_text, experience_text, achievements_pct, format_score):
    suggestions = []
    
    # Missing skills
    missing_skills = [s for s in jd_skills if s.lower() not in (x.lower() for x in resume_skills)]
    if missing_skills:
        suggestions.append(f"Add or highlight these skills for the JD: {', '.join(missing_skills)}.")
    
    # Achievements
    if achievements_pct < 0.5:
        suggestions.append("Add measurable achievements (numbers/metrics). Example: 'Reduced latency by 30%'.")
    
    # Format
    if format_score < 0.75:
        suggestions.append("Improve structure: add clear headings (Experience, Education, Skills, Projects). Avoid images/tables for ATS.")
    
    # Experience relevance
    if jd_skills and experience_text:
        missing_keywords = [kw for kw in jd_skills if kw.lower() not in experience_text.lower()]
        if missing_keywords:
            suggestions.append(f"Include relevant keywords from JD in experience section: {', '.join(missing_keywords)}")
    
    if not suggestions:
        suggestions.append("Good job! Your resume looks strong. Consider minor tweaks to exceed 90% overall.")
    
    return suggestions, missing_skills

@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), job_desc: str = Form("")):
    # Extract text
    text = extract_text_from_upload(resume)
    sections = split_sections(text)

    # Skills detection
    resume_skills = extract_skills_from_text(text)
    jd_skills = extract_required_skills_from_jd(job_desc)

    # Skills % relative to JD
    if jd_skills:
        matched = [s for s in jd_skills if s.lower() in (x.lower() for x in resume_skills)]
        skills_pct = len(matched) / len(jd_skills)
        missing_skills = [s for s in jd_skills if s.lower() not in (x.lower() for x in resume_skills)]
    else:
        skills_pct = min(1.0, len(resume_skills) / max(1, len(COMMON_SKILLS)))
        matched = resume_skills
        missing_skills = []

    # Experience relevance
    exp_text = sections.get("experience") or sections.get("work") or text
    exp_relevance = semantic_similarity(exp_text, job_desc) if job_desc else 0.5

    # Achievements
    achievements_pct = compute_achievement_score(text)

    # Format
    format_score = compute_format_score(sections)

    # Overall score
    overall = compute_overall_score(skills_pct, exp_relevance, achievements_pct, format_score)

    # Generate resume-specific suggestions
    suggestions, missing_skills = generate_suggestions(
        resume_skills=resume_skills,
        jd_skills=jd_skills,
        resume_text=text,
        experience_text=exp_text,
        achievements_pct=achievements_pct,
        format_score=format_score
    )

    # Human-friendly guidance
    guidance = {
        "skills": "Aim for 80%+ on Skills Match for strong fit; below 50% needs major skill tailoring.",
        "experience": "Experience relevance: >0.7 is good, 0.5-0.7 moderate, <0.5 needs tailoring.",
        "achievements": "Prefer 50%+ of bullets to include measurable metrics.",
        "format": "Resume format: 0.75+ is preferred for ATS friendly."
    }

    return {
        "score": overall,
        "details": {
            "skills_match_pct": round(skills_pct * 100, 1),
            "experience_relevance_pct": round(exp_relevance * 100, 1),
            "achievements_pct": round(achievements_pct * 100, 1),
            "format_score_pct": round(format_score * 100, 1)
        },
        "interpretation": {
            "skills_label": ("Good" if skills_pct >= 0.8 else "Needs Improvement" if skills_pct >= 0.5 else "Poor"),
            "experience_label": ("Good" if exp_relevance >= 0.7 else "Moderate" if exp_relevance >= 0.5 else "Low"),
            "achievements_label": ("Strong" if achievements_pct >= 0.5 else "Weak"),
            "format_label": ("ATS-friendly" if format_score >= 0.75 else "Improve formatting")
        },
        "suggestions": suggestions,
        "skills_detected": resume_skills,
        "skills_missing": missing_skills,
        "skills_in_jd": jd_skills
    }
