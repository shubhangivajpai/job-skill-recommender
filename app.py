import streamlit as st
import pandas as pd
from collections import Counter

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Skill Recommender", layout="centered")

# ---------------- TITLE ---------------- #
st.write("🔥 NEW VERSION LOADED")
st.title("Job Market Skill Recommender 🚀")
st.markdown("### Discover what skills to learn next based on real job data")

st.divider()

# ---------------- LOAD DATA ---------------- #
df = pd.read_csv("job_skills.csv")

# ---------------- CLEAN DATA ---------------- #
df['job_skills'] = df['job_skills'].fillna("")

all_skills = []

for skill_text in df["job_skills"]:   # 🔧 renamed variable (avoid confusion)
    skill_list = skill_text.split(',')
    skill_list = [s.strip().lower() for s in skill_list]
    all_skills.extend(skill_list)

# ---------------- NORMALIZE ---------------- #
skill_map = {
    "communication skills": "communication",
    "data analytics": "data analysis"
}

cleaned_skills = []

for skill in all_skills:
    if skill in skill_map:
        cleaned_skills.append(skill_map[skill])
    else:
        cleaned_skills.append(skill)

# ---------------- COUNT ---------------- #
skill_count = Counter(cleaned_skills)

# ---------------- INPUT SECTION ---------------- #
st.subheader("🧠 Enter Your Skills")

user_input = st.text_input(
    "Enter your skills (comma separated):",
    placeholder="python, sql"
)

# ---------------- BUTTON ---------------- #
if st.button("🔍 Get Recommendations"):

    if user_input.strip():   # 🔧 better validation

        user_skills = [s.strip().lower() for s in user_input.split(",")]

        st.success(f"Your skills: {', '.join(user_skills)}")

        # ---------------- VALIDATION ---------------- #
        known_skills = set(skill_count.keys())
        unknown = [s for s in user_skills if s not in known_skills]

        if unknown:
            st.warning(f"⚠️ Not common in data roles: {', '.join(unknown)}")

        # ---------------- RECOMMENDATION ---------------- #
        recommendations = []

        for skill, count in skill_count.most_common():
            if skill not in user_skills:
                recommendations.append((skill, count))

        st.subheader("📈 Recommended Skills")

        for skill, count in recommendations[:5]:
            st.markdown(f"✅ **{skill}** — demand: {count}")

    else:
        st.error("Please enter at least one skill")