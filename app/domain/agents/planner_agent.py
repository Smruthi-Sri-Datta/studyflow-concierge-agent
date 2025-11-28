# app/domain/agents/planner_agent.py

from typing import Any, Dict, List

from app.domain.agents.memory_agent import MemoryAgent
from app.domain.tools.scheduling_tool import schedule_day
from app.llm.tools import generate_plan_summary


class PlannerAgent:
    """
    Agent responsible for planning study blocks for a given day.
    """

    def __init__(self, memory_agent: MemoryAgent | None = None):
        self.memory_agent = memory_agent or MemoryAgent()

    def plan_day(
        self,
        user_id: str,
        date_str: str,
        available_windows: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        # Get profile summary and tasks from memory
        profile_summary = self.memory_agent.get_profile_summary(user_id)
        tasks = self.memory_agent.get_tasks_for_planning(user_id)

        # Use scheduling tool to create concrete blocks
        blocks = schedule_day(tasks, date_str, available_windows)

        # LLM summary of the plan
        summary_text = profile_summary["summary_text"]
        plan_summary = generate_plan_summary(summary_text, blocks)

        return {
            "profile_summary": summary_text,
            "planned_blocks": blocks,
            "plan_summary_text": plan_summary,
        }
