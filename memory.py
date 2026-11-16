
import sqlite3
import os
import json

# Database location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "career_agent.db")


# Connect to SQLite database
def connect_db():
    return sqlite3.connect(DB_PATH)


# Create database tables
def initialize_memory():

    connection = connect_db()
    cursor = connection.cursor()

    # Store student profile and skills
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career_goal TEXT,
            skills TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Store student feedback
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# Save student information
def save_student_memory(career_goal, skills):

    connection = connect_db()
    cursor = connection.cursor()

    skills_json = json.dumps(skills)

    cursor.execute("""
        INSERT INTO student_memory (career_goal, skills)
        VALUES (?, ?)
    """, (career_goal, skills_json))

    connection.commit()
    connection.close()


# Retrieve previous student information
def get_student_memory():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT career_goal, skills, updated_at
        FROM student_memory
        ORDER BY id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()
    connection.close()

    if result:
        return {
            "career_goal": result[0],
            "skills": json.loads(result[1]),
            "updated_at": result[2]
        }

    return None


# Save student feedback
def save_feedback(feedback_text):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback (feedback_text)
        VALUES (?)
    """, (feedback_text,))

    connection.commit()
    connection.close()


# Retrieve previous feedback
def get_feedback():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT feedback_text, created_at
        FROM feedback
        ORDER BY id DESC
    """)

    results = cursor.fetchall()
    connection.close()

    return results


# Test memory system
if __name__ == "__main__":

    initialize_memory()

    print("========== TESTING AGENT MEMORY ==========")

    # Save sample student information
    save_student_memory(
        "Data Analyst",
        ["Python", "SQL", "Excel"]
    )

    print("\nStudent information saved successfully!")

    # Retrieve saved information
    student = get_student_memory()

    print("\n========== RETRIEVED STUDENT MEMORY ==========")
    print(student)

    # Save sample feedback
    save_feedback("I want more practical Python courses.")

    print("\nFeedback saved successfully!")

    # Retrieve feedback
    print("\n========== PREVIOUS FEEDBACK ==========")

    for feedback in get_feedback():
        print(feedback)

    print("\nAgent memory system working successfully!")


# Save or update course progress
def save_course_progress(course_name, status):
    initialize_memory()

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT UNIQUE,
            status TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO course_progress (course_name, status)
        VALUES (?, ?)
        ON CONFLICT(course_name)
        DO UPDATE SET
            status = excluded.status,
            updated_at = CURRENT_TIMESTAMP
    """, (course_name, status))

    connection.commit()
    connection.close()


# Retrieve saved course progress
def get_course_progress():
    initialize_memory()

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT UNIQUE,
            status TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        SELECT course_name, status, updated_at
        FROM course_progress
        ORDER BY updated_at DESC
    """)

    progress = cursor.fetchall()
    connection.close()

    return progress

