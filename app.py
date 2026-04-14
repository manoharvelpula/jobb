import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Career Intelligence PRO", layout="wide")

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

# ---------------- ROADMAP DATA ----------------
roadmaps = {
    "Data Scientist": [
        {"step": "Learn Python Basics", "desc": "Syntax, loops, OOP",
         "resources": ["https://www.w3schools.com/python/", "https://www.youtube.com/watch?v=rfscVS0vtbw"]},
        {"step": "Statistics", "desc": "Probability, distributions",
         "resources": ["https://www.khanacademy.org/math/statistics-probability"]},
        {"step": "Machine Learning", "desc": "Supervised & unsupervised learning",
         "resources": ["https://www.coursera.org/learn/machine-learning"]},
        {"step": "Projects", "desc": "Build real-world ML apps",
         "resources": ["https://www.kaggle.com/learn"]}
    ],
    "ML Engineer": [
        {"step": "Python + ML", "desc": "Strong coding + ML basics",
         "resources": ["https://www.w3schools.com/python/"]},
        {"step": "Deep Learning", "desc": "CNN, RNN, Neural Networks",
         "resources": ["https://www.deeplearning.ai/"]},
        {"step": "MLOps", "desc": "Deployment, Docker",
         "resources": ["https://www.youtube.com/watch?v=06-AZXmwHjo"]},
        {"step": "Projects", "desc": "Deploy models",
         "resources": ["https://github.com"]}
    ],
    "Frontend Developer": [
        {"step": "HTML & CSS", "desc": "Structure & styling",
         "resources": ["https://www.freecodecamp.org/"]},
        {"step": "JavaScript", "desc": "Core JS",
         "resources": ["https://javascript.info/"]},
        {"step": "React", "desc": "Modern UI",
         "resources": ["https://react.dev/"]},
        {"step": "Projects", "desc": "Build websites",
         "resources": ["https://frontendmentor.io/"]}
    ]
}

learning_links = {
    "python": "https://www.w3schools.com/python/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "tensorflow": "https://www.tensorflow.org/tutorials",
    "react": "https://react.dev/learn",
    "sql": "https://www.w3schools.com/sql/",
    "docker": "https://www.docker.com/101-tutorial"
}

# ---------------- DATAFRAME ----------------
df = pd.DataFrame([
    {"Role": role, "Skills": " ".join(skills)}
    for role, skills in roles_data.items()
])

all_skills = sorted(list(set(skill for skills in roles_data.values() for skill in skills)))

# ---------------- SIDEBAR ----------------
st.sidebar.header("🧠 Your Profile")

selected_skills = st.sidebar.multiselect("Select Skills", all_skills)
experience = st.sidebar.slider("Experience", 0, 10, 1)
target_role = st.sidebar.selectbox("🎯 Target Role", list(roles_data.keys()))
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

        best_role = top_roles.iloc[0]["Role"]

        # ---------------- SKILL STRENGTH ----------------
        st.subheader("📊 Skill Strength (Rate Yourself)")

        skill_levels = {}
        for skill in selected_skills:
            level = st.slider(f"{skill} proficiency (%)", 0, 100, 50)
            skill_levels[skill] = level

        st.write("### 📈 Your Skill Strength")
        for skill, level in skill_levels.items():
            st.write(f"{skill}: {level}%")
            st.progress(level)

        # ---------------- ROADMAP ----------------
        st.subheader("🧠 Detailed Career Roadmap")

        if best_role in roadmaps:
            for i, item in enumerate(roadmaps[best_role]):
                st.markdown(f"### Step {i+1}: {item['step']}")
                st.write(f"👉 {item['desc']}")
                st.write("📚 Resources:")
                for link in item["resources"]:
                    st.write(link)
                st.markdown("---")
        else:
            st.info("Roadmap coming soon for this role")

        # ---------------- MISSING SKILLS ----------------
        st.subheader("🚨 Skills You Need to Learn")

        required_skills = set(roles_data[best_role])
        missing_skills = required_skills - set(selected_skills)

        if missing_skills:
            for skill in missing_skills:
                st.write(f"❌ {skill}")
                if skill in learning_links:
                    st.write(f"Learn here: {learning_links[skill]}")
        else:
            st.success("🔥 You already have all required skills!")

        # ---------------- TRENDS ----------------
        st.subheader("📈 Job Market Trends")
        trend_df = pd.DataFrame({
            "Role": list(trend_data.keys()),
            "Demand": list(trend_data.values())
        })
        st.bar_chart(trend_df.set_index("Role"))

        # ---------------- CAREER SWITCH ----------------
        st.subheader("🔄 Career Switch Simulator")
        needed = set(roles_data[target_role]) - set(selected_skills)
        st.write(f"To switch to **{target_role}**, you need:")
        st.error(", ".join(needed) if needed else "You are ready!")

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

            file = "career_report.pdf"
            pdf.output(file)
            return file

        if st.button("Download PDF"):
            file = generate_pdf()
            with open(file, "rb") as f:
                st.download_button("Download Now", f, file_name="career_report.pdf")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔥 AI Career Intelligence PRO | Advanced ML Project")
