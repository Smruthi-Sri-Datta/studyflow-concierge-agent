# app/agents/reflection_agent.py

from datetime import datetime
from typing import Any, Dict, List

from app.agents.memory_agent import MemoryAgent
from app.memory.store import get_user_state, save_user_state


class ReflectionAgent:
    """
    Agent responsible for:
    - taking user feedback after a study session
    - updating task statuses and simple preferences
    """

    def __init__(self, memory_agent: MemoryAgent | None = None):
        self.memory_agent = memory_agent or MemoryAgent()

    def reflect(
        self,
        user_id: str,
        completed_task_ids: List[str],
        partial_task_ids: List[str],
        difficulty_rating: int,
        notes: str,
        date_str: str | None = None,
    ) -> Dict[str, Any]:
        if date_str is None:
            date_str = datetime.today().strftime("%Y-%m-%d")

        # Update tasks and history via MemoryAgent
        history_entry = self.memory_agent.update_tasks_and_history(
            user_id=user_id,
            completed_task_ids=completed_task_ids,
            partial_task_ids=partial_task_ids,
            difficulty_rating=difficulty_rating,
            notes=notes,
            date_str=date_str,
        )

        # Simple adaptation rule for profile:
        # - if user struggled (rating >=4 and many partial tasks), reduce max_blocks_per_day
        # - if user found it easy (rating <=2 and all tasks done), increase max_blocks_per_day (up to 5)
        state = get_user_state(user_id)
        profile = state["profile"]
        max_blocks = profile.get("max_blocks_per_day", 3)

        if difficulty_rating >= 4 and len(partial_task_ids) > 0:
            max_blocks = max(1, max_blocks - 1)
        elif difficulty_rating <= 2 and len(partial_task_ids) == 0 and len(completed_task_ids) >= max_blocks:
            max_blocks = min(5, max_blocks + 1)

        profile["max_blocks_per_day"] = max_blocks
        state["profile"] = profile
        save_user_state(user_id, state)

        return {
            "history_entry": history_entry,
            "updated_profile": profile,
        }
