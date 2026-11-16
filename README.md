# AI-Powered Skill Gap and Career Development Agent

## 1. Project Overview

The AI-Powered Skill Gap and Career Development Agent is a Python-based application designed to help students identify their skill gaps and plan their career development.

The agent analyzes students' current skills based on their selected career goals. It identifies missing skills, recommends suitable learning resources, and creates personalized learning roadmaps.

It also uses a local Large Language Model (LLM), Llama 3.2 1B, through Ollama to generate personalized career advice. The system stores student feedback and learning progress so that recommendations can be adjusted according to student preferences.

## 2. Objectives

- Identify skill gaps based on students' career goals.
- Recommend suitable career paths.
- Suggest learning resources for missing skills.
- Create personalized learning roadmaps.
- Generate AI-powered career guidance.
- Store student feedback and learning progress.
- Adapt recommendations based on student preferences.

## 3. Main Features

The application contains seven main sections:

- **Home:** Provides an introduction to the career development agent.
- **Student Profile:** Allows students to provide their career goals and current skills.
- **Skill Analysis:** Compares existing skills with the skills required for a selected career and identifies missing skills.
- **Careers:** Displays available career options from the career dataset.
- **Resources:** Recommends learning resources based on identified skill gaps.
- **Learning Roadmap:** Creates personalized learning plans for developing missing skills.
- **Feedback and Progress:** Stores student feedback and tracks course progress.

### Additional AI Features

- **AI-Powered Career Advice:** Uses the Llama 3.2 1B language model to generate personalized career guidance.
- **Skill-Based Personalization:** Generates advice based on the selected career goal, current skills, and missing skills.
- **Feedback Adaptation:** Adjusts course recommendations based on preferences such as short, practical, and beginner-level courses.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | User interface |
| Pandas | Dataset handling and analysis |
| SQLite | Storing feedback and learning progress |
| CSV | Storing career, skill and course datasets |
| Ollama | Running the local language model |
| Llama 3.2 1B | Generating AI-powered career advice |

## 5. Agent Architecture

The project follows a hybrid agent approach that combines data-driven and rule-based processing with local LLM integration.

The agent follows these steps:

1. **Perception:** Receives the student's current skills and selected career goal.
2. **Reasoning:** Compares the student's skills with the skills required for the selected career.
3. **Decision-making:** Identifies missing skills and selects suitable learning resources.
4. **Action:** Generates career recommendations and personalized learning roadmaps.
5. **AI Integration:** Uses Llama 3.2 1B through Ollama to generate personalized career advice.
6. **Memory:** Stores feedback and learning progress using SQLite.
7. **Adaptation:** Adjusts learning recommendations based on student feedback.

## 6. Project Structure

```text
Skill_Career_Agent/
│
├── app.py
├── agent.py
├── tools.py
├── planner.py
├── memory.py
├── feedback.py
├── database.py
├── llm_agent.py
├── evaluate.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── careers.csv
│   ├── skills.csv
│   └── courses.csv
│
└── career_agent.db
```

Note: The database file may be created automatically when the application runs. The virtual environment and downloaded Llama model are not included in the GitHub repository.

## 7. Installation and Setup

### Step 1: Install Python

Install Python 3.11 or a compatible version.

### Step 2: Install Ollama

Download and install Ollama from:

https://ollama.com/download

### Step 3: Download the Llama model

Open PowerShell and run:

```powershell
ollama pull llama3.2:1b
```

### Step 4: Open the project folder

Open PowerShell or the terminal inside the project folder.

### Step 5: Create a virtual environment

```bash
python -m venv venv
```

### Step 6: Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 7: Install required libraries

```bash
python -m pip install -r requirements.txt
```

### Step 8: Run the application

Make sure Ollama is running, then execute:

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

## 8. Running the Evaluation

To test the agent's performance, run:

```bash
python evaluate.py
```

The current evaluation contains eight test cases covering skill analysis, course recommendations, learning plans, feedback adaptation and error handling.

**Evaluation Result: 8 out of 8 tests passed (100% success rate).**

This result represents the success rate of the implemented test cases, not a guarantee of real-world recommendation accuracy.

## 9. Limitations

- The agent uses predefined datasets, so its recommendations are limited to the available information.
- Course links direct users to learning platforms rather than specific verified courses.
- Feedback adaptation uses predefined rules rather than a trained machine learning model.
- AI-generated advice may sometimes contain inaccurate or general recommendations.
- The local Llama model requires Ollama to be installed and running.
- Career recommendations are educational guidance and do not guarantee employment.

## 10. Future Improvements

- Integrate machine learning for more advanced career recommendations.
- Include more career options and learning resources.
- Connect to real course databases and external APIs.
- Improve progress tracking and performance analysis.
- Add more advanced personalization features.
- Explore Retrieval-Augmented Generation (RAG) for more context-based career guidance.

## 11. Conclusion

The AI-Powered Skill Gap and Career Development Agent helps students understand their current skills, identify areas for improvement and plan their career development.

By combining skill analysis, course recommendations, personalized learning roadmaps, memory, feedback adaptation and local LLM integration, the project provides a structured approach to personalized learning and career planning.