
import pandas as pd
import os

# Get the project folder location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load career dataset
careers = pd.read_csv(os.path.join(BASE_DIR, "data", "careers.csv"))

# Load skills dataset
skills = pd.read_csv(os.path.join(BASE_DIR, "data", "skills.csv"))

# Load courses dataset
courses = pd.read_csv(os.path.join(BASE_DIR, "data", "courses.csv"))


# Display dataset information
print("\n========== CAREER DATASET ==========")
print(careers.head())

print("\n========== SKILLS DATASET ==========")
print(skills.head())

print("\n========== COURSES DATASET ==========")
print(courses.head())


# Display total records
print("\n========== DATASET SUMMARY ==========")
print("Total careers:", len(careers))
print("Total skills:", len(skills))
print("Total courses:", len(courses))

print("\nAll datasets loaded successfully!")
