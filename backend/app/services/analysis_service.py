import ast

from backend.app.schemas import ProgrammingLanguage


def analyse_python(code: str) -> str:
    try:
        ast.parse(code)

        return (
            "Python parser result: No syntax error was detected. "
            "The issue may instead involve logic, runtime behaviour, "
            "algorithm design, or code quality."
        )

    except SyntaxError as error:
        line = error.lineno or "unknown"
        column = error.offset or "unknown"
        message = error.msg or "Unknown syntax error"

        return (
            "Python parser detected a syntax error.\n"
            f"Line: {line}\n"
            f"Column: {column}\n"
            f"Parser message: {message}\n"
            "Use this diagnostic to guide the student, but respect "
            "the selected hint level."
        )


def analyse_code(
    code: str,
    language: ProgrammingLanguage,
) -> str:

    if language == ProgrammingLanguage.python:
        return analyse_python(code)

    return (
        f"No deterministic parser is currently configured for "
        f"{language.value}. Analyse the code using the language rules "
        "and reasoning available to you."
    )