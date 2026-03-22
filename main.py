"""
Fitness Recommendation System API
FastAPI Backend — Version 2.0.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import time, random

app = FastAPI(title="Fitness Recommendation API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
START_TIME = time.time()

# ── Schemas ───────────────────────────────────────────────────────────────────
class UserProfile(BaseModel):
    name: str
    age: int = Field(..., ge=13, le=90)
    gender: str = Field(..., pattern="^(male|female|other)$")
    weight_kg: float = Field(..., gt=20, lt=300)
    height_cm: float = Field(..., gt=100, lt=250)
    fitness_goal: str = Field(..., pattern="^(weight_loss|muscle_gain|endurance|flexibility|general_fitness)$")
    activity_level: str = Field(..., pattern="^(sedentary|light|moderate|active|very_active)$")
    experience_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    available_days: int = Field(..., ge=1, le=7)
    equipment: list[str] = Field(default=[])
    health_conditions: list[str] = Field(default=[])

class Exercise(BaseModel):
    name: str
    sets: int
    reps: str
    rest_seconds: int
    muscle_group: str
    difficulty: str
    tips: str
    required_equipment: list[str] = Field(default=[])

class WorkoutDay(BaseModel):
    day: str
    focus: str
    duration_minutes: int
    exercises: list[Exercise]
    warmup: list[str]
    cooldown: list[str]

class NutritionPlan(BaseModel):
    daily_calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    meal_timing: list[str]
    foods_to_eat: list[str]
    foods_to_avoid: list[str]
    hydration_liters: float

class Metrics(BaseModel):
    bmi: float
    bmi_category: str
    bmr: int
    tdee: int
    target_calories: int
    ideal_weight_kg_range: str

class RecommendationResponse(BaseModel):
    user_name: str
    fitness_goal: str
    selected_equipment: list[str]
    metrics: Metrics
    weekly_plan: list[WorkoutDay]
    nutrition: NutritionPlan
    lifestyle_tips: list[str]
    estimated_results: str
    processing_time_ms: float


# ── Exercise Database ─────────────────────────────────────────────────────────
# required_equipment=[]  →  bodyweight, always available
# required_equipment=["dumbbells"]  →  only shown if user has dumbbells
# etc.

ALL_EXERCISES = {

  # ════════════════════════════════════════════════════════
  # WEIGHT LOSS
  # ════════════════════════════════════════════════════════
  "weight_loss": {
    "beginner": [
      # ── bodyweight ──
      Exercise(name="Jumping Jacks",         sets=3, reps="30 reps",       rest_seconds=30, muscle_group="Full Body",      difficulty="Easy",   tips="Land softly, keep a steady rhythm",                       required_equipment=[]),
      Exercise(name="Bodyweight Squats",     sets=3, reps="15 reps",       rest_seconds=45, muscle_group="Legs",           difficulty="Easy",   tips="Chest up, knees track over toes",                         required_equipment=[]),
      Exercise(name="Knee Push-ups",         sets=3, reps="10 reps",       rest_seconds=45, muscle_group="Chest/Arms",     difficulty="Easy",   tips="Keep core tight, full range of motion",                   required_equipment=[]),
      Exercise(name="Mountain Climbers",     sets=3, reps="20 reps",       rest_seconds=30, muscle_group="Core/Cardio",    difficulty="Easy",   tips="Keep hips level, drive knees to chest",                   required_equipment=[]),
      Exercise(name="High Knees",            sets=3, reps="30 seconds",    rest_seconds=30, muscle_group="Cardio",         difficulty="Easy",   tips="Pump arms, keep core engaged",                            required_equipment=[]),
      Exercise(name="Glute Bridges",         sets=3, reps="15 reps",       rest_seconds=30, muscle_group="Glutes",         difficulty="Easy",   tips="Squeeze glutes hard at the top",                          required_equipment=[]),
      Exercise(name="Step-ups",              sets=3, reps="12 each leg",   rest_seconds=30, muscle_group="Legs/Glutes",    difficulty="Easy",   tips="Drive through the heel, stand tall at top",               required_equipment=[]),
      Exercise(name="Wall Sit",              sets=3, reps="30 seconds",    rest_seconds=30, muscle_group="Legs",           difficulty="Easy",   tips="Thighs parallel to floor, back flat on wall",             required_equipment=[]),
      # ── dumbbells ──
      Exercise(name="Dumbbell Swings",       sets=3, reps="15 reps",       rest_seconds=40, muscle_group="Full Body",      difficulty="Easy",   tips="Hinge at hips, drive with glutes not arms",               required_equipment=["dumbbells"]),
      Exercise(name="DB Squat to Press",     sets=3, reps="12 reps",       rest_seconds=45, muscle_group="Full Body",      difficulty="Easy",   tips="Press at top of squat for one fluid movement",            required_equipment=["dumbbells"]),
      Exercise(name="DB Lateral Raise",      sets=3, reps="12 reps",       rest_seconds=30, muscle_group="Shoulders",      difficulty="Easy",   tips="Lead with elbows, control the descent",                   required_equipment=["dumbbells"]),
      # ── resistance bands ──
      Exercise(name="Band Squat",            sets=3, reps="15 reps",       rest_seconds=30, muscle_group="Legs",           difficulty="Easy",   tips="Band under feet, hold at chest height",                   required_equipment=["resistance_bands"]),
      Exercise(name="Band Row",              sets=3, reps="15 reps",       rest_seconds=30, muscle_group="Back",           difficulty="Easy",   tips="Pull elbows back, squeeze shoulder blades",               required_equipment=["resistance_bands"]),
      # ── pull-up bar ──
      Exercise(name="Dead Hang",             sets=3, reps="20 seconds",    rest_seconds=30, muscle_group="Grip/Back",      difficulty="Easy",   tips="Relax shoulders down, breathe steadily",                  required_equipment=["pull_up_bar"]),
      # ── kettlebell ──
      Exercise(name="KB Deadlift",           sets=3, reps="12 reps",       rest_seconds=45, muscle_group="Hamstrings/Glutes", difficulty="Easy", tips="Hinge at hip, keep chest up",                           required_equipment=["kettlebell"]),
    ],
    "intermediate": [
      Exercise(name="Burpees",               sets=4, reps="12 reps",       rest_seconds=45, muscle_group="Full Body",      difficulty="Medium", tips="Explosive jump, controlled descent",                      required_equipment=[]),
      Exercise(name="Jump Squats",           sets=3, reps="15 reps",       rest_seconds=45, muscle_group="Legs/Cardio",    difficulty="Medium", tips="Soft landing, full squat depth",                          required_equipment=[]),
      Exercise(name="Push-ups",              sets=4, reps="15 reps",       rest_seconds=45, muscle_group="Chest/Arms",     difficulty="Medium", tips="Straight body line, chest to floor",                      required_equipment=[]),
      Exercise(name="Plank",                 sets=3, reps="45 seconds",    rest_seconds=30, muscle_group="Core",           difficulty="Medium", tips="Neutral spine, don't let hips sag",                       required_equipment=[]),
      Exercise(name="Lateral Shuffles",      sets=3, reps="30 seconds",    rest_seconds=30, muscle_group="Cardio/Legs",    difficulty="Medium", tips="Stay low in an athletic stance, quick feet",              required_equipment=[]),
      Exercise(name="Reverse Lunges",        sets=3, reps="12 each leg",   rest_seconds=40, muscle_group="Legs/Glutes",    difficulty="Medium", tips="Step back, back knee hovers just above floor",            required_equipment=[]),
      Exercise(name="Tricep Dips",           sets=3, reps="12 reps",       rest_seconds=40, muscle_group="Triceps",        difficulty="Medium", tips="Elbows point back, lower until 90 degrees",               required_equipment=[]),
      # ── dumbbells ──
      Exercise(name="DB Thrusters",          sets=3, reps="12 reps",       rest_seconds=45, muscle_group="Full Body",      difficulty="Medium", tips="Squat deep, press overhead in one explosive motion",      required_equipment=["dumbbells"]),
      Exercise(name="DB Renegade Row",       sets=3, reps="8 each arm",    rest_seconds=60, muscle_group="Back/Core",      difficulty="Medium", tips="Minimal hip rotation, brace core hard",                   required_equipment=["dumbbells"]),
      Exercise(name="DB Step-up Press",      sets=3, reps="10 each leg",   rest_seconds=45, muscle_group="Legs/Shoulders", difficulty="Medium", tips="Step up and press simultaneously",                        required_equipment=["dumbbells"]),
      # ── resistance bands ──
      Exercise(name="Band Kickbacks",        sets=3, reps="15 each leg",   rest_seconds=30, muscle_group="Glutes",         difficulty="Medium", tips="Keep hips square, squeeze at full extension",             required_equipment=["resistance_bands"]),
      Exercise(name="Band Bicycle Crunch",   sets=3, reps="20 reps",       rest_seconds=30, muscle_group="Core",           difficulty="Medium", tips="Band around feet for resistance, slow and controlled",    required_equipment=["resistance_bands"]),
      # ── kettlebell ──
      Exercise(name="KB Swings",             sets=4, reps="15 reps",       rest_seconds=40, muscle_group="Posterior Chain", difficulty="Medium", tips="Explosive hip hinge, arms guide not lift",              required_equipment=["kettlebell"]),
      Exercise(name="KB Goblet Squat",       sets=3, reps="15 reps",       rest_seconds=45, muscle_group="Legs",           difficulty="Medium", tips="Elbows inside knees at bottom, chest tall",               required_equipment=["kettlebell"]),
      # ── pull-up bar ──
      Exercise(name="Hanging Knee Raises",   sets=3, reps="12 reps",       rest_seconds=45, muscle_group="Core",           difficulty="Medium", tips="Control the swing, squeeze abs at top",                   required_equipment=["pull_up_bar"]),
      # ── treadmill ──
      Exercise(name="Treadmill Intervals",   sets=6, reps="1min fast/1min slow", rest_seconds=0, muscle_group="Cardio",   difficulty="Medium", tips="Incline 1-2%, push hard on the fast intervals",           required_equipment=["treadmill"]),
    ],
    "advanced": [
      Exercise(name="Tabata Sprints",        sets=8, reps="20s on/10s off", rest_seconds=60, muscle_group="Cardio",        difficulty="Hard",   tips="Max effort every single interval",                        required_equipment=[]),
      Exercise(name="Pistol Squats",         sets=3, reps="8 each leg",    rest_seconds=60, muscle_group="Legs",           difficulty="Hard",   tips="Use a wall for balance if needed",                        required_equipment=[]),
      Exercise(name="Plyometric Push-ups",   sets=4, reps="10 reps",       rest_seconds=60, muscle_group="Chest/Power",    difficulty="Hard",   tips="Explosive push, controlled catch",                        required_equipment=[]),
      Exercise(name="Bear Crawl",            sets=3, reps="30 meters",     rest_seconds=45, muscle_group="Full Body",      difficulty="Hard",   tips="Keep hips low, opposite arm/leg move together",           required_equipment=[]),
      Exercise(name="Russian Twists",        sets=4, reps="20 reps",       rest_seconds=30, muscle_group="Core",           difficulty="Hard",   tips="Feet elevated, rotate fully each side",                   required_equipment=[]),
      Exercise(name="Box Jumps",             sets=4, reps="10 reps",       rest_seconds=60, muscle_group="Legs/Power",     difficulty="Hard",   tips="Soft landing, step down don't jump down",                 required_equipment=[]),
      # ── dumbbells ──
      Exercise(name="DB Man-makers",         sets=3, reps="8 reps",        rest_seconds=75, muscle_group="Full Body",      difficulty="Hard",   tips="Push-up, row each arm, squat, press — one fluid sequence",required_equipment=["dumbbells"]),
      Exercise(name="DB Bulgarian Split Squat", sets=4, reps="10 each leg", rest_seconds=60, muscle_group="Legs/Glutes",   difficulty="Hard",  tips="Rear foot elevated, front shin stays vertical",           required_equipment=["dumbbells"]),
      # ── barbell ──
      Exercise(name="Barbell Clean & Press", sets=4, reps="8 reps",        rest_seconds=90, muscle_group="Full Body",      difficulty="Hard",   tips="Explosive pull from floor, catch at shoulder, press up",  required_equipment=["barbell"]),
      Exercise(name="Barbell Back Squat",    sets=4, reps="8 reps",        rest_seconds=90, muscle_group="Legs/Full Body", difficulty="Hard",   tips="Bar on traps, brace core, squat below parallel",          required_equipment=["barbell"]),
      # ── kettlebell ──
      Exercise(name="KB Clean & Press",      sets=4, reps="8 each arm",    rest_seconds=75, muscle_group="Full Body",      difficulty="Hard",   tips="Clean to rack position, press overhead",                  required_equipment=["kettlebell"]),
      # ── pull-up bar ──
      Exercise(name="Muscle-ups",            sets=3, reps="5 reps",        rest_seconds=90, muscle_group="Back/Chest",     difficulty="Hard",   tips="Explosive pull, transition above bar",                    required_equipment=["pull_up_bar"]),
      # ── treadmill ──
      Exercise(name="Treadmill Hill Sprints", sets=6, reps="45s sprint/90s walk", rest_seconds=0, muscle_group="Cardio",  difficulty="Hard",   tips="Incline 8-12%, max effort on sprints",                    required_equipment=["treadmill"]),
    ],
  },

  # ════════════════════════════════════════════════════════
  # MUSCLE GAIN
  # ════════════════════════════════════════════════════════
  "muscle_gain": {
    "beginner": [
      Exercise(name="Push-ups",              sets=3, reps="12 reps",       rest_seconds=60, muscle_group="Chest/Triceps",  difficulty="Easy",   tips="Full range of motion, 2-second descent",                  required_equipment=[]),
      Exercise(name="Bodyweight Squats",     sets=3, reps="15 reps",       rest_seconds=60, muscle_group="Legs",           difficulty="Easy",   tips="Sit back into squat, chest stays up",                     required_equipment=[]),
      Exercise(name="Glute Bridges",         sets=3, reps="15 reps",       rest_seconds=45, muscle_group="Glutes",         difficulty="Easy",   tips="Squeeze hard at the top, hold 1 second",                  required_equipment=[]),
      Exercise(name="Tricep Dips",           sets=3, reps="10 reps",       rest_seconds=60, muscle_group="Triceps",        difficulty="Easy",   tips="Elbows point back, lower to 90 degrees",                  required_equipment=[]),
      Exercise(name="Inverted Rows",         sets=3, reps="10 reps",       rest_seconds=60, muscle_group="Back/Biceps",    difficulty="Easy",   tips="Keep body straight, pull chest to bar",                   required_equipment=[]),
      # ── dumbbells ──
      Exercise(name="DB Bench Press",        sets=3, reps="10-12 reps",    rest_seconds=90, muscle_group="Chest",          difficulty="Easy",   tips="Control the descent, slight arch in back",                required_equipment=["dumbbells"]),
      Exercise(name="DB Bent-over Row",      sets=3, reps="10-12 reps",    rest_seconds=90, muscle_group="Back",           difficulty="Easy",   tips="Lead with elbow, squeeze shoulder blade at top",          required_equipment=["dumbbells"]),
      Exercise(name="Goblet Squat",          sets=3, reps="12 reps",       rest_seconds=90, muscle_group="Legs",           difficulty="Easy",   tips="Elbows inside knees at bottom, chest tall",               required_equipment=["dumbbells"]),
      Exercise(name="DB Shoulder Press",     sets=3, reps="10 reps",       rest_seconds=90, muscle_group="Shoulders",      difficulty="Easy",   tips="Don't lock out at top, keep tension",                     required_equipment=["dumbbells"]),
      Exercise(name="DB Bicep Curl",         sets=3, reps="12 reps",       rest_seconds=60, muscle_group="Biceps",         difficulty="Easy",   tips="No swinging, fully supinate at top",                      required_equipment=["dumbbells"]),
      Exercise(name="DB Tricep Kickback",    sets=3, reps="12 reps",       rest_seconds=60, muscle_group="Triceps",        difficulty="Easy",   tips="Upper arm parallel to floor, full extension",             required_equipment=["dumbbells"]),
      Exercise(name="DB Lateral Raise",      sets=3, reps="12 reps",       rest_seconds=60, muscle_group="Shoulders",      difficulty="Easy",   tips="Lead with elbows, slight forward lean",                   required_equipment=["dumbbells"]),
      # ── barbell ──
      Exercise(name="Barbell Squat",         sets=4, reps="8-10 reps",     rest_seconds=120, muscle_group="Legs/Full Body",difficulty="Easy",   tips="Bar on traps, brace core, squat to parallel",             required_equipment=["barbell"]),
      Exercise(name="Barbell Romanian DL",   sets=3, reps="10 reps",       rest_seconds=120, muscle_group="Hamstrings",    difficulty="Easy",   tips="Push hips back, soft knee, bar stays close",              required_equipment=["barbell"]),
      Exercise(name="Barbell Bench Press",   sets=4, reps="8-10 reps",     rest_seconds=120, muscle_group="Chest",         difficulty="Easy",   tips="Arch back, feet flat, bar to lower chest",                required_equipment=["barbell"]),
      Exercise(name="Barbell Overhead Press",sets=3, reps="8-10 reps",     rest_seconds=90,  muscle_group="Shoulders",     difficulty="Easy",   tips="Squeeze glutes and core throughout",                      required_equipment=["barbell"]),
      # ── pull-up bar ──
      Exercise(name="Pull-ups",              sets=3, reps="5-8 reps",      rest_seconds=90, muscle_group="Back/Biceps",    difficulty="Easy",   tips="Full dead hang start, chest to bar",                      required_equipment=["pull_up_bar"]),
      Exercise(name="Chin-ups",              sets=3, reps="5-8 reps",      rest_seconds=90, muscle_group="Biceps/Back",    difficulty="Easy",   tips="Underhand grip, think elbows to hips",                    required_equipment=["pull_up_bar"]),
      # ── resistance bands ──
      Exercise(name="Band Pull-apart",       sets=3, reps="20 reps",       rest_seconds=30, muscle_group="Rear Delts",     difficulty="Easy",   tips="Arms straight, controlled return",                        required_equipment=["resistance_bands"]),
      Exercise(name="Band Face Pull",        sets=3, reps="15 reps",       rest_seconds=30, muscle_group="Rear Delts",     difficulty="Easy",   tips="Pull to forehead, external rotate at end",                required_equipment=["resistance_bands"]),
      # ── kettlebell ──
      Exercise(name="KB Goblet Squat",       sets=4, reps="12 reps",       rest_seconds=75, muscle_group="Legs",           difficulty="Easy",   tips="Elbows inside knees, sit deep",                           required_equipment=["kettlebell"]),
    ],
    "intermediate": [
      Exercise(name="Push-ups",              sets=4, reps="15 reps",       rest_seconds=60, muscle_group="Chest",          difficulty="Medium", tips="Add 2-second pause at bottom for max tension",            required_equipment=[]),
      Exercise(name="Bulgarian Split Squat", sets=4, reps="10 each leg",   rest_seconds=75, muscle_group="Legs/Glutes",    difficulty="Medium", tips="Front foot far enough forward, shin stays vertical",      required_equipment=[]),
      Exercise(name="Pike Push-ups",         sets=3, reps="12 reps",       rest_seconds=60, muscle_group="Shoulders",      difficulty="Medium", tips="Inverted V position, lower crown toward floor",           required_equipment=[]),
      Exercise(name="Diamond Push-ups",      sets=3, reps="10 reps",       rest_seconds=60, muscle_group="Triceps/Chest",  difficulty="Medium", tips="Hands close together, elbows graze sides",               required_equipment=[]),
      # ── dumbbells ──
      Exercise(name="DB Incline Press",      sets=4, reps="10 reps",       rest_seconds=90, muscle_group="Upper Chest",    difficulty="Medium", tips="30 degree incline, full ROM",                             required_equipment=["dumbbells"]),
      Exercise(name="DB Romanian Deadlift",  sets=4, reps="10 reps",       rest_seconds=90, muscle_group="Hamstrings",     difficulty="Medium", tips="Push hips back, soft knee bend",                          required_equipment=["dumbbells"]),
      Exercise(name="DB Lateral Raise",      sets=3, reps="15 reps",       rest_seconds=60, muscle_group="Shoulders",      difficulty="Medium", tips="Lead with elbows, slight forward lean",                   required_equipment=["dumbbells"]),
      Exercise(name="DB Arnold Press",       sets=3, reps="10 reps",       rest_seconds=75, muscle_group="Shoulders",      difficulty="Medium", tips="Rotate palms as you press for full delt activation",      required_equipment=["dumbbells"]),
      Exercise(name="DB Hammer Curl",        sets=3, reps="12 reps",       rest_seconds=60, muscle_group="Biceps/Brachialis", difficulty="Medium", tips="Neutral grip, squeeze at top",                       required_equipment=["dumbbells"]),
      # ── barbell ──
      Exercise(name="Barbell Bench Press",   sets=4, reps="8-10 reps",     rest_seconds=120, muscle_group="Chest",         difficulty="Medium", tips="Arch back, feet flat on floor, bar to lower chest",       required_equipment=["barbell"]),
      Exercise(name="Barbell Back Squat",    sets=4, reps="8-10 reps",     rest_seconds=120, muscle_group="Legs/Full Body",difficulty="Medium", tips="Bar on traps, brace core, squat below parallel",          required_equipment=["barbell"]),
      Exercise(name="Deadlift",              sets=3, reps="6-8 reps",      rest_seconds=150, muscle_group="Full Body",     difficulty="Medium", tips="Hinge at hips, bar stays close to shins throughout",      required_equipment=["barbell"]),
      Exercise(name="Barbell Overhead Press",sets=3, reps="8-10 reps",     rest_seconds=90,  muscle_group="Shoulders",     difficulty="Medium", tips="Squeeze glutes, push head through at top",                required_equipment=["barbell"]),
      Exercise(name="Barbell Bent-over Row", sets=4, reps="8-10 reps",     rest_seconds=90,  muscle_group="Back",          difficulty="Medium", tips="Hinge to 45 degrees, pull to lower chest",                required_equipment=["barbell"]),
      # ── pull-up bar ──
      Exercise(name="Pull-ups",              sets=4, reps="6-10 reps",     rest_seconds=90, muscle_group="Back/Biceps",    difficulty="Medium", tips="Full dead hang, pull chest to bar",                       required_equipment=["pull_up_bar"]),
      Exercise(name="Hanging Leg Raise",     sets=3, reps="10 reps",       rest_seconds=60, muscle_group="Core",           difficulty="Medium", tips="Legs straight, raise to 90 degrees, control descent",     required_equipment=["pull_up_bar"]),
      # ── kettlebell ──
      Exercise(name="KB Goblet Squat",       sets=4, reps="12 reps",       rest_seconds=75, muscle_group="Legs",           difficulty="Medium", tips="Elbows inside knees, chest tall",                         required_equipment=["kettlebell"]),
      Exercise(name="KB Swing",              sets=4, reps="15 reps",       rest_seconds=60, muscle_group="Posterior Chain",difficulty="Medium", tips="Hip hinge, not a squat — power from glutes",              required_equipment=["kettlebell"]),
      # ── resistance bands ──
      Exercise(name="Band Face Pull",        sets=4, reps="15 reps",       rest_seconds=45, muscle_group="Rear Delts",     difficulty="Medium", tips="External rotate at end range, elbows high",               required_equipment=["resistance_bands"]),
    ],
    "advanced": [
      Exercise(name="Weighted Push-ups",     sets=4, reps="12 reps",       rest_seconds=75, muscle_group="Chest",          difficulty="Hard",   tips="Add a weight plate on your back",                         required_equipment=[]),
      Exercise(name="Pistol Squats",         sets=3, reps="8 each leg",    rest_seconds=90, muscle_group="Legs",           difficulty="Hard",   tips="Use a counterweight for balance if needed",               required_equipment=[]),
      Exercise(name="Archer Push-ups",       sets=3, reps="8 each side",   rest_seconds=75, muscle_group="Chest/Shoulders",difficulty="Hard",   tips="One arm extended, shift weight side to side",             required_equipment=[]),
      Exercise(name="Decline Push-ups",       sets=4, reps="12 reps",       rest_seconds=60, muscle_group="Upper Chest",    difficulty="Hard",   tips="Feet elevated on chair, head lower than hips",            required_equipment=[]),
      Exercise(name="Single-leg Glute Bridge",sets=4, reps="12 each leg",   rest_seconds=45, muscle_group="Glutes",         difficulty="Hard",   tips="Drive hips up, keep non-working leg straight",           required_equipment=[]),
      # ── barbell ──
      Exercise(name="Heavy Back Squat",      sets=5, reps="5 reps",        rest_seconds=180, muscle_group="Legs/Full Body",difficulty="Hard",   tips="Pause at bottom, explosive drive up",                     required_equipment=["barbell"]),
      Exercise(name="Deadlift",              sets=4, reps="5 reps",        rest_seconds=180, muscle_group="Full Body",     difficulty="Hard",   tips="Max tension before pulling, bar scrapes shins",           required_equipment=["barbell"]),
      Exercise(name="Barbell Hip Thrust",    sets=4, reps="10 reps",       rest_seconds=90,  muscle_group="Glutes",        difficulty="Hard",   tips="Upper back on bench, drive hips to ceiling",              required_equipment=["barbell"]),
      Exercise(name="Close-grip Bench Press",sets=4, reps="8 reps",        rest_seconds=120, muscle_group="Triceps/Chest",difficulty="Hard",   tips="Hands shoulder-width, elbows tuck in",                    required_equipment=["barbell"]),
      # ── dumbbells ──
      Exercise(name="DB Incline Press",      sets=4, reps="10 reps",       rest_seconds=90, muscle_group="Upper Chest",    difficulty="Hard",   tips="30 degree incline, full stretch at bottom",               required_equipment=["dumbbells"]),
      Exercise(name="DB Single-leg RDL",     sets=4, reps="10 each leg",   rest_seconds=75, muscle_group="Hamstrings/Balance", difficulty="Hard", tips="Hinge at hip, keep back flat, soft knee",              required_equipment=["dumbbells"]),
      # ── pull-up bar ──
      Exercise(name="Weighted Pull-ups",     sets=4, reps="6-8 reps",      rest_seconds=120, muscle_group="Back",          difficulty="Hard",   tips="Add 10-20% bodyweight via belt",                          required_equipment=["pull_up_bar"]),
      Exercise(name="L-sit Pull-ups",        sets=3, reps="6 reps",        rest_seconds=90,  muscle_group="Back/Core",     difficulty="Hard",   tips="Keep legs straight and parallel to floor",                required_equipment=["pull_up_bar"]),
      # ── kettlebell ──
      Exercise(name="KB Turkish Get-up",     sets=3, reps="4 each side",   rest_seconds=90, muscle_group="Full Body",      difficulty="Hard",   tips="Slow and deliberate every step, eyes on bell",            required_equipment=["kettlebell"]),
      Exercise(name="KB Double Clean & Press",sets=4,reps="8 reps",        rest_seconds=90, muscle_group="Full Body",      difficulty="Hard",   tips="Clean both bells simultaneously, press at once",          required_equipment=["kettlebell"]),
      # ── resistance bands ──
      Exercise(name="Band Pull-apart",       sets=4, reps="20 reps",       rest_seconds=30, muscle_group="Rear Delts",     difficulty="Medium", tips="Arms straight, full range, controlled return",            required_equipment=["resistance_bands"]),
    ],
  },

  # ════════════════════════════════════════════════════════
  # ENDURANCE
  # ════════════════════════════════════════════════════════
  "endurance": {
    "beginner": [
      Exercise(name="Brisk Walk",            sets=1, reps="20 minutes",    rest_seconds=0,  muscle_group="Cardio",         difficulty="Easy",   tips="Maintain a pace where you can talk but feel warm",        required_equipment=[]),
      Exercise(name="Marching in Place",     sets=3, reps="2 minutes",     rest_seconds=30, muscle_group="Cardio",         difficulty="Easy",   tips="Drive knees up high, pump arms",                          required_equipment=[]),
      Exercise(name="Step-ups",              sets=3, reps="15 each leg",   rest_seconds=30, muscle_group="Legs/Cardio",    difficulty="Easy",   tips="Use a sturdy step, full leg extension",                   required_equipment=[]),
      Exercise(name="Arm Circles",           sets=2, reps="20 each way",   rest_seconds=15, muscle_group="Shoulders",      difficulty="Easy",   tips="Full range, controlled speed",                            required_equipment=[]),
      Exercise(name="Standing Bicycle",      sets=3, reps="30 reps",       rest_seconds=20, muscle_group="Core/Cardio",    difficulty="Easy",   tips="Elbow to opposite knee, rotate fully",                    required_equipment=[]),
      Exercise(name="Treadmill Walk",        sets=1, reps="20 minutes",    rest_seconds=0,  muscle_group="Cardio",         difficulty="Easy",   tips="Incline 3-5% for extra burn",                             required_equipment=["treadmill"]),
    ],
    "intermediate": [
      Exercise(name="Jogging Intervals",     sets=6, reps="2min jog/1min walk", rest_seconds=0, muscle_group="Cardio",    difficulty="Medium", tips="Maintain 70% max heart rate during jog",                  required_equipment=[]),
      Exercise(name="Jump Rope",             sets=4, reps="2 minutes",     rest_seconds=45, muscle_group="Cardio/Calves", difficulty="Medium", tips="Stay on balls of feet, keep a consistent rhythm",         required_equipment=[]),
      Exercise(name="Jumping Jacks",         sets=4, reps="45 seconds",    rest_seconds=15, muscle_group="Cardio",        difficulty="Medium", tips="Maintain consistent pace throughout",                     required_equipment=[]),
      Exercise(name="Lateral Hops",          sets=3, reps="30 seconds",    rest_seconds=30, muscle_group="Legs/Cardio",   difficulty="Medium", tips="Quick light hops, stay on your toes",                     required_equipment=[]),
      Exercise(name="Treadmill Intervals",   sets=6, reps="1min fast/1min slow", rest_seconds=0, muscle_group="Cardio",   difficulty="Medium", tips="Incline 1-2%, really push on the fast intervals",         required_equipment=["treadmill"]),
      Exercise(name="DB Farmer Carry",       sets=4, reps="40 meters",     rest_seconds=60, muscle_group="Full Body/Grip",difficulty="Medium", tips="Tall posture, small quick steps",                         required_equipment=["dumbbells"]),
      Exercise(name="KB Swing",              sets=5, reps="20 reps",       rest_seconds=45, muscle_group="Posterior Chain",difficulty="Medium", tips="Hip hinge, power from glutes, not arms",                  required_equipment=["kettlebell"]),
    ],
    "advanced": [
      Exercise(name="Long Run",              sets=1, reps="45-60 minutes", rest_seconds=0,  muscle_group="Cardio",         difficulty="Hard",   tips="Zone 2 heart rate (60-70% max), conversational pace",     required_equipment=[]),
      Exercise(name="VO2 Max Intervals",     sets=5, reps="4min hard/3min easy", rest_seconds=0, muscle_group="Cardio",   difficulty="Hard",   tips="90-95% max effort on hard, true recovery on easy",        required_equipment=[]),
      Exercise(name="Box Jumps",             sets=5, reps="15 reps",       rest_seconds=30, muscle_group="Legs/Power",     difficulty="Hard",   tips="Explode up, land softly, step down",                      required_equipment=[]),
      Exercise(name="Burpee Box Jump",       sets=4, reps="10 reps",       rest_seconds=45, muscle_group="Full Body",      difficulty="Hard",   tips="Burpee, then explosive jump onto box",                    required_equipment=[]),
      Exercise(name="Treadmill Hill Sprints",sets=6, reps="45s sprint/90s walk", rest_seconds=0, muscle_group="Cardio",   difficulty="Hard",   tips="Incline 8-12%, all-out on sprints",                       required_equipment=["treadmill"]),
      Exercise(name="KB Complex",            sets=4, reps="6 reps each move", rest_seconds=90, muscle_group="Full Body",  difficulty="Hard",   tips="Swing → clean → press → squat without rest between moves",required_equipment=["kettlebell"]),
    ],
  },

  # ════════════════════════════════════════════════════════
  # FLEXIBILITY
  # ════════════════════════════════════════════════════════
  "flexibility": {
    "beginner": [
      Exercise(name="Cat-Cow Stretch",       sets=2, reps="10 cycles",     rest_seconds=15, muscle_group="Spine",          difficulty="Easy",   tips="Synchronize movement with breath",                        required_equipment=[]),
      Exercise(name="Child's Pose",          sets=2, reps="30 seconds",    rest_seconds=15, muscle_group="Back/Hips",      difficulty="Easy",   tips="Walk hands forward for a deeper stretch",                 required_equipment=[]),
      Exercise(name="Hip Flexor Lunge",      sets=2, reps="30s each side", rest_seconds=15, muscle_group="Hips",           difficulty="Easy",   tips="Sink hips forward and down, keep chest tall",             required_equipment=[]),
      Exercise(name="Hamstring Stretch",     sets=2, reps="30s each leg",  rest_seconds=15, muscle_group="Hamstrings",     difficulty="Easy",   tips="Hinge at hip, not the waist, soft knee",                  required_equipment=[]),
      Exercise(name="Shoulder Cross-body",   sets=2, reps="20s each arm",  rest_seconds=10, muscle_group="Shoulders",      difficulty="Easy",   tips="Pull elbow across, keep shoulder down",                   required_equipment=[]),
      Exercise(name="Pigeon Pose",           sets=2, reps="45s each side", rest_seconds=20, muscle_group="Glutes/Hips",    difficulty="Easy",   tips="Use a pillow under hip if needed",                        required_equipment=[]),
      Exercise(name="Chest Opener",          sets=2, reps="30 seconds",    rest_seconds=15, muscle_group="Chest/Shoulders",difficulty="Easy",   tips="Clasp hands behind back, lift chest",                     required_equipment=[]),
      Exercise(name="Band Overhead Stretch", sets=2, reps="10 reps",       rest_seconds=15, muscle_group="Shoulders/Lats", difficulty="Easy",   tips="Grip wide, keep arms straight, slow movement",            required_equipment=["resistance_bands"]),
    ],
    "intermediate": [
      Exercise(name="Downward Dog",          sets=3, reps="45 seconds",    rest_seconds=20, muscle_group="Full Body",      difficulty="Medium", tips="Pedal feet alternately, push heels toward floor",         required_equipment=[]),
      Exercise(name="Lizard Pose",           sets=3, reps="45s each side", rest_seconds=20, muscle_group="Hips/Groin",     difficulty="Medium", tips="Drop back knee down for support",                         required_equipment=[]),
      Exercise(name="Seated Forward Fold",   sets=3, reps="60 seconds",    rest_seconds=15, muscle_group="Hamstrings/Back",difficulty="Medium", tips="Lead with your chest, not your forehead",                 required_equipment=[]),
      Exercise(name="Bridge Pose",           sets=3, reps="30 seconds",    rest_seconds=20, muscle_group="Spine/Glutes",   difficulty="Medium", tips="Press all four corners of each foot into the ground",     required_equipment=[]),
      Exercise(name="Thread the Needle",     sets=3, reps="30s each side", rest_seconds=15, muscle_group="Thoracic Spine", difficulty="Medium", tips="Keep hips stacked, reach arm as far as possible",         required_equipment=[]),
      Exercise(name="Figure-4 Stretch",      sets=3, reps="45s each leg",  rest_seconds=15, muscle_group="Glutes/Hips",    difficulty="Medium", tips="Flex foot to protect knee, pull toward chest",            required_equipment=[]),
    ],
    "advanced": [
      Exercise(name="Full Splits",           sets=3, reps="60 seconds",    rest_seconds=30, muscle_group="Hips/Hamstrings",difficulty="Hard",   tips="Use yoga blocks under hands for support",                 required_equipment=[]),
      Exercise(name="Wheel Pose",            sets=3, reps="30 seconds",    rest_seconds=45, muscle_group="Spine/Chest",    difficulty="Hard",   tips="Press through palms and feet, lift chest high",           required_equipment=[]),
      Exercise(name="King Pigeon",           sets=2, reps="45s each side", rest_seconds=30, muscle_group="Hip Flexors/Spine", difficulty="Hard",tips="Use a strap to reach foot if needed",                    required_equipment=[]),
      Exercise(name="Standing Forward Fold", sets=3, reps="60 seconds",    rest_seconds=20, muscle_group="Hamstrings/Spine",difficulty="Hard",  tips="Bend knees slightly, fold from hips not waist",           required_equipment=[]),
      Exercise(name="Band Hamstring Stretch",sets=3, reps="45s each leg",  rest_seconds=15, muscle_group="Hamstrings",     difficulty="Hard",   tips="Keep leg straight, pull toward you gradually",            required_equipment=["resistance_bands"]),
    ],
  },

  # ════════════════════════════════════════════════════════
  # GENERAL FITNESS
  # ════════════════════════════════════════════════════════
  "general_fitness": {
    "beginner": [
      Exercise(name="Bodyweight Squats",     sets=3, reps="15 reps",       rest_seconds=45, muscle_group="Legs",           difficulty="Easy",   tips="Chest up, knees track over toes",                         required_equipment=[]),
      Exercise(name="Push-ups",              sets=3, reps="10 reps",       rest_seconds=45, muscle_group="Chest/Arms",     difficulty="Easy",   tips="Modify on knees if needed, full range",                   required_equipment=[]),
      Exercise(name="Plank",                 sets=3, reps="20 seconds",    rest_seconds=30, muscle_group="Core",           difficulty="Easy",   tips="Straight line from head to heel, breathe",                required_equipment=[]),
      Exercise(name="Reverse Lunges",        sets=3, reps="10 each leg",   rest_seconds=45, muscle_group="Legs/Glutes",    difficulty="Easy",   tips="Back knee hovers, front shin stays vertical",             required_equipment=[]),
      Exercise(name="Superman Hold",         sets=3, reps="12 reps",       rest_seconds=30, muscle_group="Lower Back",     difficulty="Easy",   tips="Lift arms and legs simultaneously, hold 2 seconds",       required_equipment=[]),
      Exercise(name="Glute Bridges",         sets=3, reps="15 reps",       rest_seconds=30, muscle_group="Glutes",         difficulty="Easy",   tips="Squeeze hard at top, drive hips high",                    required_equipment=[]),
      Exercise(name="Bird Dog",              sets=3, reps="10 each side",  rest_seconds=30, muscle_group="Core/Back",      difficulty="Easy",   tips="Opposite arm and leg, keep hips level",                   required_equipment=[]),
      # ── dumbbells ──
      Exercise(name="DB Goblet Squat",       sets=3, reps="12 reps",       rest_seconds=60, muscle_group="Legs",           difficulty="Easy",   tips="Hold at chest, elbows inside knees at bottom",            required_equipment=["dumbbells"]),
      Exercise(name="DB Shoulder Press",     sets=3, reps="10 reps",       rest_seconds=60, muscle_group="Shoulders",      difficulty="Easy",   tips="Controlled press, don't lock out at top",                 required_equipment=["dumbbells"]),
      Exercise(name="DB Bent-over Row",      sets=3, reps="10 reps",       rest_seconds=60, muscle_group="Back",           difficulty="Easy",   tips="Hinge forward, lead with elbows",                         required_equipment=["dumbbells"]),
      # ── resistance bands ──
      Exercise(name="Band Squat",            sets=3, reps="15 reps",       rest_seconds=30, muscle_group="Legs",           difficulty="Easy",   tips="Band under feet, hold at shoulders",                      required_equipment=["resistance_bands"]),
      Exercise(name="Band Pull-apart",       sets=3, reps="15 reps",       rest_seconds=20, muscle_group="Rear Delts",     difficulty="Easy",   tips="Arms straight, pull band to chest",                       required_equipment=["resistance_bands"]),
      # ── pull-up bar ──
      Exercise(name="Negative Pull-ups",     sets=3, reps="5 reps",        rest_seconds=60, muscle_group="Back/Biceps",    difficulty="Easy",   tips="Jump to top, lower yourself as slowly as possible",       required_equipment=["pull_up_bar"]),
      # ── kettlebell ──
      Exercise(name="KB Deadlift",           sets=3, reps="12 reps",       rest_seconds=60, muscle_group="Hamstrings/Glutes", difficulty="Easy", tips="Hinge at hip, keep chest up and back flat",             required_equipment=["kettlebell"]),
    ],
    "intermediate": [
      Exercise(name="Jump Squats",           sets=4, reps="12 reps",       rest_seconds=45, muscle_group="Legs/Power",     difficulty="Medium", tips="Soft landing, absorb with full squat depth",              required_equipment=[]),
      Exercise(name="Push-ups",              sets=4, reps="15 reps",       rest_seconds=45, muscle_group="Chest/Arms",     difficulty="Medium", tips="Straight body line, chest grazes floor",                  required_equipment=[]),
      Exercise(name="Side Plank",            sets=3, reps="30s each side", rest_seconds=30, muscle_group="Core/Obliques",  difficulty="Medium", tips="Hip stays lifted, stack feet",                            required_equipment=[]),
      Exercise(name="Bulgarian Split Squat", sets=3, reps="10 each leg",   rest_seconds=60, muscle_group="Legs/Glutes",    difficulty="Medium", tips="Rear foot elevated, front shin vertical",                 required_equipment=[]),
      Exercise(name="Decline Push-ups",      sets=3, reps="12 reps",       rest_seconds=45, muscle_group="Upper Chest",    difficulty="Medium", tips="Feet elevated, targets upper chest",                      required_equipment=[]),
      # ── dumbbells ──
      Exercise(name="DB Squat to Press",     sets=4, reps="12 reps",       rest_seconds=60, muscle_group="Full Body",      difficulty="Medium", tips="Fluid motion — squat, stand, press",                      required_equipment=["dumbbells"]),
      Exercise(name="DB Renegade Row",       sets=3, reps="8 each arm",    rest_seconds=60, muscle_group="Back/Core",      difficulty="Medium", tips="Minimal hip rotation, brace core hard",                   required_equipment=["dumbbells"]),
      Exercise(name="DB Reverse Lunge Curl", sets=3, reps="10 each leg",   rest_seconds=45, muscle_group="Legs/Biceps",    difficulty="Medium", tips="Step back, curl at bottom position",                      required_equipment=["dumbbells"]),
      Exercise(name="DB Romanian Deadlift",  sets=3, reps="12 reps",       rest_seconds=75, muscle_group="Hamstrings",     difficulty="Medium", tips="Push hips back, bar stays close to legs",                 required_equipment=["dumbbells"]),
      # ── barbell ──
      Exercise(name="Barbell Back Squat",    sets=4, reps="8 reps",        rest_seconds=120, muscle_group="Legs/Full Body",difficulty="Medium", tips="Bar on traps, brace core, squat below parallel",          required_equipment=["barbell"]),
      Exercise(name="Barbell Deadlift",      sets=3, reps="8 reps",        rest_seconds=120, muscle_group="Full Body",     difficulty="Medium", tips="Hinge at hips, bar stays close to shins",                 required_equipment=["barbell"]),
      Exercise(name="Barbell Bench Press",   sets=4, reps="8 reps",        rest_seconds=120, muscle_group="Chest",         difficulty="Medium", tips="Arch back, feet flat, lower bar to chest",                required_equipment=["barbell"]),
      # ── pull-up bar ──
      Exercise(name="Pull-ups",             sets=4, reps="6-10 reps",      rest_seconds=90, muscle_group="Back/Biceps",    difficulty="Medium", tips="Full dead hang, pull chest to bar",                       required_equipment=["pull_up_bar"]),
      Exercise(name="Hanging Knee Raise",   sets=3, reps="12 reps",        rest_seconds=45, muscle_group="Core",           difficulty="Medium", tips="Control the swing, squeeze abs at top",                   required_equipment=["pull_up_bar"]),
      # ── kettlebell ──
      Exercise(name="KB Swing",             sets=4, reps="15 reps",        rest_seconds=60, muscle_group="Posterior Chain",difficulty="Medium", tips="Hip hinge, power from glutes, arms just guide",           required_equipment=["kettlebell"]),
      Exercise(name="KB Goblet Squat",      sets=4, reps="12 reps",        rest_seconds=60, muscle_group="Legs",           difficulty="Medium", tips="Hold tight to chest, elbows inside knees",                required_equipment=["kettlebell"]),
      # ── resistance bands ──
      Exercise(name="Band Face Pull",       sets=3, reps="15 reps",        rest_seconds=30, muscle_group="Rear Delts",     difficulty="Medium", tips="Pull to forehead, external rotate at end range",          required_equipment=["resistance_bands"]),
    ],
    "advanced": [
      Exercise(name="Burpees",              sets=5, reps="15 reps",        rest_seconds=45, muscle_group="Full Body",      difficulty="Hard",   tips="Explosive jump, controlled descent",                      required_equipment=[]),
      Exercise(name="Pistol Squats",        sets=3, reps="8 each leg",     rest_seconds=75, muscle_group="Legs",           difficulty="Hard",   tips="Counterweight helps balance if needed",                   required_equipment=[]),
      Exercise(name="Handstand Hold",       sets=3, reps="20 seconds",     rest_seconds=60, muscle_group="Shoulders/Core", difficulty="Hard",   tips="Use wall for support, squeeze everything tight",          required_equipment=[]),
      Exercise(name="Dragon Flags",         sets=3, reps="6 reps",         rest_seconds=90, muscle_group="Core",           difficulty="Hard",   tips="Slow controlled descent, explosive return",               required_equipment=[]),
      # ── barbell ──
      Exercise(name="Barbell Complex",      sets=4, reps="6 reps each",    rest_seconds=120, muscle_group="Full Body",     difficulty="Hard",   tips="Row → clean → squat → press without putting bar down",    required_equipment=["barbell"]),
      Exercise(name="Heavy Deadlift",       sets=4, reps="5 reps",         rest_seconds=180, muscle_group="Full Body",     difficulty="Hard",   tips="Max tension before lift, bar scrapes shins",              required_equipment=["barbell"]),
      # ── dumbbells ──
      Exercise(name="DB Man-makers",        sets=3, reps="8 reps",         rest_seconds=75, muscle_group="Full Body",      difficulty="Hard",   tips="Push-up, row row, squat, press — one sequence",           required_equipment=["dumbbells"]),
      Exercise(name="DB Single-leg RDL",    sets=4, reps="10 each leg",    rest_seconds=60, muscle_group="Hamstrings/Balance", difficulty="Hard", tips="Hinge at hip, keep back flat, slight knee bend",        required_equipment=["dumbbells"]),
      # ── pull-up bar ──
      Exercise(name="Weighted Pull-ups",    sets=4, reps="6-8 reps",       rest_seconds=120, muscle_group="Back",          difficulty="Hard",   tips="Add 10-20% bodyweight via belt or vest",                  required_equipment=["pull_up_bar"]),
      Exercise(name="Muscle-ups",           sets=3, reps="5 reps",         rest_seconds=90,  muscle_group="Back/Chest",    difficulty="Hard",   tips="Explosive pull, transition above bar smoothly",           required_equipment=["pull_up_bar"]),
      # ── kettlebell ──
      Exercise(name="KB Turkish Get-up",    sets=3, reps="4 each side",    rest_seconds=90, muscle_group="Full Body",      difficulty="Hard",   tips="Slow every step, keep eyes on the bell",                  required_equipment=["kettlebell"]),
    ],
  },
}


# ── Warmup / Cooldown ─────────────────────────────────────────────────────────
WARMUP   = ["5-min light jog or jumping jacks", "Leg swings — 10 each direction", "Arm circles — 10 each way", "Hip circles — 10 each direction", "30-second deep breathing"]
COOLDOWN = ["3-min slow walk or easy march", "Quad stretch — 30s each leg", "Hamstring stretch — 30s each leg", "Chest opener — 30 seconds", "Full body shake-out and deep breathe"]

FOCUS_MAP = {
    "weight_loss":    ["HIIT & Cardio Burn","Lower Body Fat Burn","Upper Body Cardio","Full Body Circuit","Active Recovery","Metabolic Conditioning","Cardio Endurance"],
    "muscle_gain":    ["Chest & Triceps","Back & Biceps","Legs & Glutes","Shoulders & Arms","Full Body Compound","Upper Body Push","Lower Body Power"],
    "endurance":      ["Aerobic Base","Tempo Training","Interval Training","Long Steady State","Cross-Training","Recovery","VO2 Intervals"],
    "flexibility":    ["Morning Flow","Hip Opening","Spine Mobility","Shoulder Mobility","Evening Wind-Down","Full Body Stretch","Restorative"],
    "general_fitness":["Full Body Strength","Cardio & Core","Upper Body","Lower Body","HIIT Mix","Functional Movement","Active Recovery"],
}

DURATION_MAP = {
    "weight_loss":    {"beginner":35,"intermediate":45,"advanced":55},
    "muscle_gain":    {"beginner":50,"intermediate":65,"advanced":75},
    "endurance":      {"beginner":30,"intermediate":50,"advanced":70},
    "flexibility":    {"beginner":25,"intermediate":40,"advanced":55},
    "general_fitness":{"beginner":35,"intermediate":50,"advanced":60},
}

DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

RESULT_MAP = {
    "weight_loss":    "Expect 0.5–1 kg fat loss per week with consistent training and nutrition. Noticeable body composition changes in 8–12 weeks.",
    "muscle_gain":    "With progressive overload: 1–2 kg lean muscle per month for beginners, ~0.5 kg for intermediate. Visible gains in 6–8 weeks.",
    "endurance":      "Cardiovascular capacity improves 10–15% in the first 4 weeks. Expect to extend cardio duration 10–20% every two weeks.",
    "flexibility":    "Noticeable flexibility gains in 2–4 weeks of daily practice. Major range-of-motion improvements by 8–12 weeks.",
    "general_fitness":"All-round improvements visible within 3–4 weeks. Energy, strength, and stamina all rise progressively.",
}

TIPS = {
    "weight_loss":    ["Sleep 7–9 hours — poor sleep raises ghrelin (hunger hormone)","Track your food with an app — awareness alone reduces intake","Aim for 8,000–10,000 steps daily outside of workouts","Eat slowly — it takes 20 minutes to register fullness","Meal prep on Sundays to avoid impulsive food choices"],
    "muscle_gain":    ["Progressive overload — increase weight 2.5–5% each week","Never skip legs — they release the most anabolic hormones","Sleep 8+ hours — 70% of muscle repair happens during deep sleep","Take a planned deload week every 8–10 weeks","Creatine monohydrate 5g/day is the most evidence-backed supplement"],
    "endurance":      ["Build weekly mileage by no more than 10% per week","Include one long slow distance session every week","Cross-train (swim, cycle) to prevent overuse injuries","Monitor heart rate zones — most training should be Zone 2","Compression gear and ice baths speed up recovery"],
    "flexibility":    ["Stretch daily — 10 consistent minutes beats 60 sporadic minutes","Never stretch cold muscles — always warm up first","Props (blocks, straps) deepen stretches, not cheat them","Focus on slow diaphragmatic breathing during holds","Consistency beats intensity for flexibility gains"],
    "general_fitness":["Mix cardio, strength, and flexibility each week","Rest days are when adaptation happens — take them seriously","Find activities you enjoy — consistency is the only thing that works","Drink water before you feel thirsty — thirst means you're already behind","Track workouts in a notebook — seeing progress is deeply motivating"],
}


# ── Equipment filter ──────────────────────────────────────────────────────────
def filter_by_equipment(exercises: list, user_equipment: list) -> list:
    owned    = set(e.lower().strip() for e in user_equipment)
    bodyweight_only = "none" in owned or len(owned) == 0

    result = []
    for ex in exercises:
        needed = set(e.lower().strip() for e in ex.required_equipment)
        if not needed:
            result.append(ex)                   # bodyweight — always include
        elif bodyweight_only:
            continue                            # user has no gear
        elif needed.issubset(owned):
            result.append(ex)                   # user has ALL required equipment
    return result


# ── Metrics ───────────────────────────────────────────────────────────────────
def calculate_metrics(p: UserProfile) -> Metrics:
    bmi = p.weight_kg / ((p.height_cm / 100) ** 2)
    cat = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"

    bmr = int((10 * p.weight_kg + 6.25 * p.height_cm - 5 * p.age) + (5 if p.gender == "male" else -161))
    mult = {"sedentary":1.2,"light":1.375,"moderate":1.55,"active":1.725,"very_active":1.9}
    tdee = int(bmr * mult[p.activity_level])
    adj  = {"weight_loss":-500,"muscle_gain":300,"endurance":100,"flexibility":0,"general_fitness":0}

    iw = (48 + 2.7 * ((p.height_cm / 2.54) - 60)) if p.gender == "male" else (45.4 + 2.3 * ((p.height_cm / 2.54) - 60))
    return Metrics(bmi=round(bmi,1), bmi_category=cat, bmr=bmr, tdee=tdee,
                   target_calories=tdee + adj[p.fitness_goal],
                   ideal_weight_kg_range=f"{int(iw*0.9)}–{int(iw*1.1)} kg")


# ── Weekly plan ───────────────────────────────────────────────────────────────
def build_weekly_plan(p: UserProfile) -> list[WorkoutDay]:
    all_ex    = ALL_EXERCISES[p.fitness_goal][p.experience_level]
    available = filter_by_equipment(all_ex, p.equipment)

    # Bodyweight fallback pool if barely any exercises matched
    if len(available) < 4:
        fallbacks = [e for e in ALL_EXERCISES["general_fitness"]["beginner"] if not e.required_equipment]
        seen = {e.name for e in available}
        for fb in fallbacks:
            if fb.name not in seen:
                available.append(fb)
                seen.add(fb.name)
            if len(available) >= 8:
                break

    focuses  = FOCUS_MAP[p.fitness_goal]
    duration = DURATION_MAP[p.fitness_goal][p.experience_level]
    plan     = []

    # Shuffle once so days get different exercise combos
    pool = available.copy()
    random.shuffle(pool)

    # Give each day a unique slice of 4 exercises, cycling through the pool
    for i in range(p.available_days):
        start = (i * 4) % len(pool)
        # Wrap-around slice
        day_exs = (pool * 2)[start:start + 4]
        # Rotate pool slightly each day for more variety
        pool = pool[1:] + pool[:1]

        plan.append(WorkoutDay(
            day=DAYS[i],
            focus=focuses[i % len(focuses)],
            duration_minutes=duration,
            exercises=day_exs,
            warmup=WARMUP,
            cooldown=COOLDOWN,
        ))
    return plan


# ── Nutrition ─────────────────────────────────────────────────────────────────
def build_nutrition(p: UserProfile, metrics: Metrics) -> NutritionPlan:
    cal  = metrics.target_calories
    goal = p.fitness_goal

    if goal == "muscle_gain":
        protein_g = int(p.weight_kg * 2.2);  fat_g = int(cal * 0.25 / 9)
    elif goal == "weight_loss":
        protein_g = int(p.weight_kg * 2.0);  fat_g = int(cal * 0.30 / 9)
    elif goal == "endurance":
        protein_g = int(p.weight_kg * 1.6);  fat_g = int(cal * 0.22 / 9)
    else:
        protein_g = int(p.weight_kg * 1.8);  fat_g = int(cal * 0.28 / 9)

    carbs_g = max(int((cal - protein_g * 4 - fat_g * 9) / 4), 50)

    TIMING = {
        "weight_loss":    ["7:00 AM — High-protein breakfast","10:00 AM — Small snack if hungry","1:00 PM — Balanced lunch","4:00 PM — Pre-workout snack","7:00 PM — Light protein-rich dinner"],
        "muscle_gain":    ["7:00 AM — Large carb + protein breakfast","10:00 AM — Protein shake + fruit","1:00 PM — Generous lunch with rice or pasta","Pre-workout — Meal 60-90 min before training","Post-workout — Protein shake within 30 min","7:00 PM — High-protein dinner","9:00 PM — Casein shake or cottage cheese"],
        "endurance":      ["6:00 AM — Carb-rich breakfast before long sessions","During workout — 30-60g carbs per hour if over 60 min","Post-workout — Carbs + protein within 30 min","1:00 PM — Balanced lunch","7:00 PM — Carb-loading dinner if long session tomorrow"],
        "flexibility":    ["8:00 AM — Light breakfast","12:00 PM — Balanced lunch","3:00 PM — Anti-inflammatory snack","7:00 PM — Balanced dinner"],
        "general_fitness":["7:00 AM — Balanced breakfast","12:00 PM — Protein-rich lunch","3:00 PM — Healthy snack","7:00 PM — Well-balanced dinner"],
    }
    EAT = {
        "weight_loss":    ["Chicken breast & turkey","Eggs & egg whites","Greek yogurt","Leafy greens & vegetables","Berries & low-GI fruits","Oats & quinoa (moderate)","Legumes & beans","Salmon & tuna"],
        "muscle_gain":    ["Beef, chicken, turkey","Whole eggs & dairy","Brown rice, oats, pasta","Sweet potatoes","Nuts & nut butters","Avocados","Salmon & mackerel","Cottage cheese"],
        "endurance":      ["Oats, brown rice, quinoa","Bananas & dates","Chicken, fish, eggs","Beetroot (nitrate boost)","Sports drinks for long sessions","Berries & antioxidant foods"],
        "flexibility":    ["Turmeric & ginger (anti-inflammatory)","Leafy greens","Berries & citrus","Fatty fish (omega-3)","Bone broth (collagen)","Nuts & seeds"],
        "general_fitness":["Lean proteins (chicken, fish, eggs)","Complex carbs (oats, brown rice)","Colorful vegetables","Healthy fats (avocado, nuts)","Greek yogurt","Legumes"],
    }
    AVOID = {
        "weight_loss":    ["Sugary drinks & sodas","Processed snacks & chips","White bread & pastries","Alcohol","Fried foods","High-calorie sauces & dressings"],
        "muscle_gain":    ["Excessive alcohol","Junk food (empty calories)","Skipping meals","Extreme calorie deficits"],
        "endurance":      ["Heavy fatty meals before training","Excessive fiber before workouts","Alcohol (dehydrating)","High-sugar refined foods"],
        "flexibility":    ["Inflammatory foods (fried, processed)","Excess sugar","Alcohol","Refined grains"],
        "general_fitness":["Sugary drinks","Ultra-processed foods","Excess alcohol","Trans fats"],
    }

    hydration = round(p.weight_kg * 0.035 + (0.5 if p.activity_level in ["active","very_active"] else 0.2), 1)

    return NutritionPlan(
        daily_calories=cal, protein_g=max(protein_g,50), carbs_g=carbs_g, fat_g=max(fat_g,30),
        meal_timing=TIMING[goal], foods_to_eat=EAT[goal], foods_to_avoid=AVOID[goal],
        hydration_liters=hydration,
    )


# ── Main recommender ──────────────────────────────────────────────────────────
def recommend(p: UserProfile) -> RecommendationResponse:
    t0        = time.time()
    metrics   = calculate_metrics(p)
    plan      = build_weekly_plan(p)
    nutrition = build_nutrition(p, metrics)
    return RecommendationResponse(
        user_name=p.name, fitness_goal=p.fitness_goal,
        selected_equipment=p.equipment,
        metrics=metrics, weekly_plan=plan, nutrition=nutrition,
        lifestyle_tips=TIPS[p.fitness_goal],
        estimated_results=RESULT_MAP[p.fitness_goal],
        processing_time_ms=round((time.time()-t0)*1000, 3),
    )


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
def root(): return {"message": "Fitness Recommendation API v2.0 running. Visit /docs"}

@app.get("/health")
def health(): return {"status":"healthy","version":"2.0.0","uptime_seconds":round(time.time()-START_TIME,2)}

@app.post("/api/v1/recommend", response_model=RecommendationResponse)
def get_recommendation(profile: UserProfile):
    return recommend(profile)

@app.get("/api/v1/goals")
def list_goals(): return {"goals":["weight_loss","muscle_gain","endurance","flexibility","general_fitness"]}

@app.get("/api/v1/equipment")
def list_equipment(): return {"equipment":["dumbbells","barbell","resistance_bands","pull_up_bar","bench","kettlebell","treadmill","none"]}
