# Snap Class — AI Classroom Management Platform

## Overview

Snap Class is an AI-powered classroom management platform that uses face and voice recognition for user identification and authentication.

The project aims to simplify classroom workflows by integrating recognition systems with role-based dashboards and attendance automation.

Current development status: Active Development 🚧

---

## Features

### Completed

* Face Recognition Pipeline
* Voice Recognition Pipeline
* Student Registration
* Student Login
* Teacher Registration
* Teacher Login
* Home Screen UI
* Teacher UI

### In Progress

* Teacher Dashboard
* Attendance Marking System
* Student Dashboard

---

## Tech Stack

Frontend:

* Streamlit

Backend:

* Python

Machine Learning:

* Face Recognition
* Voice Recognition
* scikit-learn

Database:

* Supabase

---

## Project Structure

```text
src/
├── authentication/
├── recognition/
│   ├── face/
│   └── voice/
├── dashboard/
├── database/
├── ui/
└── utils/
```

---

## Workflow

1. User registers
2. User logs in
3. Identity verification through recognition pipelines
4. Dashboard access
5. Attendance management (Upcoming)
---

## Future Improvements

* Real-time attendance marking
* Student dashboard
* Analytics dashboard
* Recognition accuracy improvements
* Deployment

---

## Installation

```bash
git clone <repo-link>

cd snap-class

pip install -r requirements.txt

streamlit run app.py
```

---

## Author

Tarush Singla
