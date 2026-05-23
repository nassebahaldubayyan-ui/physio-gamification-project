# Gamified Physiotherapy: An Interactive Rehabilitation System Using AI and Motion Tracking for Brachial Plexus Injury

## Overview
Brachial Plexus Injuries (BPI) can significantly impact upper-limb mobility and often require long-term, repetitive rehabilitation programs. To enhance patient engagement and improve rehabilitation outcomes, this project introduces an intelligent and adaptive rehabilitation system that transforms therapeutic exercises into interactive game-based activities powered by Artificial Intelligence.
The system utilizes real-time motion tracking and AI-driven performance analysis to adapt exercise difficulty according to the patient's capabilities. In addition, a comprehensive medical dashboard enables physiotherapists to monitor patient progress and access data-driven insights that support informed clinical decision-making.
By combining gamification, artificial intelligence, motion tracking, and remote supervision, the platform delivers a smart, engaging, and effective rehabilitation experience for both patients and healthcare professionals.

---

## Technology Stack

| Category | Technologies |
|----------|-------------|
| Backend | Django, Python |
| Frontend | HTML, CSS, JavaScript |
| Computer Vision & AI | MediaPipe, JavaScript |
| Games | Unity |
| Database | SQLite |

---

## How It Works

1. The patient starts a rehabilitation game.
2. The system activates the camera and begins tracking upper-limb movements.
3. MediaPipe extracts pose and hand landmarks in real time.
4. The AI engine analyzes movement quality and calculates rehabilitation metrics.
5. The system provides immediate feedback when incorrect movement patterns are detected.
6. Based on performance, the adaptive system adjusts difficulty and determines whether the patient can progress to the next level or should repeat the current one.
7. Session results and performance metrics are stored in the database.
8. Physiotherapists can review progress through the medical dashboard.

---
#### *notes to the team:
## befor you start working on the project
1) first go to file that contain you git copy path 
2) open cmd write cd paste path here
3) git pull
4) DO NOT forget to git push after you finish!
-----
## Database Setup (SQLite_web)

This project uses **SQLite** as the database and **sqlite_web** to provide a simple web interface for viewing and managing the database.

## 1. Install SQLite_web

> This step is done only once during initial setup.

Run the following command in your terminal:

```bash
pip install sqlite-web
```

## 2. Run SQLite_web

To start the web interface for your database, run this line in vscode:

```bash
sqlite_web database.db
```

The interface will be available at:

```
http://127.0.0.1:8080
```

## 3. View the DataBase inside VScode:

ctrl + shift + p 🡢 sqlite: open database 🡢 choose database

# to activate environment for website and run django
1) venv\Scripts\activate
2) python manage.py runserver 
