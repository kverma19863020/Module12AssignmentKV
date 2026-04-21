# Reflection — Module 12

## Overview
This module required implementing user registration and login endpoints with
secure bcrypt password hashing, full BREAD calculation endpoints backed by
PostgreSQL, integration tests using pytest with a live test database, and a
CI/CD pipeline via GitHub Actions that auto-deploys to Docker Hub.

## Key Experiences

### FastAPI + SQLAlchemy
Using Depends(get_db) for dependency injection kept database session
management clean and fully testable. Defining response_model on every
route enforced proper Pydantic validation on all outputs automatically.

### Password Security
Using passlib with bcrypt ensures passwords are never stored in plain text.
The verify_password function compares hashes safely without exposing the
original password anywhere in the codebase or logs.

### Integration Testing
The biggest challenge was configuring conftest.py to use transaction
rollbacks per test so each test gets a clean database state without
dropping and recreating tables each time. This made the full test suite
fast and completely isolated.

### CI/CD Pipeline
Configuring GitHub Actions to spin up a Postgres service container, run
pytest against it, and then push a Docker image to Docker Hub on success
required careful use of needs: job ordering and GitHub repository secrets
for Docker Hub credentials.

## Challenges
- Ensuring updated_at was correctly handled in SQLAlchemy with onupdate
- Making per-test transaction rollback work correctly with FastAPI dependency
  override system
- Restricting Docker Hub push to only main branch pushes, not PRs

## Conclusion
This assignment brought together all layers of a production-ready Python API:
data modeling, business logic, HTTP routing, security, testing, and automated
deployment providing a complete backend ready for a frontend in Module 13.
