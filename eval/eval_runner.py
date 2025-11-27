# eval/eval_runner.py

import os
import sys

# Add project root to PYTHONPATH manually
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.domain.tools.scheduling_tool import schedule_day

def demo():
    tasks = [
        {
            "task_id": "DL101-CNN-01",
            "course_id": "DL101",
            "title": "Revise CNN basics",
            "deadline_date": "2025-12-05",
        },
        {
            "task_id": "NW201-Routing-01",
            "course_id": "NW201",
            "title": "Routing protocol tutorial sheet",
            "deadline_date": "2025-11-30",
        },
    ]

    date_str = "2025-11-28"

    available_windows = [
        {"start": "19:00", "end": "21:00"},
    ]

    blocks = schedule_day(tasks, date_str, available_windows)
    print("Planned study blocks:")
    for b in blocks:
        print(b)


if __name__ == "__main__":
    demo()
