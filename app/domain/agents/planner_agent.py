# app/agents/planner_agent.py

from typing import Any, Dict, List

from app.domain.agents.memory_agent import MemoryAgent
from app.domain.tools.scheduling_tool import schedule_day


class PlannerAgent:
    """
    Agent responsible for turning tasks + preferences into a concrete
    day-wise study plan (list of study blocks).
    """

    def __init__(self, memory_agent: MemoryAgent | None = None):
        self.memory_agent = memory_agent or MemoryAgent()

    def plan_day(
        self,
        user_id: str,
        date_str: str,
        available_windows: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Generate a plan for a given day and available time windows.
        """
        profile_summary = self.memory_agent.get_profile_summary(user_id)
        profile = profile_summary["profile"]

        tasks_for_planning = self.memory_agent.get_tasks_for_planning(user_id)

        blocks = schedule_day(
            tasks_for_planning,
            date_str,
            available_windows,
            block_minutes=profile["preferred_block_minutes"],
            max_blocks_per_day=profile["max_blocks_per_day"],
        )

        return {
            "profile_summary": profile_summary["summary_text"],
            "planned_blocks": blocks,
        }
