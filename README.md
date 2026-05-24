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

1. **Patient Registration**
   - The physiotherapist creates the patient profile and records clinical information, including the affected limb.

2. **Initial Assessment**
   - The patient completes a guided assessment session while the system captures movement through the camera.

3. **Motion Analysis**
   - MediaPipe detects body and hand landmarks and calculates joint angles and range of motion (ROM) in real time.

4. **Adaptive Rehabilitation**
   - The patient performs rehabilitation exercises through interactive games where physical movements control in-game actions.

5. **Performance Evaluation**
   - The system evaluates movement quality, ROM achievement, accuracy, and consistency to generate performance scores.

6. **Progress Tracking**
   - Session results and rehabilitation metrics are stored and visualized through the clinician dashboard for historical analysis.

7. **Clinical Monitoring**
   - Physiotherapists review patient progress and adjust rehabilitation plans based on objective performance data.

---
---
---
#### *notes to the team:
## Befor you start working on the project
1) First go to file that contain you git copy path 
2) Open cmd write cd paste path here
3) Git pull
4) DO NOT forget to git push after you finish!
-----
## Database Setup (SQLite_web)

This project uses **SQLite** as the database and **sqlite_web** to provide a simple web interface for viewing and managing the database.

### 1. Install SQLite_web

> This step is done only once during initial setup.

Run the following command in your terminal:

```bash
pip install sqlite-web
```

### 2. Run SQLite_web

To start the web interface for your database, run this line in vscode:

```bash
sqlite_web database.db
```

The interface will be available at:

```
http://127.0.0.1:8080
```

### 3. View the DataBase inside VScode:

ctrl + shift + p 🡢 sqlite: open database 🡢 choose database
