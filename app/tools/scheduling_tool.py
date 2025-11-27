# app/tools/scheduling_tool.py

from datetime import datetime, time, timedelta
from typing import List, Dict, Any, Tuple


def _parse_time(t: str) -> time:
    """Parse 'HH:MM' into a time object."""
    return datetime.strptime(t, "%H:%M").time()


def _split_into_blocks(start: time, end: time, block_minutes: int) -> List[Tuple[time, time]]:
    """
    Split a time window into fixed-length blocks.
    Example: 19:00–21:00 with 45 min blocks -> [(19:00, 19:45), (19:45, 20:30)]
    """
    blocks: List[Tuple[time, time]] = []
    current = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)
    delta = timedelta(minutes=block_minutes)

    while current + delta <= end_dt:
        block_start = current.time()
        block_end = (current + delta).time()
        blocks.append((block_start, block_end))
        current += delta

    return blocks


def schedule_day(
    tasks: List[Dict[str, Any]],
    date_str: str,
    available_windows: List[Dict[str, str]],
    block_minutes: int = 45,
    max_blocks_per_day: int = 3,
) -> List[Dict[str, Any]]:
    """
    Very simple scheduling function for one day.

    Args:
        tasks: list of task dicts. Each task should have at least:
               - task_id
               - course_id
               - title
               - deadline_date (YYYY-MM-DD string)
        date_str: the target date for planning (YYYY-MM-DD).
        available_windows: list of {"start": "HH:MM", "end": "HH:MM"} for that date.
        block_minutes: length of each study block.
        max_blocks_per_day: safety cap for how many blocks to schedule.

    Returns:
        List of study block dicts with:
           - date, start_time, end_time, task_id, course_id, title, priority
    """

    if not tasks or not available_windows:
        return []

    # Sort tasks by deadline (earliest first)
    def _deadline_key(task: Dict[str, Any]) -> datetime:
        return datetime.strptime(task["deadline_date"], "%Y-%m-%d")

    sorted_tasks = sorted(tasks, key=_deadline_key)

    # Generate all available blocks for the day
    all_blocks: List[Tuple[time, time]] = []
    for window in available_windows:
        start = _parse_time(window["start"])
        end = _parse_time(window["end"])
        all_blocks.extend(_split_into_blocks(start, end, block_minutes))

    # Apply max_blocks_per_day limit
    all_blocks = all_blocks[:max_blocks_per_day]

    study_blocks: List[Dict[str, Any]] = []
    block_idx = 0

    for task in sorted_tasks:
        if block_idx >= len(all_blocks):
            break

        block_start, block_end = all_blocks[block_idx]
        block_idx += 1

        study_blocks.append(
            {
                "date": date_str,
                "start_time": block_start.strftime("%H:%M"),
                "end_time": block_end.strftime("%H:%M"),
                "task_id": task["task_id"],
                "course_id": task["course_id"],
                "title": task["title"],
                "priority": "high",  # early deadlines are high priority
            }
        )

    return study_blocks
