# 19 — Deployment — Intermediate

**Concepts**: Kubernetes basics (pods, deployments, services, config maps/secrets), horizontal scaling for stateless API layers, managing GPU resources in k8s (if self-hosting inference), health checks/readiness probes for LLM services (these need custom logic — a "ready" model server is different from a normal web server).

**Resources**:
- [Kubernetes — Basics tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

**Code** (`code/19-deployment/02-intermediate/`):
- `k8s-manifests/` — deployment, service, configmap, secret manifests for the capstone API
- `readiness_probe_custom.py` — a health check that verifies the LLM provider connection and vector DB connection, not just "process is running"

**Interview questions**:
- What does a meaningful health check look like for an LLM-backed service, versus a typical stateless API? (Must verify downstream dependencies — LLM provider reachability, vector DB connection, not just that the process is alive — since a "healthy" pod that can't reach its LLM provider is actually broken.)
