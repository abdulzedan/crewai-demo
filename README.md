# Project

**CrewAI** is an AI-driven platform combining a Django backend with advanced research tooling and a Next.js frontend.
This repository demonstrates a multi-agent approach to web search, analysis, and final synthesis, built with custom CrewAI agents.

---

## Table of Contents

1. [Video Demo](#video-demo)
2. [Repository Structure](#repository-structure)
3. [Setup and Installation](#setup-and-installation)
   1. [Local Environment](#local-environment)
   2. [Docker](#docker)
4. [Backend and Frontend](#backend-and-frontend)
   1. [Backend: Python/Django](#backend-pythondjango)
   2. [Frontend: Next.js/React](#frontend-nextjsreact)
5. [How to Run the Project](#how-to-run-the-project)
6. [Deployment Options](#deployment-options)
7. [Detailed Walkthrough](#detailed-walkthrough)

---

## Video Demo

https://github.com/user-attachments/assets/d59b82e5-2ec1-40cf-a522-e8cbc57e7877

---

## Repository Structure

```plaintext
abdulzedan-crewai-demo/
├── README.md
├── docker-compose.yml
├── requirements-dev.txt
├── requirements.txt
├── stored_output.txt
├── .pre-commit-config.yaml
├── backend/
│   ├── Dockerfile                # Docker instructions for the Django backend
│   ├── MANIFEST.in
│   ├── db.sqlite3                # Local dev database (SQLite)
│   ├── manage.py
│   ├── pyproject.toml            # Main Python dependencies (CrewAI backend)
│   ├── pytest.ini
│   ├── setup.cfg
│   ├── app/                      # Main Django app code
│   ├── crewai_backend/           # Django project code
│   ├── crewai_config/            # CrewAI agent/task definitions
│   └── tests/                    # Pytest-based unit tests
├── frontend/
│   ├── Dockerfile                # Docker instructions for the Next.js frontend
│   ├── package.json
│   ├── tsconfig.json
│   ├── app/                      # Next.js 13+ (App Router)
│   ├── components/
│   ├── public/
│   └── ... etc.
├── video_demo/                   # Recorded video or placeholder for video demonstration
├── .chroma-local/                # Local Chroma DB files
├── .devcontainer/                # Dev container config
└── .github/workflows/            # GitHub Actions (CI/CD)
