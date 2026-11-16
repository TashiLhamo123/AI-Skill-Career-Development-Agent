
import ollama


def generate_career_advice(career, current_skills, missing_skills):
    prompt = f"""
    You are an AI career development assistant.

    Student's career goal: {career}
    Student's current skills: {current_skills}
    Skills the student needs to improve: {missing_skills}

    Provide:
    1. Why this career may suit the student.
    2. How the student can improve their missing skills.
    3. Three practical learning suggestions.

    Use simple English and give personalized advice.
    """

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Unable to generate AI advice. Please check Ollama is running. Error: {e}"
