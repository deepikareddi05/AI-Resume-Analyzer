# scoring.py

def compute_overall_score(skills_pct, exp_relevance, achievements_pct, format_score):
    # weights - you can tune these. Explainable.
    weights = {
        "skills": 0.40,
        "experience": 0.30,
        "achievements": 0.15,
        "format": 0.15
    }
    total = (
        skills_pct * weights["skills"] +
        exp_relevance * weights["experience"] +
        achievements_pct * weights["achievements"] +
        format_score * weights["format"]
    )
    # return 0..100
    return round(total * 100, 1)
