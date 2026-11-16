
import pandas as pd
import os

# Find project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load datasets
careers = pd.read_csv(
    os.path.join(BASE_DIR, "data", "careers.csv")
)

courses = pd.read_csv(
    os.path.join(BASE_DIR, "data", "courses.csv")
)

skills = pd.read_csv(
    os.path.join(BASE_DIR, "data", "skills.csv")
)


# TOOL 1: Analyze skill gaps
def analyze_skill_gaps(student_skills, career_name):

    # Validate career name
    if not isinstance(career_name, str) or not career_name.strip():
        return {"error": "Please provide a valid career name."}

    # Validate student skills
    if not isinstance(student_skills, (list, tuple, set)):
        return {"error": "Student skills must be provided as a list."}

    # Find selected career
    career = careers[
        careers["career"].str.lower() == career_name.strip().lower()
    ]

    if career.empty:
        return {"error": "Career not found."}

    # Get required skills
    required_skills = [
        skill.strip()
        for skill in career.iloc[0]["required_skills"].split(",")
    ]

    # Clean and remove duplicate skills
    valid_skills = set(skills["skill"].str.lower())

    cleaned_skills = []
    invalid_skills = []

    for skill in student_skills:

        if not isinstance(skill, str) or not skill.strip():
            continue

        skill_name = skill.strip()

        if skill_name.lower() in valid_skills:
            if skill_name.lower() not in [
                item.lower() for item in cleaned_skills
            ]:
                cleaned_skills.append(skill_name)

        else:
            if skill_name not in invalid_skills:
                invalid_skills.append(skill_name)

    # Compare student skills
    available_skills = [
        skill for skill in required_skills
        if skill.lower() in [
            item.lower() for item in cleaned_skills
        ]
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in [
            item.lower() for item in cleaned_skills
        ]
    ]

    # Calculate skill match percentage
    match_percentage = (
        len(available_skills) / len(required_skills)
    ) * 100

    return {
        "career": career_name.strip(),
        "available_skills": available_skills,
        "missing_skills": missing_skills,
        "invalid_skills": invalid_skills,
        "match_percentage": round(match_percentage, 2)
    }


# TOOL 2: Recommend learning courses
def recommend_courses(missing_skills):

    if not isinstance(missing_skills, (list, tuple, set)):
        return courses.iloc[0:0].copy()

    cleaned_skills = [
        skill.strip().lower()
        for skill in missing_skills
        if isinstance(skill, str) and skill.strip()
    ]

    recommendations = courses[
        courses["skill"].str.lower().isin(cleaned_skills)
    ]

    return recommendations


# TOOL 3: Explain career recommendations
def explain_career_match(student_skills, career_name):

    result = analyze_skill_gaps(
        student_skills,
        career_name
    )

    if "error" in result:
        return result

    matched = result["available_skills"]
    missing = result["missing_skills"]

    total_skills = len(matched) + len(missing)

    explanation = (
        f"This career is recommended because you already have "
        f"{len(matched)} out of {total_skills} required skills."
    )

    if matched:
        explanation += (
            f" Your matching skills are: {', '.join(matched)}."
        )

    if missing:
        explanation += (
            f" You should improve these skills: {', '.join(missing)}."
        )
    else:
        explanation += " You have all the required skills listed."

    if result["invalid_skills"]:
        explanation += (
            f" The following unrecognized skills were ignored: "
            f"{', '.join(result['invalid_skills'])}."
        )

    return {
        "career": result["career"],
        "match_percentage": result["match_percentage"],
        "matched_skills": matched,
        "missing_skills": missing,
        "invalid_skills": result["invalid_skills"],
        "explanation": explanation
    }


# TEST THE TOOLS
if __name__ == "__main__":

    print("\n========== SKILL GAP ANALYSIS ==========")

    student_skills = [
        "Python",
        "SQL",
        "Excel",
        "Python",
        "Unknown Skill"
    ]

    result = analyze_skill_gaps(
        student_skills,
        "Data Analyst"
    )

    print(result)

    print("\n========== COURSE RECOMMENDATIONS ==========")

    if "error" not in result:

        recommended = recommend_courses(
            result["missing_skills"]
        )

        print(recommended.to_string(index=False))

    print("\n========== CAREER RECOMMENDATION EXPLANATION ==========")

    explanation = explain_career_match(
        student_skills,
        "Data Analyst"
    )

    if "error" not in explanation:
        print(explanation["explanation"])
    else:
        print(explanation["error"])
