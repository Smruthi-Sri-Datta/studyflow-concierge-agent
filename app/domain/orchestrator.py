# app/domain/orchestrator.py

from typing import Any, Dict, List

from app.domain.agents.memory_agent import MemoryAgent
from app.domain.agents.planner_agent import PlannerAgent
from app.domain.agents.reflection_agent import ReflectionAgent
from app.llm.tools import generate_reflection_feedback


memory_agent = MemoryAgent()
planner_agent = PlannerAgent(memory_agent)
reflection_agent = ReflectionAgent(memory_agent)


def setup_user(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Initialize user courses, tasks and profile.

    payload example:
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

    # Start a fresh session for this user
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
    High-level reflection flow:
      - update tasks & history
      - adapt profile
      - update session
      - generate LLM feedback
      - return combined result
    """
    completed_task_ids = payload.get("completed_task_ids", [])
    partial_task_ids = payload.get("partial_task_ids", [])
    difficulty_rating = payload.get("difficulty_rating", 3)
    notes = payload.get("notes", "")
    date_str = payload.get("date")

    # 1. Core reflection logic (updates state)
    reflection_result = reflection_agent.reflect(
        user_id=user_id,
        completed_task_ids=completed_task_ids,
        partial_task_ids=partial_task_ids,
        difficulty_rating=difficulty_rating,
        notes=notes,
        date_str=date_str,
    )

    history_entry = reflection_result["history_entry"]
    profile = reflection_result["updated_profile"]

    # 2. Update / continue session
    session = memory_agent.start_or_continue_session(user_id)

    # 3. Get status for feedback
    status = memory_agent.get_status(user_id)

    # 4. LLM feedback
    feedback_text = generate_reflection_feedback(history_entry, status)

    # 5. Combined result
    return {
        "history_entry": history_entry,
        "updated_profile": profile,
        "session": session,
        "feedback_text": feedback_text,
    }


def get_status(user_id: str) -> Dict[str, Any]:
    """
    Return basic progress status for the user.
    """
    status = memory_agent.get_status(user_id)
    status["session"] = memory_agent.get_session_info(user_id)
    return status
