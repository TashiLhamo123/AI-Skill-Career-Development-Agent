
from memory import save_feedback, get_feedback
from tools import recommend_courses


def adapt_recommendations(missing_skills, feedback_text):

    print("\n========== AGENT FEEDBACK SYSTEM ==========")

    # Step 1: Save student feedback
    print("Step 1: Saving student feedback...")

    save_feedback(feedback_text)

    # Step 2: Understand student preferences
    print("Step 2: Understanding student preferences...")

    feedback = feedback_text.lower()

    # Step 3: Get suitable courses
    print("Step 3: Updating course recommendations...")

    recommendations = recommend_courses(missing_skills)

    # Adapt recommendations based on feedback
    if "short" in feedback:
        recommendations = recommendations.copy()

        recommendations["weeks"] = (
            recommendations["duration"]
            .str.extract(r"(\d+)")
            .astype(int)
        )

        recommendations = recommendations.sort_values("weeks")

    elif "practical" in feedback:
        recommendations = recommendations.copy()

        practical_platforms = [
            "DataCamp",
            "freeCodeCamp",
            "Microsoft Learn"
        ]

        recommendations["priority"] = recommendations["platform"].apply(
            lambda platform: 0
            if platform in practical_platforms else 1
        )

        recommendations = recommendations.sort_values("priority")

    elif "beginner" in feedback:
        recommendations = recommendations[
            recommendations["level"].str.lower() == "beginner"
        ]

    # Step 4: Retrieve saved feedback
    print("Step 4: Retrieving previous feedback...")

    previous_feedback = get_feedback()

    return recommendations, previous_feedback


# Test feedback adaptation
if __name__ == "__main__":

    missing_skills = [
        "Python",
        "Power BI",
        "Statistics"
    ]

    student_feedback = "I want short courses."

    recommendations, previous_feedback = adapt_recommendations(
        missing_skills,
        student_feedback
    )

    print("\n========== ADAPTED RECOMMENDATIONS ==========")

    if recommendations.empty:
        print("No matching courses found.")
    else:
        print(recommendations[
            ["course_name", "skill", "platform", "duration"]
        ].to_string(index=False))

    print("\n========== SAVED FEEDBACK ==========")

    for feedback in previous_feedback:
        print(feedback)

    print("\nAgent feedback adaptation completed!")
