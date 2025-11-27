# app/memory/store.py

from typing import Dict, Any, List

# Very simple in-memory store.
# For the capstone this is enough; in production this could be a real database.
_USER_STORE: Dict[str, Dict[str, Any]] = {}


def _default_state() -> Dict[str, Any]:
    """Initial state for a new user."""
    return {
        "courses": [],   # list of course dicts
        "tasks": [],     # list of task dicts
        "profile": {     # simple preferences
            "preferred_block_minutes": 45,
            "max_blocks_per_day": 3,
        },
        "history": [],   # reflections / past sessions
        "session": {     # simple session tracking
            "current_session_id": None,
            "last_interaction_at": None,
            "interaction_count": 0,
        },
    }



def get_user_state(user_id: str) -> Dict[str, Any]:
    """
    Get the full state for a user.
    If the user does not exist yet, create a default state.
    """
    if user_id not in _USER_STORE:
        _USER_STORE[user_id] = _default_state()
    return _USER_STORE[user_id]


def save_user_state(user_id: str, state: Dict[str, Any]) -> None:
    """Persist the full state for a user."""
    _USER_STORE[user_id] = state


def add_course(user_id: str, course: Dict[str, Any]) -> None:
    """Append a course dict to the user's courses list."""
    state = get_user_state(user_id)
    state["courses"].append(course)
    save_user_state(user_id, state)


def add_task(user_id: str, task: Dict[str, Any]) -> None:
    """Append a task dict to the user's tasks list."""
    state = get_user_state(user_id)
    state["tasks"].append(task)
    save_user_state(user_id, state)


def list_tasks(user_id: str) -> List[Dict[str, Any]]:
    """Return all tasks for the user."""
    state = get_user_state(user_id)
    return state["tasks"]
