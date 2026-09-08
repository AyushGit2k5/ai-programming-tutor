import json
import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from backend.app.prompts.tutor_prompt import build_tutor_prompt
from backend.app.schemas import (
    ProgrammingLanguage,
    TutorModelOutput,
)
from backend.app.services.session_service import format_history


load_dotenv(override=True)


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY was not found. "
        "Make sure it exists in your .env file."
    )


client = Groq(
    api_key=api_key,
)


def clean_json_response(content: str) -> str:
    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]

    elif content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    return content.strip()


def generate_hint(
    code: str,
    language: ProgrammingLanguage,
    hint_level: int,
    static_analysis: str,
    previous_interactions: list,
) -> TutorModelOutput:

    history_text = format_history(previous_interactions)

    prompt = build_tutor_prompt(
        code=code,
        language=language,
        hint_level=hint_level,
        static_analysis=static_analysis,
        history_text=history_text,
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an educational programming tutor. "
                    "Follow the tutoring policy exactly and return "
                    "only valid JSON."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.25,
        max_tokens=500,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "The AI model returned an empty response."
        )

    cleaned_content = clean_json_response(content)

    try:
        parsed_json = json.loads(cleaned_content)

        return TutorModelOutput.model_validate(parsed_json)

    except (json.JSONDecodeError, ValidationError) as error:
        raise RuntimeError(
            "The AI model returned an invalid structured response."
        ) from error