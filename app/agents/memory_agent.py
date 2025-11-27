# app/agents/memory_agent.py

from typing import Any, Dict, List

from app.memory.store import get_user_state, save_user_state


class MemoryAgent:
    """
    Agent responsible for managing long-term state for a user:
    - courses
    - tasks
    - simple profile/preferences
    - history (reflections)
    """

    def setup_user(
        self,
        user_id: str,
        courses: List[Dict[str, Any]],
        tasks: List[Dict[str, Any]],
        profile_overrides: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """
        Initialize or update a user's courses, tasks and profile.
        """
        state = get_user_state(user_id)

        # Replace courses and tasks with provided ones
        state["courses"] = courses

        # Ensure each task has a status field
        normalized_tasks: List[Dict[str, Any]] = []
        for t in tasks:
            task = dict(t)
            if "status" not in task:
                task["status"] = "pending"  # pending | in_progress | done
            normalized_tasks.append(task)
        state["tasks"] = normalized_tasks

        # Update profile preferences if provided
        if profile_overrides:
            state["profile"].update(profile_overrides)

        save_user_state(user_id, state)
        return self.get_profile_summary(user_id)

    def get_profile_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Return a compact summary of the user's state for context.
        """
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
        """
        Return tasks that are not yet completed.
        """
        state = get_user_state(user_id)
        return [t for t in state["tasks"] if t.get("status", "pending") != "done"]

    def update_tasks_and_history(
        self,
        user_id: str,
        completed_task_ids: List[str],
        partial_task_ids: List[str],
        difficulty_rating: int,
        notes: str,
        date_str: str,
    ) -> Dict[str, Any]:
        """
        Update task statuses and append a history record.
        """
        state = get_user_state(user_id)

        # Update task statuses
        for task in state["tasks"]:
            tid = task.get("task_id")
            if tid in completed_task_ids:
                task["status"] = "done"
            elif tid in partial_task_ids:
                task["status"] = "in_progress"

        # Append to history
        history_entry = {
            "date": date_str,
            "completed_task_ids": completed_task_ids,
            "partial_task_ids": partial_task_ids,
            "difficulty_rating": difficulty_rating,
            "notes": notes,
        }
        state["history"].append(history_entry)

        save_user_state(user_id, state)
        return history_entry

    def get_status(self, user_id: str) -> Dict[str, Any]:
        """
        Return a simple progress/status overview.
        """
        state = get_user_state(user_id)
        tasks = state["tasks"]
        total = len(tasks)
        done = sum(1 for t in tasks if t.get("status") == "done")

        return {
            "total_tasks": total,
            "completed_tasks": done,
            "completion_rate": (done / total) if total > 0 else 0.0,
            "profile": state["profile"],
            "history_count": len(state["history"]),
        }
