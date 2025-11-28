# app/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from app.domain import orchestrator

app = FastAPI(title="StudyFlow Concierge API")


# ---------- Request models ----------

class Course(BaseModel):
    course_id: str
    name: str


class Task(BaseModel):
    task_id: str
    course_id: str
    title: str
    deadline_date: str
    status: Optional[str] = "pending"


class Profile(BaseModel):
    preferred_block_minutes: int = 45
    max_blocks_per_day: int = 2


class SetupPayload(BaseModel):
    user_id: str
    courses: List[Course]
    tasks: List[Task]
    profile: Profile


class Window(BaseModel):
    start: str
    end: str


class PlanPayload(BaseModel):
    user_id: str
    date: str
    available_windows: List[Window]
    session_id: Optional[str] = None


class ReflectPayload(BaseModel):
    user_id: str
    completed_task_ids: List[str]
    partial_task_ids: List[str]
    difficulty_rating: int
    notes: str
    date: Optional[str] = None


# ---------- Endpoints ----------

@app.post("/setup_user")
def setup_user(payload: SetupPayload) -> Dict[str, Any]:
    result = orchestrator.setup_user(
        payload.user_id,
        {
            "courses": [c.model_dump() for c in payload.courses],
            "tasks": [t.model_dump() for t in payload.tasks],
            "profile": payload.profile.model_dump(),
        },
    )
    return result


@app.post("/plan_day")
def plan_day(payload: PlanPayload) -> Dict[str, Any]:
    result = orchestrator.plan_day(
        payload.user_id,
        {
            "date": payload.date,
            "available_windows": [w.model_dump() for w in payload.available_windows],
            "session_id": payload.session_id,
        },
    )
    return result


@app.post("/reflect")
def reflect(payload: ReflectPayload) -> Dict[str, Any]:
    result = orchestrator.reflect(
        payload.user_id,
        {
            "completed_task_ids": payload.completed_task_ids,
            "partial_task_ids": payload.partial_task_ids,
            "difficulty_rating": payload.difficulty_rating,
            "notes": payload.notes,
            "date": payload.date,
        },
    )
    return result


@app.get("/status")
def get_status(user_id: str) -> Dict[str, Any]:
    return orchestrator.get_status(user_id)
