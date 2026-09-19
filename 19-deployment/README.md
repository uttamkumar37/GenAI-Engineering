# 19 — Deployment

## Fresher

**Concepts**: Dockerizing a FastAPI app, basic Dockerfile, environment variable management in containers.

**Resources**:
- [Docker — Get Started](https://docs.docker.com/get-started/)
- [FastAPI — Deployment with Docker](https://fastapi.tiangolo.com/deployment/docker/)

**Code** (`code/01-fresher/`):
- `Dockerfile` + `docker-compose.yml` for the capstone's FastAPI service + Postgres/pgvector

**Interview questions**:
- Why is multi-stage Docker build relevant for a Python ML/AI service specifically? (Heavy build dependencies (compilers, CUDA toolkits) don't need to ship in the final runtime image — smaller, faster, more secure image.)

## Intermediate

**Concepts**: Kubernetes basics (pods, deployments, services, config maps/secrets), horizontal scaling for stateless API layers, managing GPU resources in k8s (if self-hosting inference), health checks/readiness probes for LLM services (these need custom logic — a "ready" model server is different from a normal web server).

**Resources**:
- [Kubernetes — Basics tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

**Code** (`code/02-intermediate/`):
- `k8s-manifests/` — deployment, service, configmap, secret manifests for the capstone API
- `readiness_probe_custom.py` — a health check that verifies the LLM provider connection and vector DB connection, not just "process is running"

**Interview questions**:
- What does a meaningful health check look like for an LLM-backed service, versus a typical stateless API? (Must verify downstream dependencies — LLM provider reachability, vector DB connection, not just that the process is alive — since a "healthy" pod that can't reach its LLM provider is actually broken.)

## Advanced / Senior

**Concepts**: AWS Bedrock integration (using managed model hosting instead of self-hosting), Azure OpenAI Service integration, choosing between self-hosted k8s+vLLM vs managed cloud AI services (cost/ops tradeoff, connects back to Topic 15), CI/CD pipeline for an AI service (including eval gating from Topic 16), secrets management for multi-provider API keys at scale, blue-green or canary deployment for prompt/model changes.

**Resources**:
- [AWS Bedrock — docs](https://docs.aws.amazon.com/bedrock/)
- [Azure OpenAI Service — docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

**Code** (`code/03-advanced/`):
- `bedrock_provider_adapter.py` — add AWS Bedrock as another provider in the Topic 01/05 provider abstraction
- `ci_cd_pipeline.yml` — full pipeline: test → eval-gate (Topic 16) → build → canary deploy

**Interview questions**:
- Your company wants to migrate from direct Anthropic API calls to AWS Bedrock for compliance reasons. What changes, and what stays the same in your architecture? (If you built a proper provider abstraction from Topic 01/05, only the adapter changes — this is exactly why that abstraction mattered; also discuss latency/feature-parity differences to validate.)

## Milestone

The capstone deployed via Docker + k8s manifests (can run locally via minikube/kind if no cloud budget), with at least one managed-cloud-provider integration wired into the provider abstraction.
