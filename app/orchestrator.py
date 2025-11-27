# app/orchestrator.py

from typing import Any, Dict, List

from app.agents.memory_agent import MemoryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.reflection_agent import ReflectionAgent


memory_agent = MemoryAgent()
planner_agent = PlannerAgent(memory_agent)
reflection_agent = ReflectionAgent(memory_agent)


def setup_user(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Initialize user courses, tasks and profile.

    payload format example:
    {
        "courses": [...],
        "tasks": [...],
        "profile": {
            "preferred_block_minutes": 45,
            "max_blocks_per_day": 3
        }
    }
    """
    courses = payload.get("courses", [])
    tasks = payload.get("tasks", [])
    profile = payload.get("profile", {})

    return memory_agent.setup_user(
        user_id=user_id,
        courses=courses,
        tasks=tasks,
        profile_overrides=profile,
    )


def plan_day(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Plan study blocks for a given day.

    payload example:
    {
        "date": "2025-11-28",
        "available_windows": [
            {"start": "19:00", "end": "21:00"}
        ]
    }
    """
    date_str = payload["date"]
    available_windows: List[Dict[str, str]] = payload["available_windows"]

    return planner_agent.plan_day(user_id, date_str, available_windows)


def reflect(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle reflection after a study session.

    payload example:
    {
        "completed_task_ids": [...],
        "partial_task_ids": [...],
        "difficulty_rating": 3,
        "notes": "CNN math was harder than expected.",
        "date": "2025-11-28"   # optional
    }
    """
    completed = payload.get("completed_task_ids", [])
    partial = payload.get("partial_task_ids", [])
    rating = int(payload.get("difficulty_rating", 3))
    notes = payload.get("notes", "")
    date_str = payload.get("date")

    return reflection_agent.reflect(
        user_id=user_id,
        completed_task_ids=completed,
        partial_task_ids=partial,
        difficulty_rating=rating,
        notes=notes,
        date_str=date_str,
    )


def get_status(user_id: str) -> Dict[str, Any]:
    """Return basic progress status for the user."""
    return memory_agent.get_status(user_id)
