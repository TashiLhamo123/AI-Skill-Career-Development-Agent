
import streamlit as st
import pandas as pd
from llm_agent import generate_career_advice

from tools import (
    careers,
    courses,
    skills,
    analyze_skill_gaps,
    explain_career_match
)

from planner import create_learning_plan

from memory import (
    save_feedback,
    get_feedback,
    save_course_progress,
    get_course_progress
)

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Career Development Agent",
    page_icon="🎯",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f5f7fc;
    color: #202b45;
}

/* Main content */
.block-container {
    padding-top: 165px !important;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* ==========================================
   FIXED TOP NAVIGATION
========================================== */

.st-key-sticky_nav {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    z-index: 999999 !important;
    background: #ffffff !important;
    padding: 10px 25px 12px 25px !important;
    margin: 0 !important;
    border-bottom: 1px solid #e4e8f1 !important;
    border-radius: 0 !important;
    box-shadow: 0 4px 15px rgba(30,45,80,0.12) !important;
    box-sizing: border-box !important;
}

/* Navigation heading */
.st-key-sticky_nav h3 {
    color: #5146c8 !important;
    font-size: 21px !important;
    margin: 0 0 8px 0 !important;
}

/* Horizontal menu */
.st-key-sticky_nav [role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 8px !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    width: 100% !important;
    padding: 5px 2px !important;
    scrollbar-width: thin;
}

/* Navigation items */
.st-key-sticky_nav [role="radiogroup"] label {
    flex: 0 0 auto !important;
    white-space: nowrap !important;
    background: #f0f2fa !important;
    border: 1px solid transparent !important;
    border-radius: 9px !important;
    padding: 8px 13px !important;
    color: #354366 !important;
    transition: 0.2s ease;
}

/* Hover effect */
.st-key-sticky_nav [role="radiogroup"] label:hover {
    background: #e5e9ff !important;
    border-color: #7567dc !important;
}

/* Selected navigation item */
.st-key-sticky_nav [role="radiogroup"] label:has(input:checked) {
    background: #5146c8 !important;
    color: white !important;
    border-color: #5146c8 !important;
}

/* Hide radio circles */
.st-key-sticky_nav [role="radiogroup"] input {
    display: none !important;
}

/* ==========================================
   HOME DASHBOARD IMAGE
========================================== */

.hero-image {
    width: 100vw;
    height: 35vh;
    min-height: 250px;
    background-image: url("https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1800&q=85");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    border-radius: 15px;
    margin-top: 20px;
    margin-bottom: 25px;

    /* Extend image to the full browser width */
    position: relative;
    left: 50%;
    transform: translateX(-50%);
}

/* ==========================================
   HEADINGS
========================================== */

h1 {
    color: #19284b !important;
    font-weight: 750 !important;
}

h2, h3 {
    color: #283b69 !important;
}

/* ==========================================
   METRIC CARDS
========================================== */

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e6e9f2;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 3px 12px rgba(35,50,90,0.05);
}

/* ==========================================
   CONTENT CARDS
========================================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-radius: 14px;
    border-color: #e5e9f2;
}

/* ==========================================
   BUTTONS
========================================== */

.stButton > button,
.stLinkButton > a {
    background: linear-gradient(90deg, #5146c8, #7567dc);
    color: white !important;
    border: none;
    border-radius: 9px;
    padding: 9px 20px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover,
.stLinkButton > a:hover {
    background: #39319c;
    color: white !important;
    border: none;
}

/* ==========================================
   INPUTS
========================================== */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    border-radius: 9px;
}

/* ==========================================
   PROGRESS
========================================== */

[data-testid="stProgressBar"] {
    border-radius: 10px;
}

/* ==========================================
   FOOTER
========================================== */

.footer {
    text-align: center;
    color: #77819a;
    font-size: 13px;
    padding: 20px;
}

/* Hide default sidebar */
[data-testid="stSidebar"] {
    display: none;
}

/* ==========================================
   RESPONSIVE DESIGN
========================================== */

@media (max-width: 700px) {

    .block-container {
        padding-top: 175px !important;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .st-key-sticky_nav {
        padding: 8px 12px !important;
    }

    .st-key-sticky_nav h3 {
        font-size: 17px !important;
    }

    .st-key-sticky_nav [role="radiogroup"] label {
        padding: 7px 10px !important;
        font-size: 12px !important;
    }

    .hero-image {
        height: 35vh;
        min-height: 200px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HORIZONTAL FIXED NAVIGATION
# ==================================================

pages = [
    "🏠 Home",
    "👤 Student Profile",
    "📊 Skill Analysis",
    "💼 Careers",
    "📚 Resources",
    "🗺️ Learning Roadmap",
    "📈 Feedback & Progress"
]

with st.container(key="sticky_nav"):

    st.markdown(
        "<h3>🎯 Career Development Agent</h3>",
        unsafe_allow_html=True
    )

    selected_page = st.radio(
        "Navigation",
        pages,
        horizontal=True,
        label_visibility="collapsed",
        key="main_navigation"
    )


# ==================================================
# HOME DASHBOARD
# ==================================================

if selected_page == "🏠 Home":

    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg,#252b69,#6557c9);
            padding:35px;
            border-radius:18px;
            color:white;
            margin-bottom:25px;
        ">
            <h1 style="color:white !important;">
                Build Your Future Career 🚀
            </h1>
            <p style="font-size:17px;color:white;">
                Discover your skills, explore career opportunities,
                and create a personalized learning journey.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Full-width image with 35vh height
    st.markdown(
        '<div class="hero-image"></div>',
        unsafe_allow_html=True
    )

    st.subheader("Your Career Development Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Career Options", len(careers))

    with col2:
        st.metric("Available Skills", len(skills))

    with col3:
        st.metric("Learning Resources", len(courses))

    st.divider()

    st.subheader("What Can You Do With This Agent?")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):
            st.markdown("### 📊 Skill Gap Analysis")
            st.write(
                "Identify the skills you already have "
                "and discover what you need to improve."
            )

        with st.container(border=True):
            st.markdown("### 📚 Learning Resources")
            st.write(
                "Explore courses and learning materials "
                "to improve your technical and soft skills."
            )

    with col2:

        with st.container(border=True):
            st.markdown("### 💼 Career Recommendations")
            st.write(
                "Discover careers that match your current "
                "skills and interests."
            )

        with st.container(border=True):
            st.markdown("### 🗺️ Personalized Roadmap")
            st.write(
                "Follow a learning plan designed around "
                "your selected career goal."
            )

    st.info(
        "Note: Career recommendations are based on the available "
        "sample dataset. They provide educational guidance and "
        "do not guarantee employment."
    )


# ==================================================
# STUDENT PROFILE
# ==================================================

elif selected_page == "👤 Student Profile":

    st.title("👤 Student Profile")

    st.write("Enter your details to create your student profile.")

    with st.container(border=True):

        name = st.text_input("Enter your name")

        education = st.text_input("Enter your education level")

        career_goal = st.selectbox(
            "Select your career goal",
            careers["career"].tolist()
        )

        student_skills = st.multiselect(
            "Select your current skills",
            skills["skill"].tolist()
        )

        if st.button("Save Profile", width="stretch"):

            if not name.strip():

                st.warning("Please enter your name.")

            else:

                st.session_state["student_name"] = name
                st.session_state["education"] = education
                st.session_state["career_goal"] = career_goal
                st.session_state["student_skills"] = student_skills

                st.success("Student profile saved successfully!")

    if "student_name" in st.session_state:

        st.subheader("Your Saved Profile")

        st.write("**Name:**", st.session_state["student_name"])
        st.write("**Education:**", st.session_state["education"])
        st.write("**Career Goal:**", st.session_state["career_goal"])

        st.write(
            "**Skills:**",
            ", ".join(st.session_state["student_skills"])
            if st.session_state["student_skills"]
            else "No skills selected"
        )


# ==================================================
# SKILL GAP ANALYSIS
# ==================================================


elif selected_page == "📊 Skill Analysis":

    st.title("📊 Skill Gap Analysis")

    st.write(
        "Discover your current skill level and identify "
        "the skills you need to improve."
    )

    with st.container(border=True):

        career_goal = st.selectbox(
            "Choose your career goal",
            careers["career"].tolist()
        )

        student_skills = st.multiselect(
            "Select your current skills",
            skills["skill"].tolist()
        )

    # SKILL ANALYSIS BUTTON
    if st.button("Analyze My Skills", width="stretch"):

        if not student_skills:
            st.warning("Please select at least one skill.")

        else:
            result = analyze_skill_gaps(
                student_skills,
                career_goal
            )

            if "error" in result:
                st.error(result["error"])

            else:
                st.subheader("Your Skill Analysis")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Skill Match",
                        f"{result['match_percentage']}%"
                    )

                with col2:
                    st.metric(
                        "Missing Skills",
                        len(result["missing_skills"])
                    )

                st.progress(
                    result["match_percentage"] / 100
                )

                col1, col2 = st.columns(2)

                with col1:
                    with st.container(border=True):
                        st.subheader("✅ Skills You Have")

                        if result["available_skills"]:
                            for skill in result["available_skills"]:
                                st.write("🟢", skill)
                        else:
                            st.info("No matching skills found.")

                with col2:
                    with st.container(border=True):
                        st.subheader("📌 Skills to Improve")

                        if result["missing_skills"]:
                            for skill in result["missing_skills"]:
                                st.write("🔸", skill)
                        else:
                            st.success("You have all required skills!")

                st.subheader("Skill Match Chart")

                chart_data = pd.DataFrame({
                    "Category": [
                        "Available Skills",
                        "Missing Skills"
                    ],
                    "Number of Skills": [
                        len(result["available_skills"]),
                        len(result["missing_skills"])
                    ]
                })

                st.bar_chart(
                    chart_data.set_index("Category"),
                    width="stretch"
                )

    # AI CAREER ADVICE SECTION
    st.divider()
    st.subheader("🤖 AI-Powered Career Advice")

    st.write(
        "Get personalized career guidance using the Llama language model."
    )

    if st.button("Generate AI Career Advice", width="stretch"):

        if not student_skills:
            st.warning("Please select at least one skill first.")

        else:
            ai_result = analyze_skill_gaps(
                student_skills,
                career_goal
            )

            if "error" in ai_result:
                st.error(ai_result["error"])

            else:
                with st.spinner("Generating AI career advice..."):

                    advice = generate_career_advice(
                        career_goal,
                        ai_result["available_skills"],
                        ai_result["missing_skills"]
                    )

                st.markdown("### Your Personalized AI Career Advice")
                st.markdown(advice)

                st.caption(
                    "Generated using the local Llama 3.2 1B model."
                )
     
# ==================================================
# CAREER RECOMMENDATIONS
# ==================================================

elif selected_page == "💼 Careers":

    st.title("💼 Career Recommendations")

    st.write(
        "Discover career opportunities based on your "
        "current skills."
    )

    with st.container(border=True):

        student_skills = st.multiselect(
            "Select your skills",
            skills["skill"].tolist()
        )

        find_button = st.button(
            "Find Suitable Careers",
            width="stretch"
        )

    if find_button:

        if not student_skills:

            st.warning("Please select at least one skill.")

        else:

            career_results = []

            for _, career in careers.iterrows():

                career_name = career["career"]

                explanation = explain_career_match(
                    student_skills,
                    career_name
                )

                if "error" in explanation:
                    continue

                match_percentage = explanation["match_percentage"]

                if match_percentage >= 70:
                    confidence = "High"
                elif match_percentage >= 40:
                    confidence = "Medium"
                else:
                    confidence = "Low"

                career_results.append({
                    "Career": career_name,
                    "Match Percentage": match_percentage,
                    "Confidence Level": confidence,
                    "Matched Skills": ", ".join(
                        explanation["matched_skills"]
                    ),
                    "Required Skills": (
                        len(explanation["matched_skills"])
                        + len(explanation["missing_skills"])
                    ),
                    "Explanation": explanation["explanation"]
                })

            results_df = pd.DataFrame(career_results)

            results_df = results_df.sort_values(
                by="Match Percentage",
                ascending=False
            )

            st.subheader("Your Career Matches")

            st.dataframe(
                results_df[
                    [
                        "Career",
                        "Match Percentage",
                        "Confidence Level",
                        "Matched Skills",
                        "Required Skills"
                    ]
                ],
                width="stretch",
                hide_index=True
            )

            st.subheader("Career Match Chart")

            chart_data = results_df.set_index("Career")[
                ["Match Percentage"]
            ]

            st.bar_chart(
                chart_data,
                width="stretch"
            )

            st.subheader("Why These Careers Are Recommended")

            for _, row in results_df.iterrows():

                with st.expander(
                    f"{row['Career']} — "
                    f"{row['Match Percentage']}% Match "
                    f"({row['Confidence Level']} Confidence)"
                ):

                    st.write(row["Explanation"])

                    st.write(
                        "**Matching Skills:**",
                        row["Matched Skills"]
                        if row["Matched Skills"]
                        else "No matching skills yet."
                    )

            st.info(
                "Confidence levels are rule-based labels derived "
                "from skill match percentages. They are not "
                "statistical probabilities or guarantees of job suitability."
            )


# ==================================================
# LEARNING RESOURCES
# ==================================================

elif selected_page == "📚 Resources":

    st.title("📚 Learning Resources")

    st.write(
        "Explore courses to improve your technical "
        "and soft skills."
    )

    selected_skill = st.selectbox(
        "Choose a skill",
        skills["skill"].tolist()
    )

    recommended_courses = courses[
        courses["skill"].str.lower() == selected_skill.lower()
    ]

    st.subheader("Recommended Courses")

    if recommended_courses.empty:

        st.warning("No courses are currently available for this skill.")

    else:

        for _, course in recommended_courses.iterrows():

            with st.container(border=True):

                st.markdown(
                    f"### 📘 {course['course_name']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Skill:**", course["skill"])
                    st.write("**Platform:**", course["platform"])

                with col2:
                    st.write("**Level:**", course["level"])
                    st.write("**Duration:**", course["duration"])

                st.link_button(
                    "Visit Learning Platform ↗",
                    course["link"]
                )

    st.caption(
        "These are sample learning recommendations. Links lead "
        "to platform websites, not verified individual course pages."
    )


# ==================================================
# PERSONALIZED LEARNING ROADMAP
# ==================================================

elif selected_page == "🗺️ Learning Roadmap":

    st.title("🗺️ Personalized Learning Roadmap")

    st.write(
        "Create a step-by-step learning plan based on "
        "your career goal and current skills."
    )

    with st.container(border=True):

        career_goal = st.selectbox(
            "Choose your career goal",
            careers["career"].tolist(),
            key="roadmap_career"
        )

        student_skills = st.multiselect(
            "Select your current skills",
            skills["skill"].tolist(),
            key="roadmap_skills"
        )

        generate_button = st.button(
            "Generate My Learning Roadmap",
            width="stretch"
        )

    if generate_button:

        if not student_skills:

            st.warning("Please select at least one skill.")

        else:

            plan = create_learning_plan(
                student_skills,
                career_goal
            )

            if "error" in plan:

                st.error(plan["error"])

            else:

                st.subheader("🎯 Your Career Goal")
                st.success(career_goal)

                st.subheader("Current Skill Match")

                st.metric(
                    "Skill Match",
                    f"{plan['match_percentage']}%"
                )

                st.progress(
                    plan["match_percentage"] / 100
                )

                st.subheader("Skills You Need to Improve")

                if plan["missing_skills"]:

                    for skill in plan["missing_skills"]:
                        st.write("📌", skill)

                else:

                    st.success(
                        "You already have all the required skills!"
                    )

                st.subheader("Your Recommended Learning Roadmap")

                if plan["learning_plan"]:

                    for index, course in enumerate(
                        plan["learning_plan"], start=1
                    ):

                        with st.container(border=True):

                            st.markdown(
                                f"### Step {index}: {course['course']}"
                            )

                            st.write("**Skill:**", course["skill"])
                            st.write("**Platform:**", course["platform"])
                            st.write("**Duration:**", course["duration"])

                            st.link_button(
                                "Start Learning ↗",
                                course["link"]
                            )

                else:

                    st.info(
                        "No additional courses are needed based on "
                        "the current dataset."
                    )


# ==================================================
# FEEDBACK AND PROGRESS
# ==================================================

elif selected_page == "📈 Feedback & Progress":

    st.title("📈 Feedback and Progress")

    st.write(
        "Share your feedback and track your learning journey."
    )

    st.subheader("💬 Submit Your Feedback")

    with st.container(border=True):

        feedback_text = st.text_area(
            "What would you like the agent to improve?"
        )

        if st.button("Submit Feedback", width="stretch"):

            if feedback_text.strip():

                save_feedback(feedback_text)

                st.success("Your feedback has been saved!")
                st.rerun()

            else:

                st.warning("Please enter your feedback.")

    st.divider()

    st.subheader("Previous Feedback")

    previous_feedback = get_feedback()

    if previous_feedback:

        for feedback, created_at in previous_feedback:

            with st.container(border=True):

                st.write("**Feedback:**", feedback)
                st.caption("Submitted: " + str(created_at))

    else:

        st.info("No feedback submitted yet.")

    st.divider()

    st.subheader("📚 Update Learning Progress")

    course_list = courses["course_name"].tolist()

    with st.container(border=True):

        selected_course = st.selectbox(
            "Select a course",
            course_list
        )

        progress_status = st.selectbox(
            "Update course status",
            ["Not Started", "In Progress", "Completed"]
        )

        if st.button("Update Progress", width="stretch"):

            save_course_progress(
                selected_course,
                progress_status
            )

            st.success("Course progress updated successfully!")
            st.rerun()

    st.divider()

    st.subheader("Your Course Progress")

    progress_records = get_course_progress()

    if progress_records:

        completed_courses = sum(
            1 for record in progress_records
            if record[1] == "Completed"
        )

        total_courses = len(progress_records)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Courses Tracked", total_courses)

        with col2:
            st.metric("Completed Courses", completed_courses)

        for course_name, status, updated_at in progress_records:

            with st.container(border=True):

                st.write("**Course:**", course_name)
                st.write("**Status:**", status)
                st.caption("Last updated: " + str(updated_at))

    else:

        st.info("No learning progress recorded yet.")


# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    🎯 AI-Powered Skill Gap and Career Development Agent
    <br>
    Helping students discover skills and build their future careers.
</div>
""", unsafe_allow_html=True)
