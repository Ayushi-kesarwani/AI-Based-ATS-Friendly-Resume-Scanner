# AI-Based ATS Friendly Resume Scanner 🚀

An **AI-powered Applicant Tracking System (ATS) Resume Scanner** that evaluates a candidate’s resume against a job description and provides an **ATS compatibility score**, **matched skills**, and **missing skills** using **NLP and Machine Learning**.

This project simulates how real-world ATS software screens resumes before human review.

---

## 🔍 Features

- Upload resume in PDF or DOCX format  
- Paste any Job Description
- Extract resume text automatically
- Calculate ATS Match Score (0–100%)
- Identify Matched Skills and Missing Skills
- NLP-based text preprocessing using spaCy
- Machine Learning-based similarity using TF-IDF & Cosine Similarity
- Simple and interactive Streamlit UI

---

## 🧠 How It Works

1. User uploads a resume
2. User pastes a job description
3. System extracts resume text
4. NLP preprocessing is applied
5. Skills are extracted using a predefined skill set
6. Resume and job description are converted into vectors using TF-IDF
7. Cosine similarity is used to calculate ATS score
8. Results are displayed to the user

---

## 🏗️ Tech Stack

- Programming Language: Python  
- Frontend: Streamlit  
- NLP: spaCy  
- Machine Learning: TF-IDF, Cosine Similarity  
- Libraries: PyPDF2, python-docx, scikit-learn  

---



