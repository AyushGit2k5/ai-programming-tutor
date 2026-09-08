from typing import Dict, List
from uuid import uuid4

from backend.app.schemas import ErrorType, ProgrammingLanguage


sessions: Dict[str, List[dict]] = {}


def create_session() -> str:
    session_id = str(uuid4())

    sessions[session_id] = []

    return session_id


def get_session(session_id: str):
    return sessions.get(session_id)


def add_interaction(
    session_id: str,
    code: str,
    language: ProgrammingLanguage,
    hint_level: int,
    hint: str,
    error_type: ErrorType,
    concept: str,
):
    if session_id not in sessions:
        sessions[session_id] = []

    sessions[session_id].append(
        {
            "code": code,
            "language": language.value,
            "hint_level": hint_level,
            "hint": hint,
            "error_type": error_type.value,
            "concept": concept,
        }
    )


def reset_session(session_id: str) -> bool:
    if session_id not in sessions:
        return False

    del sessions[session_id]

    return True


def format_history(history: List[dict]) -> str:
    if not history:
        return "No previous tutoring interactions."

    recent_history = history[-5:]

    formatted_items = []

    for index, interaction in enumerate(
        recent_history,
        start=1,
    ):
        formatted_items.append(
            f"""
Attempt {index}

Language:
{interaction["language"]}

Hint level:
{interaction["hint_level"]}

Previous code:
{interaction["code"]}

Previous hint:
{interaction["hint"]}

Previous error classification:
{interaction["error_type"]}

Previous concept:
{interaction["concept"]}
"""
        )

    return "\n".join(formatted_items)