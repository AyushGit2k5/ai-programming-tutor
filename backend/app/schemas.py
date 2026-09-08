from enum import Enum

from pydantic import BaseModel


class ProgrammingLanguage(str, Enum):
    python = "python"
    java = "java"
    javascript = "javascript"
    cpp = "cpp"
    csharp = "csharp"


class ErrorType(str, Enum):
    syntax = "syntax"
    runtime = "runtime"
    logic = "logic"
    algorithm = "algorithm"
    code_quality = "code_quality"
    unknown = "unknown"


class TutorModelOutput(BaseModel):
    hint: str
    error_type: ErrorType
    concept: str
    location: str


class TutorResponse(BaseModel):
    session_id: str
    language: ProgrammingLanguage
    hint_level: int
    attempt_number: int
    hint: str
    error_type: ErrorType
    concept: str
    location: str