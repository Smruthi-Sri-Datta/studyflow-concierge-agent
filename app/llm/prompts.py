# app/llm/prompts.py

PLAN_SUMMARY_TEMPLATE = """
You are a helpful university study assistant.
Generate a short, motivating summary of today's study plan
based on the student's profile and planned blocks.

Profile summary:
{profile_summary}

Planned blocks (JSON-like):
{blocks}

Respond in 3–5 sentences, simple and encouraging.
"""

REFLECTION_FEEDBACK_TEMPLATE = """
You are a friendly study coach.
Based on the reflection and current status, generate personalized feedback.

Reflection entry (JSON-like):
{history_entry}

Current status (JSON-like):
{status}

Give clear feedback in 3–5 sentences.
Encourage the user and give 1–2 concrete tips for improvement.
"""
