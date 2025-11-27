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
        "profile": {...}
    }
    """
    courses = payload.get("courses", [])
    tasks = payload.get("tasks", [])
    profile = payload.get("profile", {})

    profile_summary = memory_agent.setup_user(
        user_id=user_id,
        courses=courses,
        tasks=tasks,
        profile_overrides=profile,
    )

    # Start a fresh session for this user (e.g., onboarding session)
    session = memory_agent.start_or_continue_session(user_id)

    return {
        "profile_summary": profile_summary,
        "session": session,
    }


def plan_day(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Plan study blocks for a given day.

    payload example:
    {
        "date": "2025-11-28",
        "available_windows": [...],
        "session_id": "optional-session-id"
    }
    """
    date_str = payload["date"]
    available_windows: List[Dict[str, str]] = payload["available_windows"]
    session_id = payload.get("session_id")

    # Update session info (or start a new one if none)
    session = memory_agent.start_or_continue_session(user_id, session_id=session_id)

    plan = planner_agent.plan_day(user_id, date_str, available_windows)
    plan["session"] = session
    return plan


def reflect(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle reflection after a study session.
    """
    completed = payload.get("completed_task_ids", [])
    partial = payload.get("partial_task_ids", [])
    rating = int(payload.get("difficulty_rating", 3))
    notes = payload.get("notes", "")
    date_str = payload.get("date")
    session_id = payload.get("session_id")

    session = memory_agent.start_or_continue_session(user_id, session_id=session_id)

    reflection_result = reflection_agent.reflect(
        user_id=user_id,
        completed_task_ids=completed,
        partial_task_ids=partial,
        difficulty_rating=rating,
        notes=notes,
        date_str=date_str,
    )
    reflection_result["session"] = session
    return reflection_result


def get_status(user_id: str) -> Dict[str, Any]:
    """Return basic progress status for the user."""
    status = memory_agent.get_status(user_id)
    status["session"] = memory_agent.get_session_info(user_id)
    return status
