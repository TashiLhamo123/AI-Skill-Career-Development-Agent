
from tools import (
    analyze_skill_gaps,
    recommend_courses,
    explain_career_match
)
from planner import create_learning_plan
from feedback import adapt_recommendations


print("\n========== AGENT EVALUATION ==========")

passed = 0
failed = 0


def record_result(condition, success_message, failure_message):
    global passed, failed

    if condition:
        print("PASS:", success_message)
        passed += 1
    else:
        print("FAIL:", failure_message)
        failed += 1


# Test 1: Skill Gap Analysis
print("\nTest 1: Skill Gap Analysis")

result = analyze_skill_gaps(
    ["Python", "SQL", "Excel"],
    "Data Analyst"
)

record_result(
    result["match_percentage"] == 50.0
    and result["missing_skills"] == [
        "Power BI", "Statistics", "Data Visualization"
    ],
    "Skill gap analysis is correct.",
    "Skill gap analysis is incorrect."
)


# Test 2: Course Recommendations
print("\nTest 2: Course Recommendations")

recommended = recommend_courses([
    "Power BI", "Statistics", "Data Visualization"
])

expected_courses = [
    "Power BI Fundamentals",
    "Introduction to Statistics",
    "Data Visualization Basics"
]

actual_courses = recommended["course_name"].tolist()

record_result(
    actual_courses == expected_courses,
    "Course recommendations are correct.",
    "Course recommendations are incorrect."
)


# Test 3: Personalized Learning Plan
print("\nTest 3: Personalized Learning Plan")

result = create_learning_plan(
    ["Python", "SQL", "Excel"],
    "Data Analyst"
)

record_result(
    result["career"] == "Data Analyst"
    and result["match_percentage"] == 50.0
    and len(result["learning_plan"]) == 3,
    "Personalized learning plan is correct.",
    "Personalized learning plan is incorrect."
)


# Test 4: Feedback Adaptation
print("\nTest 4: Feedback Adaptation")

recommendations, previous_feedback = adapt_recommendations(
    ["Power BI", "Statistics", "Data Visualization"],
    "I want short courses."
)

durations = recommendations["duration"].tolist()

record_result(
    len(durations) > 0
    and durations[0] == "2 weeks",
    "Agent adapts recommendations based on feedback.",
    "Feedback adaptation is incorrect."
)


# Test 5: Invalid Career Handling
print("\nTest 5: Invalid Career Handling")

result = analyze_skill_gaps(
    ["Python", "SQL"],
    "Doctor"
)

record_result(
    "error" in result,
    "Agent correctly handles an invalid career.",
    "Agent failed to handle an invalid career."
)


# Test 6: Empty Skills Handling
print("\nTest 6: Empty Skills Handling")

result = analyze_skill_gaps(
    [],
    "Data Analyst"
)

record_result(
    result["match_percentage"] == 0.0
    and len(result["missing_skills"]) == 6,
    "Agent correctly handles an empty skills list.",
    "Empty skills handling is incorrect."
)


# Test 7: Career Recommendation Explanation
print("\nTest 7: Career Recommendation Explanation")

result = explain_career_match(
    ["Python", "SQL", "Excel"],
    "Data Analyst"
)

record_result(
    result["match_percentage"] == 50.0
    and len(result["matched_skills"]) == 3
    and len(result["missing_skills"]) == 3
    and "recommended" in result["explanation"].lower(),
    "Career recommendation explanation is correct.",
    "Career recommendation explanation is incorrect."
)


# Test 8: Invalid Career Explanation
print("\nTest 8: Invalid Career Explanation")

result = explain_career_match(
    ["Python", "SQL"],
    "Doctor"
)

record_result(
    "error" in result,
    "Career explanation handles invalid career correctly.",
    "Career explanation failed to handle invalid career."
)


# Final Evaluation Summary
total_tests = passed + failed

success_rate = (passed / total_tests) * 100

print("\n========== FINAL EVALUATION SUMMARY ==========")

print("Total Tests:", total_tests)
print("Passed:", passed)
print("Failed:", failed)
print("Success Rate:", round(success_rate, 2), "%")

if failed == 0:
    print("\nAll evaluation tests passed!")
else:
    print("\nSome tests failed. Please review the errors.")
