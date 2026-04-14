import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Career Intelligence Pro", layout="wide")

st.title("🚀 AI Career Intelligence PRO")
st.write("Next-Gen Career Analyzer with AI Insights")

# ---------------- DATA ----------------
roles_data = {
    "Data Analyst": ["python", "sql", "excel", "powerbi", "statistics"],
    "Data Scientist": ["python", "machine learning", "statistics", "pandas", "numpy"],
    "ML Engineer": ["python", "deep learning", "tensorflow", "pytorch", "mlops"],
    "AI Engineer": ["python", "nlp", "computer vision", "deep learning"],
    "Frontend Developer": ["html", "css", "javascript", "react"],
    "Backend Developer": ["python", "django", "flask", "api"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "node"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "linux"],
    "Cybersecurity Analyst": ["network", "security", "cryptography"],
    "Software Engineer": ["java", "c++", "dsa", "algorithms"]
}

salary_data = {
    "Data Analyst": "₹4–10 LPA",
    "Data Scientist": "₹8–25 LPA",
    "ML Engineer": "₹10–30 LPA",
    "AI Engineer": "₹12–35 LPA",
    "Frontend Developer": "₹3–12 LPA",
    "Backend Developer": "₹5–18 LPA",
    "Full Stack Developer": "₹6–20 LPA",
    "DevOps Engineer": "₹8–22 LPA",
    "Cybersecurity Analyst": "₹6–18 LPA",
    "Software Engineer": "₹5–20 LPA"
}

trend_data = {
    "Data Analyst": 70,
    "Data Scientist": 90,
    "ML Engineer": 95,
    "AI Engineer": 98,
    "Frontend Developer": 75,
    "Backend Developer": 80,
    "Full Stack Developer": 85,
    "DevOps Engineer": 88,
    "Cybersecurity Analyst": 92,
    "Software Engineer": 78
}

roadmaps = {
    "Data Scientist": ["Python Basics", "Statistics", "Machine Learning", "Projects"],
    "ML Engineer": ["Python", "ML", "Deep Learning", "MLOps"],
    "AI Engineer": ["Python", "NLP/CV", "Deep Learning", "Projects"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React"],
    "Backend Developer": ["Python", "Django/Flask", "APIs", "Database"],
}

df = pd.DataFrame([
    {"Role": role, "Skills": " ".join(skills)}
    for role, skills in roles_data.items()
])

all_skills = sorted(
    list(set(skill for skills in roles_data.values() for skill in skills)))

# ---------------- SIDEBAR ----------------
st.sidebar.header("🧠 Your Profile")

selected_skills = st.sidebar.multiselect("Select Skills", all_skills)
experience = st.sidebar.slider("Experience", 0, 10, 1)

target_role = st.sidebar.selectbox(
    "🎯 Target Role (Career Switch)", list(roles_data.keys()))

analyze = st.sidebar.button("🚀 Analyze")

# ---------------- MODEL ----------------
vectorizer = TfidfVectorizer()
skill_matrix = vectorizer.fit_transform(df["Skills"])

# ---------------- MAIN ----------------
if analyze:
    if not selected_skills:
        st.warning("Please select skills")
    else:
        user_input = " ".join(selected_skills)
        user_vec = vectorizer.transform([user_input])
        similarity = cosine_similarity(user_vec, skill_matrix)[0]

        df["Score"] = similarity
        top_roles = df.sort_values(by="Score", ascending=False).head(3)

        st.subheader("🎯 Top Matches")

        cols = st.columns(3)

        for i, (_, row) in enumerate(top_roles.iterrows()):
            role = row["Role"]
            score = int(row["Score"] * 100 + experience * 2)

            with cols[i]:
                st.metric(role, f"{score}%")
                st.info(f"💰 Salary: {salary_data[role]}")

        # ---------------- SKILL GAP ROADMAP ----------------
        st.subheader("🧠 Skill Roadmap")

        best_role = top_roles.iloc[0]["Role"]

        steps = roadmaps.get(
            best_role, ["Learn Basics", "Practice", "Build Projects"])

        for i, step in enumerate(steps):
            st.write(f"Step {i+1}: {step}")

        # ---------------- SKILL STRENGTH ----------------
        st.subheader("📊 Skill Strength")

        for skill in selected_skills:
            st.write(skill)
            st.progress(np.random.randint(40, 100))  # demo strength

        # ---------------- TREND ANALYSIS ----------------
        st.subheader("📈 Job Market Trends")

        trend_df = pd.DataFrame({
            "Role": list(trend_data.keys()),
            "Demand": list(trend_data.values())
        })

        st.bar_chart(trend_df.set_index("Role"))

        # ---------------- CAREER SWITCH ----------------
        st.subheader("🔄 Career Switch Simulator")

        needed_skills = set(roles_data[target_role]) - set(selected_skills)

        st.write(f"To switch to **{target_role}**, you need:")
        st.error(", ".join(needed_skills)
                 if needed_skills else "You are ready!")

        # ---------------- PDF REPORT ----------------
        st.subheader("📄 Download Report")

        def generate_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Career Report", ln=True)

            pdf.cell(200, 10, txt=f"Best Role: {best_role}", ln=True)
            pdf.cell(200, 10, txt=f"Salary: {salary_data[best_role]}", ln=True)

            pdf.cell(200, 10, txt="Skills:", ln=True)
            for skill in selected_skills:
                pdf.cell(200, 10, txt=skill, ln=True)

            file = "report.pdf"
            pdf.output(file)
            return file

        if st.button("Download PDF"):
            file = generate_pdf()
            with open(file, "rb") as f:
                st.download_button("Click to Download", f,
                                   file_name="career_report.pdf")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔥 AI Career Intelligence PRO | Unique ML Project")
