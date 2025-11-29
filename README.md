<<<<<<< HEAD
# StudyFlow Concierge Agent  
A lightweight, modular study-planning agent that helps students organize daily work, generate study schedules, and receive personalized reflection feedback.  
Built with a domain-driven architecture, Gemini LLM integration, and a clean REST API layer.

---

## 🚀 Features

### **Core Functions**
- **User setup** (courses, tasks, study profile)
- **Daily plan generation** (time-window based scheduling)
- **Personalized LLM feedback** using Gemini 2.5 Flash
- **Session tracking** (interaction count, timestamps)
- **Task history & progress tracking**

### **Technical Highlights**
- Domain-driven folder structure
- Stateless REST API using **FastAPI + Uvicorn**
- LLM abstraction layer with fallback logic
- JSON-based evaluation inputs (setup, plan, reflect)
- Clean in-memory store for simplicity  
  *(can later be replaced by Firestore / Postgres)*

---

## 🧱 Project Structure

```text
studyflow-concierge-agent/
│
├── app/
│   ├── api.py                 # REST API endpoints
│   ├── config/
│   │   └── settings.py        # env loading (Gemini key)
│   ├── domain/
│   │   ├── orchestrator.py    # high-level workflow manager
│   │   ├── agents/
│   │   │   ├── memory_agent.py
│   │   │   ├── planner_agent.py
│   │   │   └── reflection_agent.py
│   │   └── memory/
│   │       └── store.py       # simple JSON user state store
│   └── llm/
│       ├── client.py          # Gemini model loader
│       ├── prompts.py         # LLM prompt templates
│       └── tools.py           # summarization & reflection tools
│
├── eval/
│   ├── agent_demo.py          # full workflow demo
│   ├── setup_test.json
│   ├── plan_test.json
│   └── reflect_test.json
│
├── quick_models_test.py       # model listing utility
├── requirements.txt
└── README.md
=======


# StudyFlow Concierge Agent

The **StudyFlow Concierge Agent** is an AI-powered study planning and reflection system built using **FastAPI** and **Gemini LLMs**, deployed on **Google Cloud Run**. It helps students organize their study tasks, generate daily plans, reflect on progress, and receive adaptive feedback.

---

## Features

* Study plan generation based on tasks, deadlines, and user preferences
* Reflection-based adaptation (learning patterns update automatically)
* LLM-generated personalized feedback
* Lightweight REST API for easy integration
* Fully containerized and cloud-ready

---
## Flow Diagram




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

```
app/        # API + domain logic  
llm/        # Gemini client and prompts  
deploy/     # Dockerfile for Cloud Run  
eval/       # Test JSON files  
```

---

## Local Run

```bash
uvicorn app.api:app --reload --port 8000
```

---

## Deployment (Cloud Run)

```bash
gcloud run deploy studyflow-concierge-agent \
  --source . \
  --region=asia-east1 \
  --allow-unauthenticated \
  --set-env-vars=GEMINI_API_KEY=YOUR_KEY
```

---

## Testing

```bash
curl -X POST "$BASE/setup_user"  -d "@eval/setup_test.json"
curl -X POST "$BASE/plan_day"    -d "@eval/plan_test.json"
curl -X POST "$BASE/reflect"     -d "@eval/reflect_test.json"
curl "$BASE/status?user_id=demo_user"
```

---

## License

For educational and evaluation use.


>>>>>>> 75addfb (Update API, add Cloud Run Dockerfile, add flow diagram image, and update README)
