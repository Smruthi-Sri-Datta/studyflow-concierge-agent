# app/agents/memory_agent.py

from datetime import datetime
from typing import Any, Dict, List

from app.domain.memory.store import get_user_state, save_user_state


class MemoryAgent:
    """
    Handles long-term user state:
    - courses
    - tasks
    - profile/preferences
    - history (reflections)
    - session info
    """

    def setup_user(
        self,
        user_id: str,
        courses: List[Dict[str, Any]],
        tasks: List[Dict[str, Any]],
        profile_overrides: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        state = get_user_state(user_id)

        # Save courses
        state["courses"] = courses

        # Normalize tasks
        normalized = []
        for t in tasks:
            task = dict(t)
            if "status" not in task:
                task["status"] = "pending"
            normalized.append(task)
        state["tasks"] = normalized

        # Update profile
        if profile_overrides:
            state["profile"].update(profile_overrides)

        save_user_state(user_id, state)
        return self.get_profile_summary(user_id)

    def get_profile_summary(self, user_id: str) -> Dict[str, Any]:

        state = get_user_state(user_id)
        profile = state["profile"]
        courses = state["courses"]
        tasks = state["tasks"]

        summary_text = (
            f"User is enrolled in {len(courses)} courses and has {len(tasks)} tasks. "
            f"Typical study pattern: up to {profile['max_blocks_per_day']} blocks of "
            f"{profile['preferred_block_minutes']} minutes per day."
        )

        return {
            "profile": profile,
            "courses": courses,
            "tasks": tasks,
            "summary_text": summary_text,
        }

    def get_tasks_for_planning(self, user_id: str) -> List[Dict[str, Any]]:
        state = get_user_state(user_id)
        return [t for t in state["tasks"] if t.get("status") != "done"]

    def update_tasks_and_history(
        self,
        user_id: str,
        completed_task_ids: List[str],
        partial_task_ids: List[str],
        difficulty_rating: int,
        notes: str,
        date_str: str,
    ) -> Dict[str, Any]:

        state = get_user_state(user_id)

        # Update tasks
        for task in state["tasks"]:
            tid = task["task_id"]
            if tid in completed_task_ids:
                task["status"] = "done"
            elif tid in partial_task_ids:
                task["status"] = "in_progress"

        # Append history
        entry = {
            "date": date_str,
            "completed_task_ids": completed_task_ids,
            "partial_task_ids": partial_task_ids,
            "difficulty_rating": difficulty_rating,
            "notes": notes,
        }
        state["history"].append(entry)

        save_user_state(user_id, state)
        return entry

    def get_status(self, user_id: str) -> Dict[str, Any]:
        state = get_user_state(user_id)
        tasks = state["tasks"]
        total = len(tasks)
        done = sum(1 for t in tasks if t["status"] == "done")

        return {
            "total_tasks": total,
            "completed_tasks": done,
            "completion_rate": done / total if total else 0.0,
            "profile": state["profile"],
            "history_count": len(state["history"]),
        }

    # ------------ SESSION METHODS ----------------

    def start_or_continue_session(self, user_id: str, session_id: str | None = None) -> Dict[str, Any]:
        state = get_user_state(user_id)
        session = state.get("session", {})
        now = datetime.utcnow().isoformat(timespec="seconds")

        if session_id is None:
            session_id = f"session-{now}"

        session["current_session_id"] = session_id
        session["last_interaction_at"] = now
        session["interaction_count"] = session.get("interaction_count", 0) + 1

        state["session"] = session
        save_user_state(user_id, state)
        return session

    def get_session_info(self, user_id: str) -> Dict[str, Any]:
        state = get_user_state(user_id)
        return state.get("session", {})
