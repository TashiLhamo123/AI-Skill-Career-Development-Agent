
from planner import create_learning_plan
from feedback import adapt_recommendations


def run_agent():

    print("\n======================================")
    print("   AI SKILL AND CAREER DEVELOPMENT AGENT")
    print("======================================")

    # Student information
    student_skills = ["Python", "SQL", "Excel"]
    career_goal = "Data Analyst"

    # Step 1: Create learning plan
    print("\nStep 1: Starting career analysis...")

    result = create_learning_plan(
        student_skills,
        career_goal
    )

    if "error" in result:
        print(result["error"])
        return

    # Step 2: Display skill gap analysis
    print("\n========== SKILL GAP ANALYSIS ==========")

    print("Career Goal:", result["career"])
    print("Skill Match:", result["match_percentage"], "%")

    print("\nMissing Skills:")

    for skill in result["missing_skills"]:
        print("-", skill)

    # Step 3: Display initial learning plan
    print("\n========== INITIAL LEARNING PLAN ==========")

    for course in result["learning_plan"]:
        print(
            course["course"],
            "-",
            course["platform"],
            "-",
            course["duration"]
        )

    # Step 4: Collect student feedback
    print("\n========== STUDENT FEEDBACK ==========")

    feedback = input(
        "What would you like to improve? "
    )

    # Step 5: Adapt recommendations
    print("\nStep 5: Adapting the learning plan...")

    adapted_courses, previous_feedback = adapt_recommendations(
        result["missing_skills"],
        feedback
    )

    # Step 6: Display adapted recommendations
    print("\n========== UPDATED LEARNING PLAN ==========")

    if adapted_courses.empty:
        print("No matching courses found.")
    else:
        for _, course in adapted_courses.iterrows():
            print(
                course["course_name"],
                "-",
                course["platform"],
                "-",
                course["duration"]
            )

    print("\n========== AGENT SUMMARY ==========")
    print("Career goal:", career_goal)
    print("Skill match:", result["match_percentage"], "%")
    print("Feedback saved successfully.")
    print("Previous feedback records:", len(previous_feedback))

    print("\nAgent workflow completed successfully!")


if __name__ == "__main__":
    run_agent()
