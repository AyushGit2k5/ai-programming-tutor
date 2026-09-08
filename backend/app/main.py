from pathlib import Path
from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.schemas import ProgrammingLanguage, TutorResponse
from backend.app.services.analysis_service import analyse_code
from backend.app.services.session_service import (
    add_interaction,
    create_session,
    get_session,
    reset_session,
)
from backend.app.services.tutor_service import generate_hint


app = FastAPI(
    title="AI Programming Tutor API",
    description=(
        "An AI-powered programming tutor that provides progressive hints "
        "without immediately revealing the solution."
    ),
    version="1.0.0",
)


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Programming Tutor API is running",
    }


@app.post("/api/hint", response_model=TutorResponse)
def create_hint(
    language: ProgrammingLanguage = Query(
        ...,
        description="Programming language used by the student",
    ),
    hint_level: int = Query(
        ...,
        ge=1,
        le=3,
        description="Hint level: 1 = subtle, 2 = guided, 3 = detailed",
    ),
    session_id: Optional[str] = Query(
        default=None,
        description="Existing tutoring session ID",
    ),
    code: str = Body(
        ...,
        media_type="text/plain",
        description="Student source code",
    ),
):
    if not code.strip():
        raise HTTPException(
            status_code=400,
            detail="Code cannot be empty.",
        )

    if session_id:
        session = get_session(session_id)

        if session is None:
            session_id = create_session()
    else:
        session_id = create_session()

    previous_interactions = get_session(session_id)

    static_analysis = analyse_code(
        code=code,
        language=language,
    )

    result = generate_hint(
        code=code,
        language=language,
        hint_level=hint_level,
        static_analysis=static_analysis,
        previous_interactions=previous_interactions,
    )

    attempt_number = len(previous_interactions) + 1

    add_interaction(
        session_id=session_id,
        code=code,
        language=language,
        hint_level=hint_level,
        hint=result.hint,
        error_type=result.error_type,
        concept=result.concept,
    )

    return TutorResponse(
        session_id=session_id,
        language=language,
        hint_level=hint_level,
        attempt_number=attempt_number,
        hint=result.hint,
        error_type=result.error_type,
        concept=result.concept,
        location=result.location,
    )


@app.delete("/api/session/{session_id}")
def delete_session(session_id: str):
    success = reset_session(session_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    return {
        "message": "Session reset successfully.",
    }