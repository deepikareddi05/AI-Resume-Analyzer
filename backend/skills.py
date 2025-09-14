# skills.py
import re

# A curated skills list. You can extend this file as needed.
COMMON_SKILLS = [
    "python","java","c++","c#","sql","javascript","react","node.js","nodejs","express","django",
    "flask","html","css","aws","azure","gcp","docker","kubernetes","tensorflow","pytorch",
    "machine learning","data science","nlp","git","rest","graphql","nosql","mongodb","postgresql",
    "mysql","linux","bash","azure devops","ci/cd"
]

def normalize_word(w):
    return re.sub(r"[^\w\.#\+-]", "", w.lower())

def extract_skills_from_text(text, skills_list=None):
    if skills_list is None:
        skills_list = COMMON_SKILLS
    found = set()
    text_low = text.lower()
    for s in skills_list:
        s_norm = s.lower()
        # match whole word or tokens
        if re.search(r"\b" + re.escape(s_norm) + r"\b", text_low):
            found.add(s)
    return sorted(found)

def extract_required_skills_from_jd(jd_text, skills_list=None):
    # same method: which skills in our list appear in the JD
    return extract_skills_from_text(jd_text, skills_list)
