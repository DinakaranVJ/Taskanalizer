# Task Analysis Project

## Overview
This project is a **Task Analysis System** built with **Django** for the backend and **HTML, CSS, and JavaScript** for the frontend. It allows users to perform task analysis and calculates priority scores using a custom scoring algorithm. The system is designed to be simple, modular, and easy to extend.  

The repository contains:  
- Complete Django backend code  
- Frontend files (HTML, CSS, JavaScript)  
- `requirements.txt` for Python dependencies  
- Unit tests for the scoring algorithm  
- README with setup instructions  

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-root>

2. Create a Virtual Environment
python -m venv venv

3. Activate the Virtual Environment

Windows

venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Run Migrations
python manage.py migrate

6. Start the Server
python manage.py runserver

Open your browser and navigate to http://127.0.0.1:8000 to access the application.

7. Run Unit Tests

To test the scoring algorithm:

python manage.py test tests/

Algorithm Explanation

The priority scoring algorithm is designed to evaluate tasks based on multiple criteria, including urgency, complexity, and impact. Each task is assigned a numerical value for each criterion:

Urgency – How time-sensitive the task is. A task with a near deadline receives a higher score.

Complexity – Tasks that require more effort or multiple steps have higher complexity scores.

Impact – Tasks that affect multiple stakeholders or critical business functions get higher impact scores.

The algorithm computes a weighted sum of these scores to produce a final priority value. For example, urgency may be weighted at 40%, complexity at 30%, and impact at 30%. The final score is then normalized to ensure comparability across all tasks.

Additional considerations in the algorithm:

Tasks with missing values are given a default score to prevent errors.

Scores are updated dynamically whenever task attributes change.

Unit tests ensure accuracy for edge cases, such as tasks with zero urgency or extremely high complexity.

This design ensures that tasks are prioritized efficiently and fairly, enabling users to focus on the most critical work first.

Design Decisions

Backend Framework: Django was chosen for its robust ORM, built-in admin, and scalability.

Frontend: Simple HTML, CSS, and JavaScript were used to reduce dependencies and keep the UI lightweight.

Scoring Logic: Weighted sum method was preferred over more complex algorithms for transparency and ease of testing.

Trade-offs: Advanced UI frameworks (React/Vue) were skipped to focus on core functionality and scoring logic.

Time Breakdown
Section	Time Spent
Project Setup & Django Configuration	3 hours
Frontend Development	5 hours
Scoring Algorithm Implementation	4 hours
Unit Tests Creation	2 hours
Documentation & README	2 hours
Total	16 hours
Bonus Challenges

Implemented unit tests for all edge cases in the scoring algorithm.

Ensured frontend is responsive and mobile-friendly.

Future Improvements

Integrate a database dashboard to visualize task scores and priorities.

Add user authentication and role-based access for task management.

Implement a more sophisticated scoring algorithm using machine learning to predict task priority dynamically.

Add filters and sorting options in the frontend for better task management.


