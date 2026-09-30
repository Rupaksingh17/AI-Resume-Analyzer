skills_dict = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql"],
    "excel": ["excel", "ms excel"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript", "js"],
    "react": ["react"],
    "nlp": ["nlp", "natural language processing"],
    "deep learning": ["deep learning"]
}


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for main_skill, variations in skills_dict.items():
        for keyword in variations:
            if keyword in text:
                found_skills.append(main_skill)
                break

    return list(set(found_skills))


def calculate_ats_score(found_skills, job_skills):
    found_skills = set([s.lower() for s in found_skills])
    job_skills = set([s.lower() for s in job_skills])

    if len(job_skills) == 0:
        return 0, []

    matched = found_skills.intersection(job_skills)

    score = int((len(matched) / len(job_skills)) * 100)
    missing = list(job_skills - found_skills)

    return score, missing

def predict_role(skills):
    roles = {
        "Data Analyst": ["python", "sql", "excel", "data analysis"],
        "Web Developer": ["html", "css", "javascript", "react"],
        "ML Engineer": ["python", "machine learning", "deep learning", "nlp"]
    }

    scores = {}
    skill_set = set(skills)

    for role, req_skills in roles.items():
        req_set = set(req_skills)
        match = len(skill_set.intersection(req_set))
        total = len(req_set)
        score = match / total
        scores[role] = round(score * 100, 2)

    best_role = max(scores, key=scores.get)

    if scores[best_role] == 0:
        best_role = "No clear match found"

    return best_role, scores


def generate_feedback(text, skills, missing_skills):
    feedback = []
    text_lower = text.lower()

    if missing_skills:
        feedback.append("Add missing skills: " + ", ".join(missing_skills))

    word_count = len(text.split())
    if word_count < 200:
        feedback.append("Your resume is too short. Add more details.")

    if text.islower():
        feedback.append("Resume is in all small letters. Use proper capitalization.")
    elif text.isupper():
        feedback.append("Resume is in all capital letters. Avoid full caps.")

    sections = ["education", "experience", "skills", "projects"]
    for sec in sections:
        if sec not in text_lower:
            feedback.append(f"Missing section: {sec.title()}")

    if "-" not in text and "•" not in text:
        feedback.append("Use bullet points for better readability.")

    if "@" not in text:
        feedback.append("Email not found. Add contact details.")

    action_words = ["developed", "built", "created", "analyzed"]
    if not any(word in text_lower for word in action_words):
        feedback.append("Use action verbs like Developed, Built, Analyzed.")

    if len(skills) < 3:
        feedback.append("Add more relevant keywords to improve ATS score.")

    if not feedback:
        feedback.append("Great resume! No major issues found.")

    return feedback