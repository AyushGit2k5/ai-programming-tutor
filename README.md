# AI Programming Tutor

An AI-powered programming tutor that provides progressive, educational hints without immediately revealing the solution.

Instead of simply generating corrected code, the system guides students toward understanding and fixing programming problems themselves.

## Features

- Progressive three-level hint system
- Support for Python, Java, JavaScript, C++, and C#
- Syntax, runtime, logic, algorithm, and code-quality error classification
- Programming concept identification
- Approximate problem-location detection
- Session-based tutoring history
- Previous-attempt awareness
- Python AST syntax validation
- Groq-powered LLM analysis
- FastAPI backend
- Responsive web interface
- REST API with automatic Swagger documentation
- Environment-variable based API key management

## Hint Levels

### Level 1 — Subtle Nudge

Provides a small clue without directly identifying the exact solution.

The goal is to point the student toward the relevant area of the code while encouraging independent problem solving.

### Level 2 — Guided Help

Provides more targeted guidance by identifying the relevant programming concept or area of the code.

The student receives additional direction without immediately receiving the complete solution.

### Level 3 — Detailed Explanation

Provides a more detailed explanation of the underlying problem and programming concept.

The tutor can be more specific while still prioritising explanation over simply rewriting the student's program.

## How It Works

The application follows this general tutoring pipeline:

    Student Code
         |
         v
    Language + Hint Level
         |
         v
    Static Analysis
         |
         v
    Session History
         |
         v
    Tutoring Prompt
         |
         v
    Groq LLM
         |
         v
    Structured Response
         |
         +-- Hint
         +-- Error Type
         +-- Concept
         +-- Location

For Python submissions, the application first performs deterministic syntax analysis using Python's built-in AST parser.

The resulting diagnostic information is provided to the tutoring system alongside the student's selected hint level and previous tutoring history.

The LLM then generates a structured educational response rather than simply returning corrected code.

## Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- Groq API

### Frontend

- HTML
- CSS
- JavaScript

### Static Analysis

- Python AST

## Project Structure

    ai-programming-tutor/
    |
    +-- backend/
    |   +-- app/
    |       +-- __init__.py
    |       +-- main.py
    |       +-- schemas.py
    |
    |       +-- prompts/
    |       |   +-- __init__.py
    |       |   +-- tutor_prompt.py
    |       |
    |       +-- services/
    |       |   +-- __init__.py
    |       |   +-- tutor_service.py
    |       |   +-- analysis_service.py
    |       |   +-- session_service.py
    |       |
    |       +-- static/
    |           +-- index.html
    |           +-- styles.css
    |           +-- app.js
    |
    +-- .env
    +-- .gitignore
    +-- requirements.txt
    +-- README.md

## Installation

### 1. Clone the Repository

    git clone YOUR_REPOSITORY_URL

Then enter the project directory:

    cd ai-programming-tutor

### 2. Create a Virtual Environment

On Windows:

    python -m venv .venv

Activate it using PowerShell:

    .venv\Scripts\Activate.ps1

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Configure the Groq API Key

Create a file named:

    .env

in the project root.

Add:

    GROQ_API_KEY=your_groq_api_key_here

Never commit your real API key to GitHub.

The .env file is excluded from version control through .gitignore.

## Running the Application

Activate the virtual environment if it is not already active:

    .venv\Scripts\Activate.ps1

Start the FastAPI application:

    python -m uvicorn backend.app.main:app --reload

The development server should start at:

    http://127.0.0.1:8000

## Web Interface

Open:

    http://127.0.0.1:8000

The web interface allows the user to:

- Select a programming language
- Select a hint level
- Enter normal multi-line source code
- Request an AI-generated hint
- View the detected error category
- View the relevant programming concept
- View the approximate location of the problem
- Request additional hints during the same tutoring session
- Reset the tutoring session

## API Documentation

FastAPI automatically provides Swagger documentation.

Open:

    http://127.0.0.1:8000/docs

The main tutoring endpoint is:

    POST /api/hint

The endpoint accepts:

- Programming language
- Hint level
- Optional session ID
- Source code as plain text

It returns a structured response containing:

- Session ID
- Programming language
- Hint level
- Attempt number
- Educational hint
- Error type
- Programming concept
- Approximate problem location

## Error Classification

The tutor classifies the primary issue using one of the following categories:

- syntax
- runtime
- logic
- algorithm
- code_quality
- unknown

This provides additional structure beyond a standard conversational LLM response.

## Session-Aware Tutoring

Each tutoring interaction can belong to a session.

The application stores previous:

- Code attempts
- Hint levels
- Generated hints
- Error classifications
- Programming concepts

This context allows later hints to take previous attempts into account instead of simply generating the same response repeatedly.

The current implementation stores sessions in memory.

Restarting the server therefore clears existing sessions.

## Python Static Analysis

Python submissions are analysed using Python's built-in ast module before being sent to the LLM.

For example, the parser can detect syntax errors and provide information such as:

- Line number
- Column number
- Parser error message

This diagnostic information is then supplied to the tutoring system.

The application parses Python code but does not directly execute arbitrary student code.

## Structured AI Output

The model is instructed to return structured information containing:

    {
        "hint": "Educational hint for the student",
        "error_type": "syntax",
        "concept": "Conditional statements",
        "location": "The if statement near line 3"
    }

Pydantic validates the model output before it is returned through the API.

This makes the AI response easier for the frontend and other applications to consume reliably.

## Security

API credentials are stored using environment variables.

The following files and directories are excluded from Git:

- .env
- .venv
- Python cache files
- IDE configuration files
- Local databases
- Logs

Never place a Groq API key directly inside Python or JavaScript source code.

If an API key is accidentally exposed publicly, revoke it and generate a new one.

## Current Limitations

- Session state is stored only in memory.
- Sessions are lost when the backend restarts.
- Deterministic syntax analysis currently supports Python only.
- Other supported languages currently rely primarily on LLM analysis.
- The application does not currently execute student programs.
- Authentication and user accounts are not currently implemented.
- The application is currently intended for development and educational use.

## Future Improvements

Potential future improvements include:

- Persistent sessions using PostgreSQL or Redis
- Monaco Editor integration
- Sandboxed code execution
- Automated test-case analysis
- User authentication
- Student progress tracking
- Hint-effectiveness evaluation
- More deterministic language parsers
- Additional programming languages
- Automated backend tests
- Docker support
- Cloud deployment
- Rate limiting and production API protections

## Purpose

The project explores how large language models can be used as structured programming tutors rather than simple solution generators.

The system combines deterministic analysis, progressive tutoring policies, session context, structured LLM output, API development, and a dedicated frontend to provide assistance based on how much help the student requests.