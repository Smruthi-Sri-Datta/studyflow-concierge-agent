# app/llm/tools.py

from typing import Any, Dict, List

from app.llm.client import get_llm_client
from app.llm.prompts import PLAN_SUMMARY_TEMPLATE, REFLECTION_FEEDBACK_TEMPLATE


def _safe_text(response) -> str:
    """
    Safely extract model text output across Gemini APIs.
    """
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        if isinstance(response, dict) and "text" in response:
            return response["text"].strip()
    except Exception:
        pass

    return str(response)


# ----------------------------------------------------------
#   PLAN SUMMARY — With LLM + fallback
# ----------------------------------------------------------

def generate_plan_summary(profile_summary: str, blocks: List[Dict[str, Any]]) -> str:
    """
    Return a natural-language summary of the plan for the day.
    Uses Gemini 2.5 if available; uses rule-based fallback otherwise.
    """
    try:
        model = get_llm_client()

        # Format prompt using your custom template file
        prompt = PLAN_SUMMARY_TEMPLATE.format(
            profile_summary=profile_summary,
            blocks=blocks,
        )

        response = model.generate_content(prompt)
        return _safe_text(response)

    except Exception as e:
        # Safe fallback – never break planning
        block_lines = "\n".join(
            f"- {b['date']} {b['start_time']}-{b['end_time']} | {b['title']} ({b['course_id']})"
            for b in blocks
        )

        return (
            "Plan summary (Fallback Mode):\n"
            f"{profile_summary}\n\n"
            "Today's blocks:\n"
            f"{block_lines}\n\n"
            f"(LLM failed: {type(e).__name__})"
        )


# ----------------------------------------------------------
#   REFLECTION FEEDBACK — With LLM + fallback
# ----------------------------------------------------------

def generate_reflection_feedback(history_entry: Dict[str, Any],
                                 status: Dict[str, Any]) -> str:
    """
    Generate supportive reflection feedback using Gemini.
    Falls back to a friendly, rule-based version if LLM call fails.
    """
    try:
        model = get_llm_client()

        # Fill reflection template
        prompt = REFLECTION_FEEDBACK_TEMPLATE.format(
            history_entry=history_entry,
            status=status,
        )

        response = model.generate_content(prompt)
        return _safe_text(response)

    except Exception as e:
        # Extract fields safely
        completed = len(history_entry.get("completed_task_ids", []))
        partial = len(history_entry.get("partial_task_ids", []))
        diff = history_entry.get("difficulty_rating", "?")

        return (
            "Reflection feedback (Fallback Mode):\n"
            f"- Completed: {completed}, Partial: {partial}\n"
            f"- Difficulty: {diff}/5\n"
            "Try to start with the hardest topic next time, "
            "take small breaks, and keep building consistency.\n"
            f"(LLM failed: {type(e).__name__})"
        )
