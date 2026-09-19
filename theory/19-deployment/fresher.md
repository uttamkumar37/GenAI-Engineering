# 19 — Deployment — Fresher

**Concepts**: Dockerizing a FastAPI app, basic Dockerfile, environment variable management in containers.

**Resources**:
- [Docker — Get Started](https://docs.docker.com/get-started/)
- [FastAPI — Deployment with Docker](https://fastapi.tiangolo.com/deployment/docker/)

**Code** (`code/19-deployment/01-fresher/`):
- `Dockerfile` + `docker-compose.yml` for the capstone's FastAPI service + Postgres/pgvector

**Interview questions**:
- Why is multi-stage Docker build relevant for a Python ML/AI service specifically? (Heavy build dependencies (compilers, CUDA toolkits) don't need to ship in the final runtime image — smaller, faster, more secure image.)
