import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Career Intelligence PRO", layout="wide")

st.title("🚀 AI Career Intelligence PRO")
st.write("Next-Gen Career Analyzer with AI Insights")

# ---------------- SESSION STATE ----------------
if "analyze_clicked" not in st.session_state:
    st.session_state.analyze_clicked = False

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
    "Data Scientist": [
        {"step": "Learn Python Basics", "desc": "Syntax, loops, OOP",
         "resources": ["https://www.w3schools.com/python/"]},
        {"step": "Statistics", "desc": "Probability, distributions",
         "resources": ["https://www.khanacademy.org/math/statistics-probability"]},
        {"step": "Machine Learning", "desc": "Supervised & unsupervised learning",
         "resources": ["https://www.coursera.org/learn/machine-learning"]}
    ]
}

learning_links = {
    "python": "https://www.w3schools.com/python/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "tensorflow": "https://www.tensorflow.org/tutorials",
    "react": "https://react.dev/learn",
    "sql": "https://www.w3schools.com/sql/"
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

if st.sidebar.button("🚀 Analyze"):
    st.session_state.analyze_clicked = True

# ---------------- MODEL ----------------
vectorizer = TfidfVectorizer()
skill_matrix = vectorizer.fit_transform(df["Skills"])

# ---------------- MAIN ----------------
if st.session_state.analyze_clicked:

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

        # ---------------- MISSING SKILLS ----------------
        st.subheader("🚨 Skills You Need to Learn")

        required = set(roles_data[best_role])
        missing_skills = required - set(selected_skills)

        if missing_skills:
            for skill in missing_skills:
                st.write(f"❌ {skill}")
                if skill in learning_links:
                    st.write(f"Learn: {learning_links[skill]}")
        else:
            st.success("🔥 You already have all required skills!")

        # ---------------- EXCEL DOWNLOAD ----------------
        st.subheader("📊 Download Report (Excel)")

        report_df = pd.DataFrame({
            "Selected Skills": selected_skills,
        })

        summary_df = pd.DataFrame({
            "Best Role": [best_role],
            "Salary": [salary_data[best_role]]
        })

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            report_df.to_excel(writer, sheet_name='Skills', index=False)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

        st.download_button(
            label="Download Excel Report",
            data=output.getvalue(),
            file_name="career_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔥 AI Career Intelligence PRO | Advanced ML Project")
