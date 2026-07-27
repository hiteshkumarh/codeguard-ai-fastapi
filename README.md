# CodeGuard AI

AI-assisted static code analysis platform built with a decoupled
frontend and FastAPI backend. CodeGuard AI analyzes source code for
security vulnerabilities, code-quality problems, risky patterns, and
potential logical issues using custom static analyzers and optional
Groq-powered AI review.

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Architecture](#architecture)
-   [Tech Stack](#tech-stack)
-   [Project Structure](#project-structure)
-   [API Endpoints](#api-endpoints)
-   [Getting Started](#getting-started)
-   [Environment Variables](#environment-variables)
-   [Running the Backend](#running-the-backend)
-   [Running the Frontend](#running-the-frontend)
-   [Running Tests](#running-tests)
-   [Docker](#docker)
-   [Deployment](#deployment)
-   [Security](#security)
-   [Limitations](#limitations)
-   [Future Improvements](#future-improvements)

## Overview

CodeGuard AI is a full-stack code-analysis application designed to help
developers identify potentially unsafe code, bugs, code smells, and
maintainability issues.

The application combines deterministic static-analysis rules with
optional AI-assisted review through the Groq API. The frontend and
backend are completely separated and communicate through versioned REST
APIs.

The project currently supports a Python-based analysis pipeline and
includes a dedicated Node.js module for JavaScript-specific analysis.

## Features

-   **Static Code Analysis** --- Detects predefined security and
    code-quality patterns without requiring an LLM.
-   **AI-Assisted Review** --- Uses Groq to provide additional
    code-quality and potential issue analysis.
-   **Python Analysis** --- Custom Python analyzer for detecting risky
    patterns.
-   **JavaScript Analysis** --- Separate Node.js analyzer for
    JavaScript-specific processing.
-   **Severity Classification** --- Analysis findings can be categorized
    by severity.
-   **Analysis History** --- Stores analysis reports for later
    retrieval.
-   **Report Details** --- Retrieve individual reports using report IDs.
-   **Decoupled Frontend and Backend** --- Frontend communicates with
    FastAPI exclusively through REST APIs.
-   **Interactive API Documentation** --- Swagger UI and OpenAPI
    documentation are generated automatically by FastAPI.
-   **Environment-Based Configuration** --- Secrets and CORS
    configuration are loaded through environment variables.
-   **Docker Support** --- Backend and frontend can be orchestrated
    using Docker Compose.
-   **Automated Tests** --- Pytest coverage for critical backend
    behavior.

## Architecture

CodeGuard AI uses a decoupled full-stack architecture.

``` text
┌─────────────────────────────┐
│          Frontend           │
│    HTML / CSS / JavaScript  │
└──────────────┬──────────────┘
               │
               │ REST API / JSON
               ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│ Routes / Validation / CORS  │
└──────────────┬──────────────┘
               │
               ▼
        ┌──────────────┐
        │ Service Layer│
        └──────┬───────┘
               │
       ┌───────┼──────────┐
       ▼       ▼          ▼
   Static    Groq AI   Repository
  Analyzers   Service      Layer
       │                    │
       │                    ▼
       │                  SQLite
       │
       └──────► JavaScript Analyzer
                  Node.js
```

The backend follows a layered modular architecture:

``` text
API Routes
    ↓
Services
    ↓
Analyzers / AI Integration
    ↓
Repositories
    ↓
Database
```

### Backend Responsibilities

-   API routing
-   Request and response validation
-   CORS handling
-   Static-analysis orchestration
-   Groq API integration
-   Database persistence
-   Report retrieval
-   Application configuration

### Frontend Responsibilities

-   Code input
-   File selection and client-side interaction
-   REST API communication
-   Analysis-result presentation
-   Historical report navigation

## Tech Stack

  Layer                 Technology
  --------------------- ---------------------------------
  Frontend              HTML5, CSS3, Vanilla JavaScript
  Backend               Python 3.12, FastAPI
  Validation            Pydantic
  Configuration         pydantic-settings
  ORM                   SQLAlchemy
  Database              SQLite
  AI                    Groq API
  LLM                   `llama-3.1-8b-instant`
  JavaScript Analysis   Node.js
  API Server            Uvicorn
  Testing               Pytest
  Containerization      Docker, Docker Compose

## Project Structure

``` text
codeguard-ai-fastapi/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   │       ├── analysis.py
│   │   │       ├── health.py
│   │   │       └── results.py
│   │   │
│   │   ├── analyzers/
│   │   │   ├── base_analyzer.py
│   │   │   ├── code_analyzer.py
│   │   │   ├── js_analyzer.py
│   │   │   └── python_analyzer.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   │
│   │   ├── db/
│   │   │   └── database.py
│   │   │
│   │   ├── dependencies/
│   │   ├── models/
│   │   │   └── analysis.py
│   │   │
│   │   ├── repositories/
│   │   │   └── result_repository.py
│   │   │
│   │   ├── schemas/
│   │   │   └── analysis.py
│   │   │
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   └── analysis_service.py
│   │   │
│   │   ├── utils/
│   │   │   └── language_detector.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_analysis.py
│   │   └── test_health.py
│   │
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── api.js
│   │   └── app.js
│   └── pages/
│       └── results.html
│
├── js-analyzer/
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── render.yaml
└── README.md
```

## API Endpoints

All application APIs use the `/api/v1` prefix.

  ------------------------------------------------------------------------------
  Method                  Endpoint                       Description
  ----------------------- ------------------------------ -----------------------
  `POST`                  `/api/v1/analyze`              Analyze submitted
                                                         source code

  `GET`                   `/api/v1/reports`              Retrieve paginated
                                                         report summaries

  `GET`                   `/api/v1/report/{report_id}`   Retrieve a specific
                                                         analysis report

  `GET`                   `/api/v1/results`              Retrieve the most
                                                         recent analysis result
                                                         for frontend rendering

  `GET`                   `/api/v1/health`               Check backend service
                                                         health
  ------------------------------------------------------------------------------

When the backend is running, interactive Swagger documentation is
available at:

``` text
http://127.0.0.1:8000/docs
```

## Getting Started

### Prerequisites

Install the following before running the project locally:

-   Python 3.12+
-   pip
-   Node.js and npm
-   Git

Docker is optional.

### 1. Clone the Repository

``` bash
git clone https://github.com/hiteshkumarh/codeguard-ai-fastapi.git
cd codeguard-ai-fastapi
```

### 2. Create a Python Virtual Environment

From the repository root:

``` bash
python -m venv .venv
```

Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

``` cmd
.venv\Scripts\activate
```

Linux/macOS:

``` bash
source .venv/bin/activate
```

### 3. Install Backend Dependencies

``` bash
cd backend
pip install -r requirements.txt
```

### 4. Install JavaScript Analyzer Dependencies

From the repository root:

``` bash
cd js-analyzer
npm install
```

Then return to the repository root.

## Environment Variables

Copy the example configuration:

``` text
backend/.env.example
```

to:

``` text
backend/.env
```

Example:

``` env
GROQ_API_KEY=your_groq_api_key_here
FRONTEND_CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

`GROQ_API_KEY` enables AI-assisted analysis through Groq.

`FRONTEND_CORS_ORIGINS` defines which frontend origins may access the
backend during browser-based development.

### Important

Never commit your real `.env` file or API keys.

The repository should ignore local environment files:

``` gitignore
.env
.env.*
!.env.example
backend/.env
```

If no valid Groq API key is configured, the application can continue
using its local static-analysis capabilities where supported by the
current configuration.

## Running the Backend

Activate the virtual environment and move into the backend directory:

``` powershell
cd backend
```

Start FastAPI:

``` bash
uvicorn app.main:app --reload
```

The backend runs at:

``` text
http://127.0.0.1:8000
```

Swagger UI:

``` text
http://127.0.0.1:8000/docs
```

Health endpoint:

``` text
http://127.0.0.1:8000/api/v1/health
```

A `404` response for `GET /` on port `8000` is expected because the
backend is API-only and does not serve the frontend.

## Running the Frontend

Open a second terminal and move into the frontend directory:

``` bash
cd frontend
```

Start a basic local HTTP server:

``` bash
python -m http.server 5500
```

Open:

``` text
http://localhost:5500
```

The frontend and backend must both be running during local development.

``` text
Frontend: http://localhost:5500
Backend:  http://127.0.0.1:8000
Swagger:  http://127.0.0.1:8000/docs
```

Do not open `index.html` directly through a `file://` URL because the
application is designed to communicate with the backend over HTTP.

## Running Tests

Activate the Python virtual environment and enter the backend directory:

``` bash
cd backend
```

Run:

``` bash
pytest
```

The test suite covers critical behavior including:

-   Health endpoint
-   Analysis endpoint
-   Request validation
-   Static-analysis behavior

## Docker

The repository includes:

``` text
backend/Dockerfile
docker-compose.yml
```

To build and start the configured services:

``` bash
docker compose up --build
```

To stop them:

``` bash
docker compose down
```

The backend Docker image includes the runtime requirements needed for
the JavaScript analyzer according to the current project configuration.

## Deployment

The repository contains `render.yaml` for deployment configuration.

Before deployment:

1.  Configure `GROQ_API_KEY` as a secret/environment variable on the
    hosting platform.
2.  Configure the allowed production frontend origin.
3.  Never place production secrets in `render.yaml`, Dockerfiles,
    frontend JavaScript, or source code.
4.  Verify the frontend API base URL points to the deployed backend.
5.  Verify the JavaScript analyzer runtime is available in the deployed
    backend environment.

SQLite is appropriate for local development and small single-instance
deployments, but a production deployment requiring multiple instances or
significant concurrent writes should use a production database such as
PostgreSQL.

## Security

CodeGuard AI follows several basic security practices:

-   API keys are loaded from environment variables.
-   Groq credentials remain backend-only.
-   CORS origins are configurable.
-   Request payloads are validated using Pydantic.
-   Frontend and backend responsibilities are separated.
-   Secrets should never be committed to Git.

If an API key is accidentally committed or exposed in a prompt, log,
screenshot, or public repository, revoke it and generate a new key.

## Limitations

-   AI-generated findings can contain false positives or incorrect
    severity classifications.
-   AI analysis should not be treated as a replacement for professional
    security review.
-   Static-analysis coverage is limited to the rules currently
    implemented by the project.
-   JavaScript analysis depends on the separate Node.js analyzer and its
    installed dependencies.
-   SQLite is not ideal for horizontally scaled production deployments.
-   The current frontend uses Vanilla JavaScript rather than a component
    framework.
-   Analysis of an entire large repository is more limited than
    dedicated enterprise SAST platforms.

## Future Improvements

Potential improvements include:

-   Improve severity classification and reduce AI false positives.
-   Add confidence scores and explanations for findings.
-   Add more deterministic security rules.
-   Expand language support.
-   Add repository-level scanning.
-   Add GitHub repository/PR analysis.
-   Add background processing for large scans.
-   Add PostgreSQL support for larger deployments.
-   Add rate limiting and request-size limits.
-   Improve frontend result filtering and visualization.
-   Add broader integration and end-to-end test coverage.
-   Add CI/CD using GitHub Actions.
-   Add dependency and secret scanning.

## Disclaimer

CodeGuard AI is an educational and developer-assistance tool. Findings
produced by static rules or AI models should be reviewed before security
or engineering decisions are made.

## License

No license is specified unless a license file is included in this
repository.
