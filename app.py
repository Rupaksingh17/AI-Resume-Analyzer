from flask import Flask, render_template, request, send_file
from parser import extract_text
from analyzer import extract_skills, calculate_ats_score, generate_feedback, predict_role
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

latest_result = {}

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    global latest_result

    file = request.files.get('resume')
    role = request.form.get('role')

    if not file:
        return render_template("index.html", error="Please upload a resume")

    text = extract_text(file)
    skills = extract_skills(text)

    if role == "data":
        job_skills = ["python", "sql", "excel", "data analysis"]
    elif role == "web":
        job_skills = ["html", "css", "javascript", "react"]
    elif role == "ml":
        job_skills = ["python", "machine learning", "deep learning", "nlp"]
    else:
        job_skills = []

    score, missing = calculate_ats_score(skills, job_skills)
    feedback = generate_feedback(text, skills, missing)

    predicted_role, role_scores = predict_role(skills)

    latest_result = {
        "skills": skills,
        "ats_score": score,
        "missing_skills": missing,
        "feedback": feedback,
        "predicted_role": predicted_role,
        "role_scores": role_scores
    }

    return render_template("index.html", result=latest_result)


@app.route('/download')
def download():
    global latest_result

    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Resume Analysis Report", styles['Title']))
    content.append(Paragraph(f"ATS Score: {latest_result.get('ats_score', 0)}%", styles['Normal']))
    content.append(Paragraph(f"Suggested Role: {latest_result.get('predicted_role', '')}", styles['Normal']))

    content.append(Paragraph("Skills Found:", styles['Heading2']))
    for skill in latest_result.get('skills', []):
        content.append(Paragraph(f"- {skill}", styles['Normal']))

    content.append(Paragraph("Missing Skills:", styles['Heading2']))
    for skill in latest_result.get('missing_skills', []):
        content.append(Paragraph(f"- {skill}", styles['Normal']))

    content.append(Paragraph("Suggestions:", styles['Heading2']))
    for f in latest_result.get('feedback', []):
        content.append(Paragraph(f"- {f}", styles['Normal']))

    doc.build(content)

    return send_file("report.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)