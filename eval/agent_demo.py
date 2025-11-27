# eval/agent_demo.py

import os
import sys

# Ensure project root is on path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import orchestrator


def main():
    user_id = "demo_user"

    # 1. Setup user with courses and tasks
    setup_payload = {
        "courses": [
            {"course_id": "DL101", "name": "Deep Learning"},
            {"course_id": "NW201", "name": "Computer Networks"},
        ],
        "tasks": [
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
        ],
        "profile": {
            "preferred_block_minutes": 45,
            "max_blocks_per_day": 2,
        },
    }

    profile_summary = orchestrator.setup_user(user_id, setup_payload)
    print("Profile summary after setup:")
    print(profile_summary["summary_text"])
    print()

    # 2. Plan for a day
    plan_payload = {
        "date": "2025-11-28",
        "available_windows": [
            {"start": "19:00", "end": "21:00"},
        ],
    }

    plan_result = orchestrator.plan_day(user_id, plan_payload)
    print("Planned blocks:")
    for b in plan_result["planned_blocks"]:
        print(b)
    print()

    # 3. Simulate reflection (assume first task completed, second partial)
    reflect_payload = {
        "completed_task_ids": ["NW201-Routing-01"],
        "partial_task_ids": ["DL101-CNN-01"],
        "difficulty_rating": 4,
        "notes": "Routing was fine, CNN math was hard.",
        "date": "2025-11-28",
    }

    reflection = orchestrator.reflect(user_id, reflect_payload)
    print("Reflection result:")
    print(reflection)
    print()

    # 4. Check status
    status = orchestrator.get_status(user_id)
    print("Current status:")
    print(status)


if __name__ == "__main__":
    main()
