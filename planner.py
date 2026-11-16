
from tools import analyze_skill_gaps, recommend_courses
from memory import (
    initialize_memory,
    save_student_memory,
    get_student_memory
)


def create_learning_plan(student_skills, career_name):

    print("\n========== AGENT PLANNING ==========")

    # Step 1: Initialize memory
    print("Step 1: Checking agent memory...")
    initialize_memory()

    # Step 2: Save student information
    print("Step 2: Saving student information...")

    save_student_memory(career_name, student_skills)

    # Step 3: Analyze skills
    print("Step 3: Analyzing student skills...")

    analysis = analyze_skill_gaps(
        student_skills,
        career_name
    )

    if "error" in analysis:
        return analysis

    # Step 4: Identify missing skills
    print("Step 4: Identifying missing skills...")

    missing_skills = analysis["missing_skills"]

    # Step 5: Recommend courses
    print("Step 5: Finding learning resources...")

    recommended_courses = recommend_courses(missing_skills)

    # Step 6: Create learning plan
    print("Step 6: Creating personalized learning plan...")

    learning_plan = []

    for _, course in recommended_courses.iterrows():

        learning_plan.append({
            "skill": course["skill"],
            "course": course["course_name"],
            "platform": course["platform"],
            "duration": course["duration"],
            "link": course["link"]
        })

    # Step 7: Retrieve saved memory
    print("Step 7: Retrieving student memory...")

    previous_memory = get_student_memory()

    return {
        "career": career_name,
        "match_percentage": analysis["match_percentage"],
        "available_skills": analysis["available_skills"],
        "missing_skills": missing_skills,
        "learning_plan": learning_plan,
        "previous_memory": previous_memory
    }


# Test the updated planner
if __name__ == "__main__":

    student_skills = ["Python", "SQL", "Excel"]

    result = create_learning_plan(
        student_skills,
        "Data Analyst"
    )

    print("\n========== FINAL AGENT RESULT ==========")

    if "error" in result:
        print(result["error"])

    else:
        print("Career:", result["career"])
        print("Skill Match:", result["match_percentage"], "%")

        print("\nMissing Skills:")
        for skill in result["missing_skills"]:
            print("-", skill)

        print("\nLearning Recommendations:")
        for item in result["learning_plan"]:
            print(item["course"], "-", item["platform"])

        print("\nRetrieved Previous Memory:")
        print(result["previous_memory"])

        print("\nAgent successfully completed its workflow!")
