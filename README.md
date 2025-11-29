# StudyFlow Concierge Agent

The **StudyFlow Concierge Agent** is an AI-powered study planning and reflection system built using **FastAPI** and **Gemini LLMs**, deployed on **Google Cloud Run**. It helps students organize their study tasks, generate daily plans, reflect on progress, and receive adaptive feedback.

---

## Features

- Study plan generation based on tasks, deadlines, and user preferences  
- Reflection-based adaptation (learning patterns update automatically)  
- LLM-generated personalized feedback  
- Lightweight REST API for easy integration  
- Fully containerized and cloud-ready  

---

## Flow Diagram

<p align="center">
  <img src="assets/image.png" width="600">
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
llm/        # Gemini client and prompts
eval/       # Test JSON files
Dockerfile  # Cloud Run container
