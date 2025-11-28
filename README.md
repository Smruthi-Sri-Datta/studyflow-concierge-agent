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
