# StudyFlow Concierge Agent

The **StudyFlow Concierge Agent** is an AI-powered study planning and reflection system built using **FastAPI** and **Gemini LLMs**, deployed on **Google Cloud Run**. It helps students organize their study tasks, generate daily plans, reflect on progress, and receive adaptive feedback.

---

## Features

- Study plan generation based on tasks, deadlines, and user preferences  
- Reflection-based adaptation (learning patterns update automatically)  
- LLM-generated personalized feedback  
- Lightweight REST API for easy integration  
- Fully containerized and cloud-ready (Docker + Cloud Run)

---

## Flow Diagram

<p align="center">
  <img src="assets/flow-diagram.png" width="450">
</p>

---

## API Endpoints

| Method | Endpoint      | Description                            |
| ------ | ------------- | -------------------------------------- |
| GET    | `/`           | Health check                           |
| POST   | `/setup_user` | Initialize profile, courses, and tasks |
| POST   | `/plan_day`   | Generate study plan                    |
| POST   | `/reflect`    | Submit reflection and get feedback     |
| GET    | `/status`     | Current study progress                 |

---

## Project Structure

```text
app/        # API + domain logic
app/llm/    # Gemini client and prompts
deploy/     # Cloud Run instructions
eval/       # Test JSON payloads
Dockerfile  # Container build for Cloud Run
```

---

# Local Run
uvicorn app.api:app --reload --port 8000

---

# Deployment (Cloud Run)
gcloud run deploy studyflow-concierge-agent \
  source . \
  region=asia-east1 \
  allow-unauthenticated \
  set-env-vars=GEMINI_API_KEY=YOUR_KEY

---

# Testing
Assuming BASE is your Cloud Run URL\
curl -X POST "$BASE/setup_user"  -H "Content-Type: application/json" -d "@eval/setup_test.json"\
curl -X POST "$BASE/plan_day"    -H "Content-Type: application/json" -d "@eval/plan_test.json"\
curl -X POST "$BASE/reflect"     -H "Content-Type: application/json" -d "@eval/reflect_test.json"\
curl "$BASE/status?user_id=demo_user"

---

# License
For educational and evaluation use.




