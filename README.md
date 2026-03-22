# 🏋️ FitForge — AI-Powered Fitness Recommendation System

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

A complete **API-Based ML Integration Project** that generates personalized fitness plans in real time. Built with FastAPI on the backend and a single-file HTML/CSS/JS frontend — no frameworks, no build steps.


## 📸 Project Overview

FitForge takes a user profile (age, weight, goal, equipment, experience) and returns a fully personalized:

- 📅 **Weekly workout plan** — exercises filtered strictly to your available equipment
- 🥗 **Nutrition protocol** — calories, macros, meal timing, foods to eat/avoid
- 📊 **Body metrics** — BMI, BMR, TDEE, ideal weight range
- 💡 **Lifestyle tips** — goal-specific coaching advice


## 🗂️ Project Structure

```
fitness-api/
├── backend/
│   ├── main.py            # FastAPI app — recommendation engine + all routes
│   └── requirements.txt   # Python dependencies (3 packages only)
├── frontend/
│   └── index.html         # Complete UI — no build step, open directly in browser
└── README.md
```


## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI 0.115 |
| Server | Uvicorn (ASGI) |
| Data Validation | Pydantic v2 |
| Frontend | HTML5 / CSS3 / Vanilla JS |
| Version Control | Git |
| Language | Python 3.12 |



## 🚀 Getting Started (Windows)

### Prerequisites
- Python 3.12 — download from [python.org](https://www.python.org/downloads/release/python-3129/)
- ✅ During install, check **"Add Python to PATH"**



### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/fitness-api.git
cd fitness-api
```



### Step 2 — Set Up the Backend

Open Command Prompt inside the `backend` folder:

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```



### Step 3 — Run the API Server

```cmd
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
```

> ⚠️ Keep this terminal open — the API runs here.



### Step 4 — Open the Frontend

Navigate to `frontend/` in File Explorer and **double-click `index.html`** — it opens directly in your browser.



### Step 5 — Use the App

1. Fill in your profile (name, age, weight, goal, etc.)
2. Click the equipment pills to select what you have available
3. Click **BUILD MY PLAN →**
4. Your personalized plan appears instantly



## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root — API status message |
| `GET` | `/health` | Health check + uptime |
| `GET` | `/docs` | Auto-generated Swagger UI |
| `POST` | `/api/v1/recommend` | Generate full personalized plan |
| `GET` | `/api/v1/goals` | List available fitness goals |
| `GET` | `/api/v1/equipment` | List supported equipment options |



## 📦 Example API Request

```bash
curl -X POST http://localhost:8000/api/v1/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex",
    "age": 28,
    "gender": "male",
    "weight_kg": 78,
    "height_cm": 175,
    "fitness_goal": "muscle_gain",
    "activity_level": "moderate",
    "experience_level": "intermediate",
    "available_days": 4,
    "equipment": ["dumbbells", "pull_up_bar"],
    "health_conditions": []
  }'
```

### Example Response

```json
{
  "user_name": "Alex",
  "fitness_goal": "muscle_gain",
  "selected_equipment": ["dumbbells", "pull_up_bar"],
  "metrics": {
    "bmi": 25.5,
    "bmi_category": "Normal",
    "bmr": 1847,
    "tdee": 2863,
    "target_calories": 3163,
    "ideal_weight_kg_range": "67–81 kg"
  },
  "weekly_plan": [
    {
      "day": "Monday",
      "focus": "Chest & Triceps",
      "duration_minutes": 65,
      "exercises": [
        {
          "name": "DB Incline Press",
          "sets": 4,
          "reps": "10 reps",
          "rest_seconds": 90,
          "muscle_group": "Upper Chest",
          "difficulty": "Medium",
          "tips": "30 degree incline, full ROM",
          "required_equipment": ["dumbbells"]
        }
      ],
      "warmup": ["5-min light jog or jumping jacks", "..."],
      "cooldown": ["3-min slow walk", "..."]
    }
  ],
  "nutrition": {
    "daily_calories": 3163,
    "protein_g": 172,
    "carbs_g": 310,
    "fat_g": 88,
    "hydration_liters": 2.9,
    "meal_timing": ["7:00 AM — Large carb + protein breakfast", "..."],
    "foods_to_eat": ["Beef, chicken, turkey", "..."],
    "foods_to_avoid": ["Excessive alcohol", "..."]
  },
  "lifestyle_tips": ["Progressive overload — increase weight 2.5–5% each week", "..."],
  "estimated_results": "With progressive overload, expect 1–2 kg lean muscle per month...",
  "processing_time_ms": 1.24
}
```



## 🧠 How the Recommendation Engine Works

### Equipment Filtering
Every exercise in the database is tagged with `required_equipment`. The filter strictly enforces:
- `required_equipment = []` → bodyweight, always shown regardless of selection
- `required_equipment = ["dumbbells"]` → only shown if user selected dumbbells
- If user selects **No Equipment**, only bodyweight exercises are returned

Tested across **165 combinations** (5 goals × 3 levels × 11 equipment scenarios) with zero leaks.

### Body Metrics Formulas

| Metric | Formula Used |
|---|---|
| BMI | weight(kg) / height(m)² |
| BMR | Mifflin-St Jeor equation |
| TDEE | BMR × activity multiplier |
| Target Calories | TDEE ± goal adjustment |
| Ideal Weight | Hamwi formula |

### Goal-Based Calorie Adjustments

| Goal | Calorie Adjustment |
|---|---|
| Weight Loss | TDEE − 500 kcal |
| Muscle Gain | TDEE + 300 kcal |
| Endurance | TDEE + 100 kcal |
| Flexibility | TDEE (maintenance) |
| General Fitness | TDEE (maintenance) |

### Exercise Database Size

- **5 fitness goals** × **3 experience levels** = 15 exercise pools
- Each pool contains **15–20 exercises** tagged by required equipment
- Equipment options: Dumbbells, Barbell, Resistance Bands, Pull-up Bar, Bench, Kettlebell, Treadmill, or None



## 🔧 Supported Fitness Goals

| Goal | Description |
|---|---|
| `weight_loss` | HIIT, cardio circuits, fat-burning workouts |
| `muscle_gain` | Progressive overload, compound lifts, hypertrophy |
| `endurance` | Aerobic base, interval training, long steady-state cardio |
| `flexibility` | Yoga flows, mobility drills, static stretching |
| `general_fitness` | Balanced mix of strength, cardio, and mobility |



## 🏗️ Supported Equipment

| Value to send in API | Display Name |
|---|---|
| `dumbbells` | Dumbbells |
| `barbell` | Barbell |
| `resistance_bands` | Resistance Bands |
| `pull_up_bar` | Pull-up Bar |
| `bench` | Bench |
| `kettlebell` | Kettlebell |
| `treadmill` | Treadmill |
| `none` | No Equipment (bodyweight only) |



## 🔁 Daily Usage

Every time you want to run the project:

```cmd
cd fitness-api\backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

Then open `frontend\index.html` in your browser.



## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `python` not recognized | Reinstall Python 3.12 with "Add to PATH" checked |
| `venv\Scripts\activate` fails | Run PowerShell as Admin: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Frontend says "Cannot reach backend" | Make sure `uvicorn` is running in a separate CMD window |
| Port 8000 already in use | Use `--port 8001` and update `const API` in `index.html` |
| `pydantic-core` build error | You are on Python 3.13/3.14 — switch to Python 3.12 |



## 🔌 Extending the Project

| Idea | How to implement |
|---|---|
| Real ML model | Replace `recommend()` in `main.py` with a scikit-learn or HuggingFace pipeline |
| Save user history | Add SQLite with `databases` + `aiosqlite` |
| User authentication | Add `fastapi-users` or API key header middleware |
| Deploy online | Dockerize and deploy to [Railway](https://railway.app) or [Render](https://render.com) |
| Add tests | Use `pytest` + `httpx` for API integration tests |
| Progress tracking | Add a `/progress` endpoint that stores and compares weekly results |



## 🌿 Git Workflow

```bash
# Initial setup
git init
git add .
git commit -m "feat: initial fitness recommendation system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fitness-api.git
git push -u origin main

# Feature branch workflow
git checkout -b feature/add-ml-model
# make your changes
git add .
git commit -m "feat: integrate trained recommendation model"
git push origin feature/add-ml-model
```
