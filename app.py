# AI-Based ATS Friendly Resume Scanner
# Author: Ayushi Kesarwani (Student Project)
# Tech: Python, Streamlit, NLP (spaCy), ML (TF-IDF)

import streamlit as st
from PyPDF2 import PdfReader
import docx
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AI ATS Resume Scanner", page_icon="📄", layout="centered")

# -------------------- LOAD NLP MODEL --------------------
@st.cache_resource

def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

# -------------------- SKILL DATABASE --------------------
SKILLS = [
    "python", "java", "c", "c++", "sql", "mysql", "mongodb",
    "machine learning", "deep learning", "artificial intelligence",
    "nlp", "data science", "data analysis",
    "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "matplotlib",
    "git", "github", "docker", "aws", "azure",
    "html", "css", "javascript", "react", "node.js",
    "flask", "django"
]

# -------------------- FUNCTIONS --------------------

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + " "
    return text


def extract_text_from_docx(file):
    document = docx.Document(file)
    text = ""
    for para in document.paragraphs:
        text += para.text + " "
    return text


def clean_text(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)


def extract_skills(text):
    text = text.lower()
    found_skills = set()
    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)
    return found_skills


def calculate_ats_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(similarity * 100, 2)

# -------------------- UI --------------------
st.title("📄 AI-Based ATS Friendly Resume Scanner")
st.markdown("Analyze your resume against a job description using AI & NLP")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description", height=200)

# -------------------- PROCESS --------------------
if resume_file and job_description:

    # Extract resume text
    if resume_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(resume_file)
    else:
        resume_text = extract_text_from_docx(resume_file)

    if resume_text.strip() == "":
        st.error("❌ Unable to extract text. Please upload a text-based resume.")
        st.stop()

    # Clean text
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(job_description)

    # ATS Score
    ats_score = calculate_ats_score(clean_resume, clean_jd)

    # Skill Extraction
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills.difference(resume_skills)

    # -------------------- OUTPUT --------------------
    st.subheader("📊 ATS Match Score")
    st.progress(min(int(ats_score), 100))
    st.success(f"Your ATS Score: {ats_score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        if matched_skills:
            st.write(", ".join(sorted(matched_skills)))
        else:
            st.write("No matched skills found")

    with col2:
        st.subheader("❌ Missing Skills")
        if missing_skills:
            st.write(", ".join(sorted(missing_skills)))
        else:
            st.write("No missing skills 🎉")

    # Suggestions
    st.subheader("📝 Improvement Suggestions")
    if ats_score < 60:
        st.warning("Your resume needs major improvement. Add missing skills and align experience with JD.")
    elif ats_score < 80:
        st.info("Good resume, but adding missing skills can improve ATS ranking.")
    else:
        st.success("Excellent! Your resume is highly ATS-friendly.")

    # Debug / Learning view
    with st.expander("🔍 View Extracted Resume Text"):
        st.write(resume_text[:2000])

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("AI-Based ATS Resume Scanner | Student Learning Project")
