# FitForge — Fitness Recommendation System

A complete API-based ML integration project featuring:
- **FastAPI** backend with a rule-based recommendation engine
- **Personalized workout plans** based on goal, experience, and availability
- **Nutrition targets** using Mifflin-St Jeor BMR + TDEE calculations
- **Polished frontend** with real-time plan generation
- **Git version control** workflow

---

## Project Structure

```
fitness-api/
├── backend/
│   ├── main.py            # FastAPI app — recommendation engine + all routes
│   └── requirements.txt
├── frontend/
│   └── index.html         # Single-file UI (no build step)
└── README.md
```

---

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Frontend

Open `frontend/index.html` in your browser.

---

## API Endpoints

| Method | Endpoint              | Description                          |
|--------|-----------------------|--------------------------------------|
| GET    | `/`                   | Root status                          |
| GET    | `/health`             | Health check + uptime                |
| GET    | `/docs`               | Swagger UI (auto-generated)          |
| POST   | `/api/v1/recommend`   | Full personalized fitness plan       |
| GET    | `/api/v1/goals`       | List available fitness goals         |
| GET    | `/api/v1/equipment`   | List supported equipment options     |

---

## Example Request

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
    "equipment": ["dumbbells", "barbell", "pull_up_bar"],
    "health_conditions": []
  }'
```

**Response includes:**
- `metrics` — BMI, BMR, TDEE, target calories, ideal weight range
- `weekly_plan` — day-by-day workouts with exercises, sets, reps, rest, tips
- `nutrition` — macros, calorie target, hydration, foods to eat/avoid, meal timing
- `lifestyle_tips` — 5 goal-specific coaching tips
- `estimated_results` — realistic outcome description
- `processing_time_ms` — model inference time

---

## ML / Recommendation Logic

The engine uses:
- **Mifflin-St Jeor formula** — accurate BMR for males and females
- **Harris-Benedict activity multipliers** — TDEE from lifestyle input
- **Goal-based calorie adjustment** — deficit for loss, surplus for gain
- **Macro partitioning** — protein-first for muscle/loss, carb-first for endurance
- **Progressive exercise selection** — different DB per goal × experience level
- **Hamwi ideal weight formula** — personalized healthy weight range

To swap in a real ML model (e.g. collaborative filtering or neural net), replace the `recommend()` function — the API schema stays identical.

---

## Git Workflow

```bash
git init
git add .
git commit -m "feat: initial fitness recommendation system"

git checkout -b feature/add-ml-model
# ... integrate scikit-learn or pytorch model ...
git commit -m "feat: replace rule engine with trained classifier"
git push origin feature/add-ml-model
```
