# Task Analysis Project

## Overview
This project is a **Task Analysis System** built with **Django** for the backend and **HTML, CSS, and JavaScript** for the frontend. It allows users to perform task analysis and computes scores using a custom scoring algorithm.  

---

## Features
- Simple and responsive frontend interface
- Backend powered by Django
- Scoring algorithm implemented in Python
- Unit tests for validating the scoring algorithm

---

## Project Structure
project-root/
│
├── backend/ # Django backend code
│ ├── manage.py
│ ├── app/ # Django app containing models, views, urls
│ └── ...
│
├── templates/ # Frontend HTML templates
│ ├── index.html
│ └── ...
│
├── static/ # CSS and JavaScript files
│ ├── css/
│ └── js/
│
├── tests/ # Unit tests for scoring algorithm
│ └── test_scoring.py
│
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-root>
Create a Virtual Environment
python -m venv venv
Activate the Virtual Environment
Windows
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Start the Server
python manage.py runserver

### Algorithm Explanation

The scoring algorithm calculates the task score based on predefined criteria. The implementation ensures accurate computation and handles edge cases. Unit tests are included to verify correctness.
Dependencies

Python 3.13+

Django

Any other dependencies listed in requirements.txt
